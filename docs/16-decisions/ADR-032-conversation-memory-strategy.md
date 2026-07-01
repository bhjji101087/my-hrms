# ADR-032 - Conversation Memory Strategy

Architecture Decision Record

Date: 2026-06-23
Last Updated: 2026-06-24
Status: Approved
Approved By: Bhajan Lal (Product Owner)
Approved Date: 2026-06-24

Related documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md` - Approved v2.1
- ADR-005 Multi-Tenancy Model - Approved
- ADR-006 Tenant Context and Data Access - Approved
- ADR-008 Identity and Access Management - Approved
- ADR-009 Event-Driven Backbone - Approved
- ADR-019 Enterprise AI/RAG Platform Architecture - Approved
- ADR-027 Provider-Abstraction Framework - Approved
- ADR-030 Enterprise Vector Store Strategy - Approved
- ADR-031 AI Observability and Telemetry - Approved

---

# Context

The HR Copilot must support natural multi-turn conversations such as:

- A user asks a policy question and then asks a follow-up without repeating the policy.
- A manager narrows an employee lookup over several turns.
- An administrator drafts a report or workflow through iterative refinement.

Without controlled memory, each turn loses useful context. With uncontrolled memory, the
platform may retain sensitive HR content, reuse information after permissions change,
create hidden employee profiles, accept malicious instructions from prior turns, exceed
model context limits, or expose one tenant/user's conversation to another.

Conversation memory must therefore provide continuity while preserving:

- Tenant isolation and current RBAC plus ABAC authorization.
- Purpose limitation, data minimization, retention, deletion, and DPDP obligations.
- Prompt-injection and memory-poisoning defenses.
- Provider independence and no vendor-hosted hidden conversation state.
- Bounded context windows, predictable token cost, and degraded stateless operation.
- Auditability without making telemetry or audit logs a transcript store.

---

# Decision

## 1. Use four explicit memory tiers

| Tier | Purpose | Storage | Default |
|---|---|---|---|
| Turn context | Current request, authorized retrieval, and tool results | Process memory | Required; destroyed after response |
| Session memory | Recent user/assistant turns for immediate continuity | Redis through `ICacheProvider` | Enabled with short idle and absolute TTL |
| Conversation summary | Compact, provenance-aware continuity across sessions | SQL Server `AI` schema | Disabled until tenant policy enables it |
| Long-term personal memory | Preferences or inferred user profile | None | Prohibited by default; separate consent/ADR required |

Memory tiers are independent. Enabling session memory does not automatically enable
durable summaries or transcript retention.

Persistent report drafts, workflow drafts, policies, forms, and configuration work are not
a fifth conversation-memory tier. They belong to a separate future **Workspace Memory**
capability defined in section 18 and require their own ADR before implementation.

## 2. Make SessionOnly the platform default

The default tenant memory policy is `SessionOnly`:

- Turn context is destroyed after the response completes.
- Recent turns are kept in Redis with a configurable idle TTL and absolute maximum lifetime.
- Initial recommended values are 30 minutes idle and 24 hours absolute; they are policy
  configuration, not hardcoded feature rules.
- Durable summaries and full transcripts are off.
- Long-term personal memory is off.

Tenant administrators with `AI.ManageMemory` may select an approved policy mode:

- `Disabled` - each request is stateless.
- `SessionOnly` - short-lived recent turns only.
- `SessionAndSummary` - short-lived turns plus controlled SQL summary.

Platform security policy defines maximum retention. A tenant may choose a shorter period,
but cannot exceed the platform maximum or disable mandatory security/audit metadata.

### 2.1 Enforce conversation purpose boundaries

Every conversation has an immutable `PurposeKey` selected from a tenant-approved purpose
catalog, for example `PolicySupport`, `PayrollSupport`, `EmployeeLookup`, `ReportDrafting`,
or `WorkflowDrafting`. Purpose configuration defines allowed data classifications, source
types, read tools, roles/ABAC scopes, and memory policy.

Memory can be reused only when the current request remains compatible with the declared
purpose. A significant purpose change triggers:

1. Reauthorization against the target purpose.
2. Removal of context that is not permitted for the target purpose.
3. Session reset when safe reduction cannot be proven.
4. A new conversation when the target purpose has different sensitive-data, tool, domain,
   or authorization boundaries.

For example, follow-up payroll questions may remain in `PayrollSupport`, while changing
from payroll support to an employee performance review normally starts a new conversation.
The user is told when a new conversation or reset is required. Purpose cannot be changed
silently by the model or inferred solely from conversation text.

## 3. Keep model-provider calls stateless

The platform does not depend on provider-hosted conversation threads, assistants, or hidden
memory. Each model request receives only the context assembled and authorized by the HRMS
for that turn.

Provider conversation/thread identifiers are not the system of record. If a provider
requires a temporary request identifier, it is treated as an adapter detail, expires with
the request/session, and cannot be used to recover unreviewed provider-side memory.

This keeps Claude/OpenAI/Gemini switching possible through `ILlmProvider` without losing
the platform's privacy, authorization, or deletion controls.

## 4. Store short-term session memory in Redis

Short-term memory is the session-memory tier. It uses `ICacheProvider`, with Redis as the
approved first distributed cache.
Keys are created only by a centralized server-side key builder and include trusted tenant,
user, and conversation scope. Client-supplied key fragments are never used directly.

Conceptual key:

`ai:{TenantId}:{UserId}:{ConversationId}:{SecurityContextVersion}`

Each entry contains only:

- Normalized user turn needed for continuity.
- Assistant response summary, not hidden chain-of-thought.
- Citation/source references and confidence band where relevant.
- Prompt/model/index versions.
- Created, last-accessed, idle-expiry, and absolute-expiry times.
- Security-context version and sensitivity classification.

Raw tool payloads, retrieved source chunks, vectors, secrets, authentication tokens,
passwords, provider credentials, hidden reasoning, and unnecessary HR fields are not stored.

Redis controls:

- TLS and authentication outside local development.
- Tenant/user/conversation namespace validation on every operation.
- Size and turn-count limits per conversation.
- Atomic expiry refresh bounded by the absolute maximum.
- Encryption at rest where persistence is enabled.
- No production persistence unless approved backup/deletion behavior is defined.
- Regulated or high-risk tenants may use a dedicated cache placement by configuration.

## 5. Store only policy-enabled summaries in SQL Server

When `SessionAndSummary` is enabled, SQL Server stores a compact conversation summary and
metadata in the `AI` schema. It does not store a full transcript by default.

Required entities:

```text
AI.Conversation
  ConversationId, TenantId, UserId, PurposeKey, PurposeVersion, PurposeScopeJson,
  MemoryMode, ContextGeneration, Status,
  SecurityContextVersion, Sensitivity, LastActivityDate, ExpiresDate,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate, IsDeleted, VersionNumber

AI.ConversationSummary
  ConversationSummaryId, TenantId, ConversationId, SummaryVersion,
  SummarySourceTurnStart, SummarySourceTurnEnd,
  EncryptedSummary, SourceReferencesJson, PermissionTagsJson,
  PromptVersion, ModelRegistryVersion, ConfidenceBand,
  SummaryQualityScore, SummaryQualityEvaluationVersion,
  EffectiveFrom, EffectiveTo, ExpiresDate,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate, IsDeleted, VersionNumber

AI.MemoryPolicy
  MemoryPolicyId, TenantId, Mode, IdleTtlMinutes, AbsoluteTtlMinutes,
  SummaryRetentionDays, MaxTurns, MaxContextTokens, SummaryTriggerJson,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate, IsDeleted, VersionNumber

AI.MemoryDeletionRequest
  MemoryDeletionRequestId, TenantId, UserId, ConversationId, Scope,
  Status, RequestedDate, CompletedDate, LegalHoldReference,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate, IsDeleted, VersionNumber
```

Every tenant table has SQL Server RLS using ADR-006 session context. Summary content is
application-level encrypted in addition to database-at-rest controls. Indexes include
`(TenantId, UserId, Status)` and `(TenantId, ConversationId, SummaryVersion)`.

Conversation memory is derived/ephemeral data, not a business system of record. Rows use
soft deletion for workflow/audit consistency and are then purged or cryptographically
erased under approved retention/DPDP rules. This does not authorize physical deletion of
core HR business records.

## 6. Do not store conversation memory in Qdrant

Conversation turns, summaries, and inferred personal preferences are not embedded or
indexed in Qdrant by default.

Qdrant remains limited to approved tenant knowledge sources under ADR-030. This prevents
uncontrolled semantic recall of old personal conversations and keeps user deletion,
permission changes, and retention deterministic.

A future proposal for semantic conversation recall requires a separate ADR, explicit
tenant/user consent, deletion proof, isolation tests, and security/privacy approval.

## 7. Reauthorize memory on every turn

Memory is context, never authorization. Every request revalidates:

- Trusted `TenantId` and current `UserId`.
- Conversation ownership or explicitly delegated scope.
- Current RBAC permissions and ABAC scope.
- User/employment/account status.
- Tenant memory policy and feature entitlement.
- Source/document approval, effective date, sensitivity, and current permission tags.

`SecurityContextVersion` is generated from server-side authorization versions, including
role/permission, ABAC policy, assignment/scope, delegation, and account-state versions. It
does not store raw roles or sensitive attributes.

If the current version differs from stored memory:

1. Session memory is invalidated.
2. Durable summaries are not added to the model context.
3. Each source reference is reauthorized.
4. The summary is re-created from still-authorized information or retired.
5. The invalidation and outcome are audited.

Permission checks are repeated even when the version matches, so a missed invalidation
event cannot become the only security control.

## 8. Invalidate memory through domain events

ADR-009 events trigger scoped invalidation, including:

- `UserPermissionsChanged`
- `UserRoleChanged`
- `TenantRoleMatrixChanged`
- `EmployeeAssignmentChanged`
- `EmployeeStatusChanged`
- `DelegationChanged`
- `KnowledgeDocumentSuperseded`
- `KnowledgeDocumentDeleted`
- `MemoryPolicyChanged`
- `TenantSuspended`
- `TenantOffboardingStarted`

Events carry identifiers and versions only, not conversation content. Consumers are
idempotent. A periodic reconciliation job checks for missed/stale security-context versions.

## 9. Summarize safely and preserve provenance

Summarization runs only when the tenant policy enables it and a configured turn/token/time
threshold is reached.

The summarizer:

1. Receives only currently authorized session content.
2. Treats all conversation text as untrusted data, never system instructions.
3. Removes unnecessary PII and sensitive tool output.
4. Separates user-stated facts, cited source facts, unresolved questions, preferences, and
   assistant assumptions.
5. Retains source IDs, document versions, effective dates, permission tags, and uncertainty.
6. Rejects or flags instructions attempting to change system policy, tools, identity,
   tenant, permissions, retention, or safety behavior.
7. Records the exact included range as `SummarySourceTurnStart` and
   `SummarySourceTurnEnd`.
8. Produces a new immutable summary version; prior versions follow retention policy.
9. Runs the approved summary-quality evaluation and stores `SummaryQualityScore` plus the
   evaluation version.

A summary cannot convert an unsupported answer into a fact. Cited source facts are
re-retrieved and reauthorized when needed. User-provided facts are labeled as user-provided
and are not treated as verified HR records.

Summarization uses `ILlmProvider` with an admin-approved model assignment and budget. The
feature does not depend on provider-native memory or summarization state.

`SummaryQualityScore` is informational operational/evaluation metadata. It may trigger
review, regeneration, or model comparison, but it never grants authorization, upgrades a
source's trust, converts an unsupported statement into fact, or bypasses confidence and
citation rules. ADR-034 defines the final scoring method and promotion thresholds.

## 10. Assemble context with a bounded token budget

The context orchestrator allocates a configurable token budget in this priority order:

1. System/safety instructions.
2. Current user request.
3. Current identity, tenant, permission, locale, and use-case policy.
4. Fresh authorized RAG/tool results.
5. Latest authorized conversation summary.
6. Most recent authorized session turns, newest first.

Memory is dropped before safety instructions or fresh authoritative evidence. When content
does not fit, the system summarizes or omits older context and tells the user when material
context was unavailable. It never silently truncates citations or security instructions.

## 11. Defend against memory poisoning and replay

- Stored user/assistant text is always marked as untrusted conversation content.
- Instructions inside memory cannot override system, tenant, safety, or tool policy.
- Session entries and summaries carry integrity/version checks.
- Message IDs and idempotency keys prevent duplicate/replayed turns.
- Conversation access is ownership/ABAC checked to prevent IDOR.
- Inputs and summaries pass prompt-injection and sensitive-data detectors.
- Cross-user conversation linking is forbidden unless a separately approved collaborative
  conversation design exists.
- Support impersonation/delegation is explicitly scoped, displayed, time-boxed, and audited;
  it does not merge the support user's personal memory with the target user's memory.

## 12. Apply configurable retention, deletion, and legal hold

Initial policy limits:

| Memory data | Default | Platform-governed options before ADR-022 finalization |
|---|---|---|
| Turn context | Destroy after response | Request lifetime only |
| Session memory | 30-minute idle, 24-hour absolute | Platform-configured maximum |
| Conversation metadata | Policy-controlled | 30, 60, or 90 days within approved policy limits |
| Conversation summary | Disabled | 30, 60, or 90 days when tenant explicitly enables it |
| Full transcript | Disabled | Not permitted without separate approval |
| Long-term personal memory | Disabled | Not permitted without separate approval |

ADR-022 must finalize retention, archive, backup-erasure, legal-hold, and deletion schedules
before implementation approval. Allowed retention values and maximums are effective-dated
platform configuration, not feature-code constants. The policy engine prevents unlimited
retention and may restrict a tenant to shorter options based on sensitivity, jurisdiction,
service tier, or compliance policy.

Users can request deletion of eligible memory. Tenant administrators can apply policy-wide
deletion, and offboarding deletes all eligible tenant memory. Legal hold pauses eligible
purge through a separately authorized workflow without making held content available to AI.

Deletion covers Redis entries, SQL summaries/metadata, replicas, exports, backups according
to policy, and provider-side temporary state. Completion is auditable and testable.

## 13. Define API and permission requirements

The Phase 6D OpenAPI must include:

| Endpoint | Permission | Behavior |
|---|---|---|
| `POST /api/v1/ai/conversations` | `AI.Use` | Create conversation under current tenant/user/policy |
| `POST /api/v1/ai/conversations/{id}/messages` | `AI.Use` plus ownership/ABAC | Add idempotent turn after reauthorization |
| `GET /api/v1/ai/conversations/{id}` | `AI.Use` plus ownership/ABAC | Return eligible summary and currently retained session turns only |
| `POST /api/v1/ai/conversations/{id}/reset` | `AI.Use` plus ownership/ABAC | Clear active continuity context while preserving metadata/audit |
| `DELETE /api/v1/ai/conversations/{id}` | `AI.ManageOwnMemory` or `AI.ManageMemory` | Request eligible deletion with audit |
| `GET /api/v1/ai/admin/memory-policies` | `AI.ManageMemory` | View effective tenant memory policy |
| `PUT /api/v1/ai/admin/memory-policies/{id}` | `AI.ManageMemory` | Create immutable effective-dated policy version |

All endpoints use `/api/v1`, JWT, server-resolved tenant context, RBAC plus ABAC,
correlation IDs, standard envelopes, rate limits, and audit. Mutations require an
`Idempotency-Key`. Raw memory content is never returned to tenant administrators unless
they independently have authorization to the conversation and every referenced source.

Reset is idempotent and increments `ContextGeneration`. It removes active Redis session
memory and retires eligible summaries from future context assembly, while preserving the
conversation record, reset event, and mandatory audit history. It is not a deletion or
legal-hold bypass. A reset cannot restore older context, and in-flight summary results from
an earlier context generation are discarded.

## 14. Handle concurrency and ordering deterministically

- Each conversation has a monotonically increasing turn sequence and optimistic version.
- Concurrent message submissions are serialized per conversation or rejected with a
  conflict that the client can safely retry.
- Idempotency is scoped by tenant, conversation, and message ID.
- Summary versions reference the exact included start/end turn range and context generation.
- Late/failed summary jobs cannot overwrite a newer summary.
- Deletion or invalidation wins over in-flight summarization; the result is discarded.

## 15. Fail safely into stateless mode

- If Redis is unavailable, the request may continue without session memory when the use
  case permits; the response indicates that prior context was unavailable.
- If SQL summaries are unavailable, the system uses fresh authorized context only.
- If authorization or tenant resolution is unavailable, the request fails closed.
- A failed/low-confidence summary is not stored or used.
- Memory failure cannot cause a fallback to provider-hosted hidden memory.
- Durable deletion, audit, and security events use the event/outbox path and are not lost
  because a cache is unavailable.

## 16. Observe memory without logging its content

ADR-031 telemetry includes low-cardinality metrics for:

- Session memory hit, miss, expiry, eviction, and invalidation.
- Summary generation duration, success/failure, and version conflict.
- Summary-quality score distribution, evaluation version, and regeneration rate.
- Token reduction from summary/context compaction.
- Stateless degraded-mode activation.
- Permission-context mismatch and memory-poisoning blocks.
- Deletion request age and completion outcome.

Prompts, turns, summaries, source IDs, user/tenant IDs, and sensitive fields are prohibited
from operational metrics, traces, and logs.

## 17. Bound cost and storage

- Per-tenant/user conversation, turn, byte, token, and summary quotas are effective-dated
  policy data.
- Summarization occurs at thresholds, not after every turn.
- An approved lower-cost model may summarize when quality/security evaluation permits.
- Oversized conversations are compacted, ended, or continued in a new conversation rather
  than retained without limit.
- Redis and SQL usage feed ADR-033 cost governance without exposing content.

## 18. Reserve Workspace Memory as a separate future capability

Some multi-session work is a persistent user-created business artifact, not conversational
history. Examples include:

- Draft reports and report specifications.
- Workflow definitions under iterative refinement.
- Policy, form, navigation, and configuration drafts.
- Other named work products that users intentionally save and resume.

These artifacts require a future **Workspace Memory** ADR and are explicitly outside this
conversation-memory decision. Workspace Memory must:

- Store a typed, named business artifact with owner, collaborators, purpose, module, status,
  version, effective dates, and lifecycle.
- Use the owning module's RBAC/ABAC, workflow, audit, retention, and approval controls.
- Support explicit save, resume, share, submit, archive, and delete operations.
- Never depend on a chat transcript as the artifact's system of record.
- Keep conversation context as optional provenance, not hidden authority.
- Define conflict handling, collaboration, data classification, legal hold, and export.

Until that ADR and constitutional five-document set are Approved, multi-session business
artifacts use their owning module's normal draft entities rather than conversation memory.

---

# Alternatives Considered

## Remain completely stateless

Strong privacy and simplicity, but poor multi-turn usability and repeated tokens/retrieval.
Supported as tenant mode, but rejected as the only platform behavior.

## Store full transcripts permanently in SQL Server

Simple history and debugging, but excessive sensitive-data retention, deletion burden, and
breach impact. Rejected as the default.

## Store conversation embeddings in Qdrant

Enables semantic recall, but makes permission changes, deletion, memory poisoning, and
purpose limitation harder. Rejected for the initial architecture.

## Use provider-native threads and memory

Convenient but weakens provider portability, creates hidden retention, and reduces control
over authorization and deletion. Rejected.

## Build long-term personalized employee profiles automatically

Could improve personalization but creates significant privacy, fairness, transparency, and
employment-risk concerns. Rejected without separate consent, requirements, and ADR.

## Store all memory only in Redis

Good for short sessions but unsuitable for controlled cross-session summaries, legal hold,
auditable deletion workflows, and durable policy metadata. Rejected as the sole store.

## Keep memory only in the browser

Reduces server storage but cannot reliably enforce enterprise retention, deletion, audit,
cross-device continuity, or safe authorization. Rejected as the primary design.

---

# Consequences

## Positive

- Useful multi-turn conversations without default long-term profiling.
- Current permissions are rechecked before every reuse.
- Provider/model switching does not lose or expose hidden provider memory.
- Session data is short-lived; durable storage contains compact summaries only when enabled.
- Qdrant remains limited to approved knowledge, simplifying privacy and deletion.
- Context/token use is bounded and measurable.
- Stateless degraded mode preserves availability without fabricating memory.

## Negative

- Summaries may omit nuance and require careful evaluation.
- Redis, SQL summary, invalidation, deletion, and reconciliation flows add complexity.
- Full conversation history is not available by default.
- Permission changes may intentionally remove conversational continuity.
- Production Redis and encrypted SQL summary storage still have infrastructure/operations
  cost.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Cross-tenant/user memory disclosure | Trusted key builder, RLS, ownership/ABAC, reauthorization, negative tests |
| Stale access after permission change | SecurityContextVersion, events, reconciliation, per-turn checks |
| Memory prompt injection/poisoning | Untrusted-data boundary, detectors, no system-instruction inheritance |
| Sensitive retention | SessionOnly default, summary opt-in, no transcript/profile, TTL and deletion |
| Incorrect summary becomes fact | Provenance/uncertainty, immutable versions, citations re-retrieved, evaluation |
| Redis loss/outage | Stateless degraded mode; durable summary optional; no security bypass |
| Provider retains hidden state | Stateless provider calls and adapter controls |
| Excess token/storage cost | Context budgets, quotas, threshold summarization, bounded retention |
| Deletion misses replicas/backups | ADR-022 workflow, deletion ledger, tests, provider-state verification |
| Concurrent turns corrupt context | Sequence/version, idempotency, serialization/conflict handling |

---

# Acceptance Criteria Before Approval/Implementation

| ID | Criterion |
|---|---|
| CM-AC-001 | Default policy is `SessionOnly`; durable summaries, transcripts, semantic conversation recall, and long-term personal memory are disabled. |
| CM-AC-002 | Every memory operation derives tenant/user scope from trusted server context and passes ownership plus RBAC/ABAC checks. |
| CM-AC-003 | Cross-tenant, cross-user, guessed-ID, and delegated/impersonation negative tests return no unauthorized memory. |
| CM-AC-004 | Permission, role, assignment, delegation, employee-status, policy, and document changes invalidate affected memory before reuse. |
| CM-AC-005 | Stored memory contains no raw tool payloads, retrieved chunks, vectors, secrets, tokens, hidden reasoning, or unnecessary HR fields. |
| CM-AC-006 | Qdrant contains no conversation turn, summary, or inferred personal-preference vectors. |
| CM-AC-007 | Summaries preserve provenance, source versions, permission tags, uncertainty, and included turn sequence. |
| CM-AC-008 | Prompt-injection/memory-poisoning tests prove stored text cannot override system, tenant, authorization, tool, retention, or safety policy. |
| CM-AC-009 | Context-budget tests never truncate safety instructions or required citations and clearly signal unavailable material context. |
| CM-AC-010 | Redis/summary-store outages produce stateless degraded behavior without cross-tenant fallback or fabricated continuity. |
| CM-AC-011 | Idle/absolute TTL, maximum retention, quota, and policy changes are effective-dated configuration rather than feature-code constants. |
| CM-AC-012 | User deletion, tenant deletion, offboarding, legal hold, and backup-erasure workflows pass approved ADR-022 tests. |
| CM-AC-013 | Concurrent/replayed message tests preserve ordering, idempotency, summary version, and deletion precedence. |
| CM-AC-014 | Memory APIs are versioned, OpenAPI-documented, audited, tenant-isolated, and contract-tested. |
| CM-AC-015 | Telemetry reports memory health and token reduction without exporting conversation content or raw identities. |
| CM-AC-016 | Switching LLM providers requires no memory migration to provider-hosted threads and no feature-code change. |
| CM-AC-017 | Unit coverage is at least 85%, with integration, security, privacy, concurrency, expiry, deletion, and end-to-end tests. |
| CM-AC-018 | Every summary stores exact source-turn start/end lineage and context generation, enabling deterministic regeneration and audit. |
| CM-AC-019 | Summary quality metadata is versioned and informational only; it cannot influence authorization or source trust. |
| CM-AC-020 | `TenantRoleMatrixChanged` invalidates memory created under the prior role-permission mapping. |
| CM-AC-021 | Conversation reset clears active continuity, increments context generation, preserves metadata/audit, and discards stale in-flight summaries. |
| CM-AC-022 | Purpose changes reauthorize and reduce/reset context or require a new conversation when domain/sensitivity/tool boundaries differ. |
| CM-AC-023 | Summary/metadata retention supports approved 30/60/90-day options while enforcing platform security/compliance maximums. |
| CM-AC-024 | Persistent report/workflow/policy/form artifacts are excluded from conversation memory and require Workspace Memory or owning-module draft governance. |

---

# Impact

## Architecture

Adds a memory-policy and purpose evaluator, centralized Redis key builder, conversation context
assembler, safe summarizer, security-context versioning, event-driven invalidation,
reconciliation, reset/deletion orchestration, summary lineage/quality metadata, and
stateless degraded mode. Workspace Memory remains a separately governed future capability.

## Database

Requires `AI.Conversation`, `AI.ConversationSummary`, `AI.MemoryPolicy`, and
`AI.MemoryDeletionRequest` in the future AI DB design. All are tenant-scoped with mandatory
audit/version columns, RLS, indexes, encrypted sensitive content, effective dates, and
retention/purge behavior. The design includes purpose/version/context-generation fields,
summary source-turn lineage, and informational summary-quality metadata.

## Security

Adds per-turn memory authorization, ownership checks, security-context invalidation,
memory-poisoning controls, encrypted summaries, restricted deletion/legal-hold workflows,
and cross-tenant/cross-user memory testing.

## Performance

Redis supports low-latency recent context. SQL summaries reduce context tokens but add
occasional summarization cost. Limits, quotas, asynchronous summarization, and stateless
fallback bound latency and storage growth.

## Development

Technical, Database, UI, API/OpenAPI, Security, and Test documents must implement these
contracts and acceptance criteria. No code starts until the constitutional five-document
set and OpenAPI are Approved.

## Operations

Operations owns Redis capacity/backup policy, expiry health, invalidation/reconciliation,
summary-store health, deletion completion, and memory runbooks. Security owns policy
maximums, poisoning controls, access review, and incident response.

---

# Official References

- OWASP GenAI prompt injection risk:
  `https://genai.owasp.org/llmrisk/llm01-prompt-injection/`
- Redis key expiration: `https://redis.io/docs/latest/commands/expire/`
- SQL Server Row-Level Security:
  `https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security`
- NIST Privacy Framework: `https://www.nist.gov/privacy-framework`

References last validated: 2026-06-23.

---

# Approval

Solution Architect: Approved (Agent 6 / Codex)  
Security Architect: ____  
Database Architect: ____  
.NET Architect: ____  
Prompt/Context Engineer: ____  
Product Owner: Bhajan Lal - Approved 2026-06-24

(Status: Approved)
