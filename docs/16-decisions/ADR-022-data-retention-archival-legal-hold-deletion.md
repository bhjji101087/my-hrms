# ADR-022 - Data Retention, Archival, Legal Hold, and Deletion

Architecture Decision Record

Date: 2026-06-27
Status: Approved
Owner: Data Governance / Privacy Architect
Reviewers: Security, Database Architecture, Legal/Compliance, Platform/Operations, Product Owner

Related approved documents:

- `docs/12-security/SEC-DESIGN-001-threat-model.md`
- `docs/12-security/SEC-AI-001-ai-security-extension.md`
- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md`
- `docs/15-ai/AI-OPS-001-enterprise-ai-operations.md`
- ADR-005 Multi-Tenancy Model
- ADR-006 Tenant Context and Data Access
- ADR-007 Effective-Dated and Bitemporal Data
- ADR-008 Identity and Access Management
- ADR-009 Event-Driven Backbone
- ADR-019 Enterprise AI/RAG Platform Architecture
- ADR-030 Enterprise Vector Store Strategy
- ADR-032 Conversation Memory Strategy
- ADR-035 Semantic and Retrieval Cache Architecture

---

# Context

The HRMS stores highly sensitive employee, payroll, identity, compliance, audit, workflow,
document, integration, and AI-derived data across SQL Server, Azure Blob Storage, Redis,
Qdrant, events, backups, telemetry, and future provider systems.

The platform must support India-first privacy obligations, future GDPR expansion, tenant
offboarding, legal hold, statutory HR/payroll retention, audit immutability, data-subject
rights, backup restore, and AI derived-store deletion without weakening tenant isolation or
business audit requirements.

The existing database standard says business tables use soft delete. That remains valid for
normal transactional integrity, but privacy deletion and tenant offboarding also require
governed purge, anonymization, cryptographic erasure, tombstones, and restore-time
reconciliation for records whose lawful retention period has expired.

External basis checked on 2026-06-27:

- India's Digital Personal Data Protection Act, 2023 requires lawful purpose, consent and
  notice controls, and erasure when retention is no longer necessary except where law
  requires retention.
- GDPR requires storage limitation and includes erasure/restriction rights, subject to
  legal obligations and legal-claim exceptions.
- NIST Privacy Framework provides enterprise privacy-risk structure.
- NIST SP 800-88 Rev. 2 defines media sanitization concepts including cryptographic erase.
- Microsoft SQL Server backup guidance requires tested restore strategies.
- Azure Blob immutable storage supports retention and legal hold concepts for protected
  records.

---

# Decision

## 1. Create a governed retention policy engine

Retention, archival, legal hold, deletion, anonymization, and purge are governed by a
central policy engine. Rules are data, not code.

Every policy is:

- Tenant-scoped or platform-scoped.
- Effective-dated.
- Versioned.
- Jurisdiction-aware.
- Data-classification-aware.
- Purpose-aware.
- Approved by data governance and legal/compliance where required.
- Audited and reversible only by superseding policy version, not by editing history.

Hardcoded retention periods in feature logic are prohibited.

## 2. Separate lifecycle states

Data lifecycle states are explicit:

| State | Meaning |
|---|---|
| Active | Used for current business, support, AI, reporting, or operations. |
| SoftDeleted | Hidden from normal use but retained for business integrity, undo, audit, or workflow closure. |
| Archived | Moved or marked for lower-access retention while still legally/business required. |
| Restricted | Use is limited because of privacy request, dispute, investigation, legal hold, or tenant policy. |
| LegalHold | Retention/deletion is paused for scoped legal/regulatory reason. |
| Expired | Retention period has ended and no legal hold or statutory reason remains. |
| PurgePending | Approved deletion workflow is queued and awaiting execution/reconciliation. |
| Purged | Data is physically removed, anonymized, token-destroyed, or made unreachable according to policy. |
| Tombstoned | A minimal marker remains to prevent reappearance after restore or replay. |

Business modules may continue to use `IsDeleted` for normal soft delete. Privacy deletion
uses the governed lifecycle and must also handle derived stores, backups, and provider
residual state.

## 3. Legal hold has precedence over deletion

Legal hold blocks purge, anonymization, crypto erasure, and backup erasure for the scoped
records until the hold is released.

Every hold records:

- Tenant and affected subjects/entities.
- Legal basis, jurisdiction, issuing authority, owner, and approver.
- Scope, effective date, review date, expiry/renewal date, and release process.
- Affected systems and derived stores.
- Evidence references and audit history.

Legal hold does not grant broad access. It restricts deletion but RBAC, ABAC, RLS, masking,
purpose limitation, and audit still apply.

## 4. Statutory and contractual retention is policy data

The platform will not hardcode statutory retention periods because country, state,
employment type, payroll rule, tax rule, contract, tenant industry, and litigation status can
change.

Retention schedules are configured by:

- Country, state/region, legal entity, worker type, document class, and tenant service tier.
- Data category such as employee master, payroll, leave, attendance, recruitment,
  performance, disciplinary, grievance, workflow, audit, integration, support, and AI.
- Purpose and legal basis.
- Minimum retention, maximum retention, archive trigger, purge trigger, and hold behavior.

Default platform templates may be provided, but a tenant-specific legal owner must approve
activation.

## 5. Tenant isolation applies to all retention operations

Every retention, archival, deletion, purge, hold, restore-reconciliation, and evidence
operation is tenant-scoped.

Controls:

- SQL Server RLS remains active for tenant-scoped governance tables.
- Background jobs run with explicit audited tenant system context.
- Cross-tenant bulk operations are prohibited unless executed by a platform role with
  bounded tenant list, reason, approval, preview, and audit.
- Tenant administrators can manage only own-tenant policy where delegated and cannot weaken
  platform maximums or legal holds.
- Metrics and evidence expose only authorized tenant data.

## 6. Use deletion methods appropriate to storage type

| Storage | Primary method | Notes |
|---|---|---|
| SQL Server business records | Soft delete, anonymization, field purge, cryptographic erasure, or physical purge where policy permits | Audit/tombstone remains minimal and tenant-scoped |
| SQL Server audit records | Retain immutable audit until retention expiry; purge only by governed archival/deletion workflow | Audit cannot be silently edited |
| Azure Blob source documents | Delete, archive, legal hold, immutable retention, or version cleanup according to policy | Object metadata links to policy and deletion evidence |
| Qdrant vectors | Delete points/collections or rebuild alias without expired chunks | Vectors are derived data; source metadata remains authoritative |
| Redis memory/cache | TTL, namespace rotation, targeted invalidation, or purge | Cache/memory loss is safe and expected |
| Events/outbox | Retain minimal event metadata; purge payloads by event retention policy | Raw sensitive payloads are prohibited by event design |
| Telemetry | Retain redacted metrics/logs/traces by operational policy | Telemetry is not the audit ledger |
| Backups | Expire backup sets by schedule; do not surgically edit immutable backups | Restore-time tombstone reconciliation is mandatory |
| Provider residual state | Delete through provider contract/API where supported; otherwise record residual limitation | Provider activation requires deletion terms |

## 7. Preserve minimal tombstones after deletion

Deletion must not allow data to reappear after restore, event replay, cache rebuild, vector
rebuild, or provider synchronization.

Tombstones contain only:

- TenantId.
- Entity/data subject reference or irreversible hash.
- Data category.
- Deletion decision ID.
- Deletion effective date.
- Legal basis or request type.
- Scope/version.
- Retain-until date for tombstone itself.

Tombstones cannot contain original personal data, source content, prompts, responses, or
business record values unless legally required and approved.

## 8. Reconcile restores and replays

Any restore from SQL, blob, Qdrant snapshot, Redis persistence, event replay, or external
provider export must run deletion and legal-hold reconciliation before returned data becomes
available to AI, reporting, search, or users.

Restore reconciliation checks:

- Tenant catalog and RLS status.
- Legal holds.
- Deletion tombstones.
- Superseded source documents.
- Source and vector manifests.
- AI memory/cache invalidation.
- Provider residual-state status.
- Audit and cost ledger continuity.

Restored data that is expired or deleted must remain inaccessible and be purged again.

## 9. Govern tenant offboarding

Tenant offboarding is a workflow, not a script.

Minimum stages:

1. Confirm authority, contract termination, export obligations, and legal holds.
2. Freeze or limit new processing.
3. Export tenant data where contract/legal policy allows.
4. Disable tenant access and integrations.
5. Remove or archive active business data according to retention policy.
6. Delete derived AI stores: Qdrant, Redis memory/cache, summaries, provider residual state.
7. Rotate or revoke tenant secrets, API keys, webhooks, and provider credentials.
8. Tombstone tenant identifiers to prevent restore/replay reactivation.
9. Reconcile backups and restore tests.
10. Produce an offboarding completion certificate.

## 10. Apply AI-specific deletion rules

AI derived stores must follow ADR-032, ADR-035, SEC-AI-001, and AI-OPS-001.

Rules:

- Conversation session memory expires by Redis TTL and can be reset on request.
- Conversation summaries are deleted, anonymized, or crypto-erased by memory policy and
  data-subject request outcome.
- Semantic/exact/retrieval/embedding cache entries are disposable and must be invalidated
  on deletion, role/permission changes, source changes, legal hold, or incident.
- Qdrant vectors are deleted or made unreachable when source documents expire, are
  superseded, or are deleted.
- AI audit metadata remains for lawful audit retention but must avoid raw prompt/response
  storage by default.
- Provider-side residual data deletion must be requested and tracked under provider terms.
- AI cannot answer from deleted, expired, held, or restored-but-unreconciled sources.

## 11. Define governance tables in a future DB design

The future database design must include governance entities similar to:

```text
Governance.DataInventory
Governance.RetentionPolicy
Governance.RetentionRule
Governance.LegalHold
Governance.LegalHoldScope
Governance.DataSubjectRequest
Governance.DeletionRequest
Governance.DeletionJob
Governance.DeletionJobItem
Governance.DeletionTombstone
Governance.ArchivalPackage
Governance.RestoreReconciliation
Governance.ProviderResidualState
```

Every tenant-scoped table follows database standards: `TenantId`, audit columns,
`IsDeleted`, `VersionNumber`, RLS, and indexes on `TenantId`, status, category, and due
dates. Sensitive fields require encryption or irreversible hashing where appropriate.

## 12. Use event-driven invalidation and evidence

Retention and deletion publish versioned events through ADR-009:

- `RetentionPolicyChanged`
- `LegalHoldApplied`
- `LegalHoldReleased`
- `DataSubjectRequestReceived`
- `DeletionRequested`
- `DeletionCompleted`
- `DeletionFailed`
- `TombstoneCreated`
- `ArchiveCreated`
- `TenantOffboardingStarted`
- `TenantOffboardingCompleted`
- `RestoreReconciliationRequired`
- `RestoreReconciliationCompleted`
- `ProviderResidualDeletionRequested`
- `ProviderResidualDeletionCompleted`

Events contain identifiers, versions, status, and evidence references only. They do not
carry raw personal data, document text, prompts, responses, or secrets.

## 13. Require OpenAPI-documented operations

Administrative and tenant-facing retention operations must be versioned and documented in
OpenAPI before implementation.

Required capabilities:

- Retention policy read/preview.
- Legal hold create/release/review.
- Data-subject request intake/status.
- Deletion request preview/submit/approve/status.
- Tenant offboarding status.
- Restore reconciliation status.
- Provider residual-state status.
- Evidence/certificate retrieval.

Destructive operations require RBAC, ABAC, reason, approval reference, idempotency key,
optimistic concurrency, dry-run/preview where possible, audit, and rate limiting.

## 14. Produce deletion and archival evidence

Every retention, archive, hold, deletion, purge, and offboarding workflow produces evidence:

- Policy version used.
- Scope and excluded records.
- Legal hold checks.
- Systems touched.
- Job item status.
- Failed/retried items.
- Provider residual-state results.
- Backup restore reconciliation requirement.
- Completion certificate.

Evidence is tenant-scoped and retained under a separate governance retention policy.

---

# Alternatives Considered

## Soft delete only

Rejected. Soft delete preserves business integrity but does not satisfy erasure, tenant
offboarding, AI derived-store removal, provider residual-state tracking, or restore-time
reconciliation.

## Immediate physical delete everywhere

Rejected. HR/payroll records often have statutory retention, audit, legal hold, and payroll
reconciliation requirements. Immediate deletion could violate law or destroy evidence.

## Per-module retention logic

Rejected. It would create inconsistent policy, duplicate jobs, missing AI/cache/vector
cleanup, and hardcoded legal rules.

## Backup surgery for every deletion request

Rejected. Immutable and point-in-time backups are not edited per request. The platform uses
backup expiry plus tombstone reconciliation after restore.

---

# Consequences

Positive:

- Provides one governance model for retention, deletion, legal hold, AI derived stores, and
  tenant offboarding.
- Preserves auditability while supporting privacy rights and statutory retention.
- Prevents deleted data from reappearing after restore or event replay.
- Keeps legal retention rules configurable and jurisdiction-aware.
- Supports future modules without changing core deletion logic.

Costs:

- Requires governance DB design, background jobs, OpenAPI, evidence workflows, and tests.
- Requires legal review for retention templates.
- Requires operational discipline for backups, provider residual state, and restore
  reconciliation.

Risks:

- Incorrect policy configuration can over-retain or over-delete data.
- Provider residual-state guarantees may vary by provider.
- Legacy restored data can reappear if reconciliation is skipped.
- Tenant administrators may misunderstand the difference between soft delete, erasure, and
  legal hold.

---

# Impact

Architecture:

- Adds a platform governance capability used by every module.
- Requires event-driven deletion and invalidation.
- Requires restore reconciliation as part of DR.

Database:

- Requires governance schema tables and RLS.
- Requires tombstones, deletion job tracking, archival package metadata, and legal hold
  scope tables.
- Requires indexes for due retention jobs and request status.

Security:

- Strengthens DPDP/GDPR readiness and tenant offboarding.
- Requires least-privilege destructive APIs and immutable evidence.
- Requires provider deletion tracking.

Operations:

- Requires scheduled retention scans, deletion workers, reconciliation jobs, and evidence
  dashboards.
- Requires backup expiry and restore testing.

Development:

- No module may implement private deletion logic outside this framework.
- New modules register data categories and retention hooks through configuration and events.

---

# Acceptance Criteria

| ID | Criterion |
|---|---|
| ADR022-AC-001 | Retention policies are effective-dated, tenant/jurisdiction/data-category scoped, approved, audited, and stored as configuration data. |
| ADR022-AC-002 | Legal hold blocks purge/anonymization/crypto-erasure for scoped data until released, without granting broader read access. |
| ADR022-AC-003 | Soft delete, archive, legal hold, purge, anonymization, cryptographic erasure, and tombstone states are distinct and auditable. |
| ADR022-AC-004 | Tenant isolation and RLS apply to retention, hold, deletion, offboarding, archival, and restore-reconciliation tables and jobs. |
| ADR022-AC-005 | Deletion workflows reconcile SQL Server, Azure Blob, Qdrant, Redis, events, telemetry, audit, backups, and provider residual state. |
| ADR022-AC-006 | Deleted data cannot reappear after backup restore, Qdrant restore, Redis restore, event replay, index rebuild, or provider synchronization. |
| ADR022-AC-007 | Minimal tombstones exist for deleted records and contain no unnecessary personal/business data. |
| ADR022-AC-008 | AI memory, cache, summaries, vectors, and provider residual state are deleted or invalidated according to approved policy. |
| ADR022-AC-009 | Tenant offboarding has an approved, evidence-producing workflow with export, disablement, deletion, credential revocation, derived-store cleanup, and tombstoning. |
| ADR022-AC-010 | Backup expiry and restore reconciliation are documented and tested; immutable backups are not surgically edited per deletion request. |
| ADR022-AC-011 | Administrative retention/deletion/legal-hold APIs are versioned, OpenAPI-documented, RBAC/ABAC protected, idempotent, audited, and support preview where meaningful. |
| ADR022-AC-012 | Provider activation requires documented data retention, deletion, legal hold, residual-state, and breach-notification behavior. |
| ADR022-AC-013 | Retention jobs and deletion jobs are idempotent, retryable, observable, and produce tenant-scoped completion evidence. |
| ADR022-AC-014 | Every new module registers data categories, lawful purpose, retention class, archival behavior, deletion hooks, and legal-hold support before implementation. |
| ADR022-AC-015 | Unit coverage is at least 85%, with integration, restore-reconciliation, tenant-isolation, legal-hold, provider, AI-derived-store, and end-to-end deletion tests. |

---

# Official and Primary References

- Digital Personal Data Protection Act, 2023:
  `https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf`
- GDPR Regulation 2016/679:
  `https://eur-lex.europa.eu/eli/reg/2016/679/oj`
- NIST Privacy Framework:
  `https://www.nist.gov/privacy-framework`
- NIST SP 800-88 Rev. 2, Guidelines for Media Sanitization:
  `https://csrc.nist.gov/pubs/sp/800/88/r2/final`
- Microsoft SQL Server backup and restore:
  `https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases?view=sql-server-ver17`
- Azure Blob immutable storage:
  `https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview`
- Qdrant snapshots:
  `https://qdrant.tech/documentation/concepts/snapshots/`
- Redis persistence:
  `https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/`

References last validated: 2026-06-27.

---

# Approval

Data Governance/Privacy Architect: Drafted by Codex 2026-06-27  
Security Architect: ____  
Database Architect: ____  
Platform/Operations Architect: ____  
Legal/Compliance: ____  
Product Owner: Approved by Bhajan Lal 2026-06-27

(Status: Approved - owner approved 2026-06-27)
