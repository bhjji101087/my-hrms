# AI-DR-001 - AI Disaster Recovery Design and Exercise Plan

Version: 1.0
Date: 2026-06-27
Status: Approved
Owner: Platform/Operations Architect
Reviewers: Security, Data Governance/Privacy, Database Architecture, Solution Architecture, Product/AI

Related approved documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md`
- `docs/15-ai/AI-OPS-001-enterprise-ai-operations.md`
- `docs/12-security/SEC-AI-001-ai-security-extension.md`
- `docs/16-decisions/ADR-009-event-driven-backbone.md`
- `docs/16-decisions/ADR-019-ai-rag-architecture.md`
- `docs/16-decisions/ADR-030-vector-store-strategy.md`
- `docs/16-decisions/ADR-031-ai-observability-telemetry.md`
- `docs/16-decisions/ADR-032-conversation-memory-strategy.md`
- `docs/16-decisions/ADR-033-ai-cost-governance.md`
- `docs/16-decisions/ADR-034-rag-evaluation-framework.md`
- `docs/16-decisions/ADR-035-semantic-cache-architecture.md`
- `docs/16-decisions/ADR-022-data-retention-archival-legal-hold-deletion.md` - Draft companion

---

# 1. Purpose

This document defines disaster recovery design, recovery order, validation, and exercise
requirements for the HRMS AI platform. It covers AI gateway/orchestration, provider
configuration, SQL Server AI data, source documents, Qdrant vectors, Redis memory/cache,
events/outbox, telemetry, cost ledger, evaluation evidence, and retention/deletion
reconciliation.

AI disaster recovery must restore safe service, not merely restart infrastructure. Recovery
is successful only when tenant isolation, RBAC/ABAC, source integrity, deletion tombstones,
legal holds, citations, quality gates, cost controls, and audit continuity are validated.

---

# 2. Scope

Covered:

- AI gateway/orchestrator and policy enforcement.
- SQL Server AI schemas and governance metadata.
- Source documents and manifests in object storage.
- Qdrant vector collections, snapshots, aliases, and deterministic rebuild.
- Redis session memory, semantic/retrieval caches, and namespace rotation.
- Event/outbox, queues, invalidation, deletion, and replay.
- Provider adapter registry, model/prompt/index/cache/memory/evaluation bundle versions.
- Observability stack and incident evidence.
- AI retention/deletion/legal-hold reconciliation.
- DR exercises and acceptance criteria.

Not covered:

- Full HRMS platform DR outside AI dependencies.
- Provider-owned disaster recovery beyond approved provider contracts and adapter failover.
- Autonomous AI agents.

---

# 3. DR Principles

1. Core HRMS remains available when AI is unavailable.
2. Safety and tenant isolation override speed of recovery.
3. AI degraded mode is preferable to unsafe AI availability.
4. Derived stores are rebuildable from canonical sources and approved configuration.
5. Redis memory/cache loss is acceptable; stale or unauthorized reuse is not.
6. Qdrant snapshots are useful but deterministic rebuild from source is the required fallback.
7. Backup restore must be followed by ADR-022 deletion/legal-hold/tombstone reconciliation.
8. DR cannot silently activate paid managed services or new providers.
9. Recovery evidence must be immutable, tenant-safe, and linked to incident/change records.
10. DR exercises are release gates for production AI.

---

# 4. Recovery Classification

| Scenario | Expected mode | User-facing behavior |
|---|---|---|
| LLM provider outage | Provider fallback or retrieval-only/unavailable | Explain temporary AI unavailability; core HRMS unaffected |
| Embedding provider outage | Pause ingestion; existing retrieval may continue where safe | New knowledge may be delayed |
| Qdrant outage | Retrieval unavailable or approved source navigation fallback | AI refuses grounded answer if evidence cannot be retrieved |
| Redis outage | Stateless AI turn and cache miss | Conversation continuity reduced; no unsafe fallback |
| SQL AI schema outage | AI fails closed for config/audit/cost/policy | AI unavailable; core HRMS status depends on platform SQL |
| Object storage outage | Pause ingestion/evaluation; existing approved index may continue if safe | New document ingestion delayed |
| Event/outbox backlog | Durable backlog, bounded replay, disable stale cache/memory if needed | AI may run with conservative invalidation |
| Telemetry outage | AI may continue if durable audit works | Operations alerted; no sensitive debug mode |
| Security incident | Scoped disablement, evidence preservation | AI path disabled or limited |
| Regional/dependency disaster | Restore/rebuild in dependency order | AI unavailable until validation passes |

---

# 5. Initial Recovery Objectives

These are initial platform objectives. Tenant contracts may define stricter values only
after architecture, cost, and test evidence support them.

| Capability | RTO | RPO | Recovery note |
|---|---:|---:|---|
| Core HRMS without AI | Outside this document | Outside this document | AI outage must not block core HRMS |
| AI gateway service | 4 hours | 15 minutes for config/audit metadata | Must fail closed if policy/config unavailable |
| SQL Server AI config/audit/cost/evaluation metadata | 4 hours | 15 minutes | Restore plus RLS/deletion reconciliation |
| Object storage source documents/manifests | 8 hours | 15 minutes | Required for rebuild and source integrity |
| Qdrant vector retrieval | 8 hours | 24 hours | Snapshot restore or deterministic rebuild |
| Redis session memory | No restore target | 0 retained-memory expectation | Stateless fallback; sessions may reset |
| Redis semantic/retrieval cache | No restore target | 0 retained-cache expectation | Safe miss; namespace rotation allowed |
| Event/outbox processing | 4 hours | 15 minutes | Replay idempotently after validation |
| Provider fallback | 1 hour where approved | N/A | No automatic paid provider activation |
| Observability stack | 8 hours | Best effort for sampled telemetry | Durable audit is separate |
| Deletion/legal-hold reconciliation | Before AI reactivation | No missed tombstones accepted | Blocks affected AI data availability |

---

# 6. Canonical Sources and Derived Stores

| Store | Role | DR strategy |
|---|---|---|
| SQL Server AI metadata | System of record for policies, manifests, audit, cost, evaluation, memory summaries | Back up, restore, RLS validate, reconcile tombstones |
| Azure Blob source documents | System of record for approved knowledge source files and artifacts | Redundancy, versioning/retention where approved, restore, malware/hash validation |
| Qdrant | Derived vector retrieval index | Restore snapshot when safe; otherwise rebuild from source/manifests |
| Redis memory/cache | Ephemeral derived continuity/cache | Prefer safe loss; failover where configured; purge/rotate after incident |
| Event/outbox and broker | Durable coordination and invalidation | Restore/replay idempotently; dead-letter reconciliation |
| Provider systems | External inference dependency | Failover through approved adapter only; validate provider residual data |
| Telemetry stack | Operational visibility | Restore dashboards/alerts; durable audit remains authoritative |

Qdrant and Redis are never the system of record. A successful DR plan must prove the AI
platform works correctly after losing either store.

---

# 7. Backup and Protection Strategy

## 7.1 SQL Server

Required:

- Full, differential, and transaction-log backup strategy appropriate to the selected
  deployment model.
- Point-in-time restore capability where supported.
- Separate production/non-production backup storage and keys.
- Backup encryption.
- Regular restore tests into isolated environment.
- Post-restore RLS, tenant catalog, legal hold, tombstone, and audit validation.

## 7.2 Azure Blob source artifacts

Required:

- Versioned source manifests with content hashes.
- Storage redundancy aligned to tenant/residency policy.
- Immutable retention or legal hold where approved for records requiring preservation.
- Malware scan status preserved with artifact metadata.
- Restore validation against SQL manifests.

## 7.3 Qdrant

Required:

- Snapshot schedule and retention for production collections where approved.
- Snapshot encryption and access control.
- Restore tests for collection/alias placement.
- Deterministic rebuild from SQL metadata and source documents.
- Tenant partition, payload filter, effective-date, permission, and citation validation
  before alias activation.

## 7.4 Redis

Required:

- Redis Sentinel or Cluster failover only where approved by deployment profile.
- Persistence disabled for sensitive ephemeral stores unless approved and deletion-tested.
- If persistence is enabled, backup retention, encryption, ACL, and deletion behavior must
  be documented.
- Cache and memory namespaces can be rotated during DR.
- Loss of Redis must degrade to stateless turn and cache miss.

## 7.5 Events and queues

Required:

- Durable outbox in SQL Server.
- Idempotent consumers.
- Dead-letter queues with owner and replay policy.
- Replay order and stop conditions.
- Reconciliation for invalidation, deletion, cost, and evaluation events.

## 7.6 Secrets and provider configuration

Required:

- Secrets are backed by approved secret-management recovery controls.
- Restored environments cannot accidentally use production secrets outside production.
- Provider keys can be revoked and rotated during recovery.
- Provider fallback uses only pre-approved configuration and budget policy.

---

# 8. Recovery Order

Standard regional/dependency recovery order:

1. Declare incident and freeze risky AI changes.
2. Preserve evidence and establish incident command.
3. Restore identity, tenant catalog, and platform authorization prerequisites.
4. Restore SQL Server AI metadata and governance records.
5. Restore object storage source artifacts and manifests.
6. Restore event/outbox and broker processing in paused or controlled mode.
7. Run ADR-022 legal-hold/deletion/tombstone reconciliation.
8. Restore or rebuild Qdrant vector indexes in shadow placement.
9. Validate Qdrant tenant partitioning, metadata filters, citations, freshness, and quality.
10. Restore Redis only where safe; otherwise rotate namespaces and run stateless/cache-miss.
11. Validate provider registry, credentials, budget reservation, and fallback policy.
12. Restore observability dashboards/alerts and durable audit routes.
13. Run AI security, isolation, evaluation, and smoke tests.
14. Activate AI in scoped canary or degraded mode.
15. Expand only after evidence confirms RTO/RPO and safety objectives.

---

# 9. Restore Validation Gates

AI service cannot return to normal production until these pass:

- Tenant catalog and RLS validation.
- Cross-tenant negative retrieval tests.
- RBAC/ABAC and field-masking tests.
- Legal hold and deletion tombstone reconciliation.
- Source manifest and content-hash validation.
- Qdrant collection/alias/index-version validation.
- Redis memory/cache namespace and stale-entry checks.
- Event/outbox replay reconciliation.
- Prompt/model/provider/index/cache/memory/evaluation bundle compatibility.
- Citation, groundedness, refusal, and confidence smoke tests.
- Cost ledger and budget reservation validation.
- Security telemetry and incident alert validation.
- Degraded-mode and rollback validation.

Any failed tenant isolation, legal hold, deletion, provider credential, or security test
blocks normal AI reactivation.

---

# 10. Degraded-Mode Playbook

| Dependency failure | Degraded behavior |
|---|---|
| LLM unavailable | Retrieval-only or AI unavailable; no ungrounded answer |
| Embedding unavailable | Existing approved index may serve; new ingestion paused |
| Reranker unavailable | Use evaluated no-rerank profile only |
| Qdrant unavailable | No knowledge answer unless approved source navigation fallback exists |
| Redis unavailable | Stateless turn, cache miss, no memory continuity |
| SQL AI metadata unavailable | AI unavailable because policy/config/audit cannot be trusted |
| Blob source unavailable | Pause ingestion/evaluation; existing index may continue if source status can be trusted |
| Event backlog | Conservative invalidation, pause promotions, reconcile before normal mode |
| Telemetry outage | AI may continue only if durable audit/security controls work |

Degraded mode must be visible in tenant-safe status APIs and dashboards.

---

# 11. Exercise Program

DR exercises are mandatory before production and at approved cadence.

| Exercise | Minimum cadence | Evidence required |
|---|---|---|
| Tabletop regional AI outage | Quarterly during active development, semiannual after stable production | Participants, decisions, gaps, action owners |
| SQL AI metadata point-in-time restore | Quarterly before production, then semiannual | RPO/RTO, RLS, audit, cost, policy validation |
| Qdrant snapshot restore | Quarterly before production, then semiannual | Snapshot integrity, tenant partition, alias, retrieval validation |
| Qdrant deterministic rebuild | Semiannual | Source manifest, embedding/index version, rebuild time, quality result |
| Redis failover and namespace rotation | Quarterly before production, then semiannual | Stateless fallback, cache/memory invalidation evidence |
| Provider outage/fallback drill | Quarterly | Approved fallback only, cost/budget validation |
| Event/outbox replay drill | Quarterly | Idempotency, dead-letter, invalidation/deletion replay evidence |
| Deletion reappearance test after restore | Semiannual and after retention design changes | Tombstones prevent AI/search/report reappearance |
| Security incident recovery drill | Semiannual | Evidence preservation, disablement, key rotation, safe re-entry |
| Full AI ORR recovery exercise | Before production and annually | End-to-end recovery, validation gates, final approval |

Exercises create tracked findings with owner, severity, due date, and retest result.
Repeated failed exercises block production expansion.

---

# 12. Exercise Scenarios

Required scenario library:

1. Qdrant collection corruption with prior snapshot available.
2. Qdrant total loss requiring deterministic rebuild.
3. Redis cache poisoning and namespace rotation.
4. Redis outage with stateless AI fallback.
5. SQL AI metadata restore to point in time.
6. Restored deleted source document tries to reappear in AI answer.
7. Tenant offboarding interrupted halfway.
8. Provider outage and fallback provider unavailable due budget policy.
9. Prompt/model rollback after hallucination/security regression.
10. Event/outbox backlog delays permission invalidation.
11. Blob source storage unavailable during ingestion.
12. Provider secret compromise during DR.
13. Telemetry backend outage during active AI incident.
14. Regional dependency outage.

---

# 13. DR Evidence Manifest

Every DR event or exercise produces an evidence manifest:

- Incident/exercise ID.
- Scope and affected tenants/use cases.
- Declared start/end time.
- RTO/RPO targets and actuals.
- Backup/snapshot/source versions used.
- Bundle versions restored.
- Legal hold/deletion reconciliation result.
- Tenant isolation and RBAC/ABAC test results.
- Qdrant/Redis/event/provider validation results.
- Evaluation/security smoke-test results.
- Open findings, accepted risks, and approval to re-enter service.
- Tenant communication timeline where applicable.

Evidence is tenant-safe, access-controlled, immutable, and linked to audit records.

---

# 14. Roles and Approval

| Role | DR responsibility |
|---|---|
| Incident Commander | Declares DR event, coordinates roles, approves recovery progression |
| Platform/Operations | Restores infrastructure, Qdrant, Redis, event/broker, telemetry |
| Database Architect/DBA | Restores SQL Server, validates RLS, point-in-time state, backup integrity |
| Security | Evidence protection, isolation validation, credential rotation, security clearance |
| Data Governance/Privacy | Legal hold, deletion, tombstone, offboarding, provider residual-state validation |
| Product/AI Owner | Degraded-mode decision, tenant communication, canary/expansion decision |
| Domain Owner | HR/payroll/policy correctness validation |
| Finance/FinOps | Provider/budget/cost ledger validation |

Normal production reactivation requires Incident Commander, Security, Operations, Data
Governance, and Product/AI approval. SEV-0 security incidents require Security clearance.

---

# 15. OpenAPI and Automation Requirements

Phase 6D API/OpenAPI must document DR and operational endpoints for:

- AI component health and degraded mode.
- DR event/exercise status.
- Backup/snapshot/rebuild job status.
- Qdrant index restore/rebuild/alias promotion status.
- Redis namespace rotation and cache/memory disablement status.
- Event/outbox replay status.
- Deletion/legal-hold restore reconciliation status.
- Provider fallback/disablement status.
- DR evidence manifest retrieval.

All endpoints require RBAC, ABAC, tenant scoping, reason, correlation ID, idempotency where
needed, audit, rate limiting, and no exposure of raw prompts, responses, vectors, cache
entries, secrets, or other tenants' data.

---

# 16. Residual Risks

| Risk | Status | Mitigation |
|---|---|---|
| Qdrant rebuild may exceed initial RTO for large tenants | Open | Snapshot plus rebuild strategy, tenant tier capacity planning |
| Provider outage may affect all fallback models | Open | Retrieval-only/unavailable degraded mode; no unsafe fallback |
| Redis persistence can reintroduce stale memory/cache | Controlled | Prefer no persistence for ephemeral data; namespace rotation and deletion tests |
| Backup restore can reintroduce deleted data | Controlled | ADR-022 tombstones and restore reconciliation before AI activation |
| Telemetry outage can reduce visibility during DR | Controlled | Durable audit independent of telemetry; local health alerts |
| Legal hold and deletion conflict can delay recovery | Accepted | Data Governance approval required before affected AI availability |

---

# 17. Acceptance Criteria

| ID | Criterion |
|---|---|
| AIDR-AC-001 | AI DR distinguishes canonical stores from derived stores and proves AI works safely after Qdrant or Redis loss. |
| AIDR-AC-002 | RTO/RPO targets exist for AI gateway, SQL AI metadata, object storage, Qdrant, Redis, events, providers, telemetry, and deletion reconciliation. |
| AIDR-AC-003 | SQL AI restore validates RLS, tenant catalog, audit, cost, policy, legal hold, and deletion tombstones before AI use. |
| AIDR-AC-004 | Qdrant recovery supports snapshot restore and deterministic rebuild from SQL metadata and source artifacts. |
| AIDR-AC-005 | Qdrant restored/rebuilt indexes pass tenant partition, permission, effective-date, citation, quality, and rollback tests before alias activation. |
| AIDR-AC-006 | Redis outage degrades to stateless turn/cache miss and never releases stale or unauthorized memory/cache content. |
| AIDR-AC-007 | Event/outbox replay is idempotent and reconciles invalidation, deletion, cost, and evaluation events. |
| AIDR-AC-008 | Provider fallback uses only pre-approved adapters, credentials, residency, budget, and evaluation policy. |
| AIDR-AC-009 | DR cannot automatically activate paid services, broader data scope, stale source content, or unapproved providers. |
| AIDR-AC-010 | Restore-time ADR-022 legal-hold/deletion/tombstone reconciliation blocks data reappearance after restore or replay. |
| AIDR-AC-011 | DR validation includes cross-tenant negative tests, RBAC/ABAC tests, citation tests, prompt/model/index compatibility, and security smoke tests. |
| AIDR-AC-012 | DR exercises include Qdrant restore/rebuild, Redis failover/rotation, SQL restore, event replay, provider outage, deletion reappearance, and security incident scenarios. |
| AIDR-AC-013 | Every DR event/exercise produces immutable, tenant-safe evidence with RTO/RPO actuals, validation results, findings, and re-entry approval. |
| AIDR-AC-014 | DR and operational APIs are versioned, OpenAPI-documented, RBAC/ABAC protected, idempotent where needed, audited, and redacted. |
| AIDR-AC-015 | Unit coverage is at least 85%, with integration, restore, replay, failover, deletion reconciliation, tenant isolation, security, and end-to-end DR tests. |

---

# 18. Official and Primary References

- NIST SP 800-34 Rev. 1, Contingency Planning Guide:
  `https://csrc.nist.gov/pubs/sp/800/34/r1/final`
- NIST SP 800-61 Rev. 3, Incident Response:
  `https://csrc.nist.gov/pubs/sp/800/61/r3/final`
- Microsoft SQL Server backup and restore:
  `https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases?view=sql-server-ver17`
- Azure Storage redundancy:
  `https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy`
- Azure Blob immutable storage:
  `https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview`
- Qdrant snapshots:
  `https://qdrant.tech/documentation/concepts/snapshots/`
- Redis persistence:
  `https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/`
- Redis Sentinel:
  `https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/`
- RabbitMQ reliability:
  `https://www.rabbitmq.com/docs/reliability`

References last validated: 2026-06-27.

---

# Approval

Platform/Operations Architect: Drafted by Codex 2026-06-27  
Security Architect: ____  
Data Governance/Privacy: ____  
Database Architect: ____  
Solution Architect: ____  
Product/AI Owner: ____  
Product Owner: Approved by Bhajan Lal 2026-06-27

(Status: Approved - owner approved 2026-06-27)
