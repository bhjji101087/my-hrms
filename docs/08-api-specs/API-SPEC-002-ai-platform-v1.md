# API Specification - AI Platform Endpoints v1

Document Owner: API Governance + .NET Architect
Created Date: 2026-06-27
Version: 1.0
Status: Approved
Reviewers: Solution Architecture, Security, Data Governance/Privacy, Platform/Operations, Product/AI, Domain Owners

Machine-readable OpenAPI artifact:

- `docs/08-api-specs/OPENAPI-002-ai-platform-v1.yaml`

Related approved documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md`
- `docs/15-ai/AI-OPS-001-enterprise-ai-operations.md`
- `docs/15-ai/AI-DR-001-disaster-recovery-and-exercise-plan.md`
- `docs/12-security/SEC-AI-001-ai-security-extension.md`
- ADR-019 Enterprise AI/RAG Platform Architecture
- ADR-022 Data Retention, Archival, Legal Hold, and Deletion
- ADR-030 Enterprise Vector Store Strategy
- ADR-031 AI Observability and Telemetry
- ADR-032 Conversation Memory Strategy
- ADR-033 AI Cost Governance
- ADR-034 Enterprise AI and RAG Evaluation Framework
- ADR-035 Enterprise Semantic and Retrieval Cache Architecture

---

# 1. Purpose

This specification defines the public and administrative REST API surface for the governed
AI platform. It covers AI conversations, stateless Q&A, knowledge ingestion, evaluation,
deployment-bundle governance, operational disablement, cache namespace rotation, disaster
recovery exercise status, and retention reconciliation status.

The API is intentionally policy-driven. It exposes controlled operations while preserving
tenant isolation, RBAC/ABAC, audit, OpenAPI documentation, no direct AI state mutation, and
provider independence.

---

# 2. API Conventions

- **Base path:** `/api/v1`
- **Content type:** `application/json`
- **Authentication:** JWT bearer token on every endpoint.
- **Tenant context:** resolved server-side from identity/host/tenant catalog; never trusted
  from request body.
- **Authorization:** RBAC plus ABAC on every endpoint and object.
- **Response envelope:** existing platform envelope:
  `{ "success": true, "message": "", "data": { ... } }`
- **Error envelope:** existing platform envelope:
  `{ "success": false, "message": "...", "errors": [ ... ] }`
- **Correlation:** `X-Correlation-Id` accepted and echoed.
- **Idempotency:** `Idempotency-Key` required for critical POST operations.
- **Pagination:** `page`, `pageSize`, `sort`, `filter`, `search` on list endpoints.
- **Audit:** every AI request emits AI audit metadata; administrative/destructive actions
  emit immutable audit and outbox events.
- **Security denial:** authorization, policy, budget, safety, retention, degraded-mode, and
  incident-disablement denials are explicit, not generic 500s.

OpenAPI 3.0.3 is used for compatibility with the already-approved foundational OpenAPI file.

---

# 3. Non-Negotiable API Security Rules

1. AI APIs cannot directly create, update, delete, approve, publish, payroll, workflow,
   identity, provider, or configuration business state outside approved admin APIs.
2. AI answer endpoints must reauthorize retrieval, memory, cache, tool calls, and output
   release per request.
3. AI APIs do not expose raw vectors, raw cache entries, raw memory entries, system prompts,
   provider secrets, hidden reasoning, unrestricted source chunks, or other tenants'
   diagnostics.
4. Operational APIs require elevated permissions, reason, approval reference where required,
   optimistic concurrency where applicable, idempotency, and audit.
5. Degraded mode must fail closed when policy, tenant, authorization, audit, or retention
   state cannot be verified.

---

# 4. Endpoint Groups

| Group | Purpose |
|---|---|
| Conversations | Purpose-scoped session and message API for Copilot surfaces. |
| Stateless AI | Single-turn `ask` API for approved RAG/read-only answers. |
| Knowledge | Tenant-approved source ingestion, validation, indexing, and publication. |
| Evaluation | Evaluation runs and promotion evidence from ADR-034. |
| Governance bundles | Model/prompt/index/cache/memory/evaluation bundle lifecycle. |
| Operations | Health, status, disablement, degraded mode, and emergency controls. |
| Cache operations | Namespace rotation and cache disablement status. |
| DR and retention | DR exercise and restore/deletion reconciliation status. |
| Streaming | SSE-based progressive responses for ask and conversation messages. |
| Batch | Multiple independent governed AI requests in one API call. |
| Bulk knowledge | Bulk source registration, validation, publication, archival, and metadata updates. |

---

# 5. Conversation APIs

## POST `/ai/conversations`

Creates a purpose-scoped AI conversation.

Permissions:

- `AI.Conversation.Create`

Request:

```json
{
  "purposeKey": "PolicySupport",
  "locale": "en-IN",
  "metadata": {
    "surface": "Copilot"
  }
}
```

Response:

```json
{
  "success": true,
  "message": "",
  "data": {
    "conversationId": "018ff2b2-8c4c-7ad8-a96b-d4f98bba1191",
    "purposeKey": "PolicySupport",
    "memoryMode": "SessionOnly",
    "status": "Active"
  }
}
```

Controls:

- Purpose must exist in the tenant-approved purpose catalog.
- Memory mode is resolved by policy, not caller preference.
- Conversation scope is tenant/user-bound and cannot be transferred by request body.

## GET `/ai/conversations`

Lists the caller's authorized conversations. Admin cross-user listing requires separate
permission and ABAC scope.

Permissions:

- `AI.Conversation.View`

Query:

- `status`
- `purposeKey`
- `page`
- `pageSize`

## GET `/ai/conversations/{conversationId}`

Returns conversation metadata and current policy state. It does not return unrestricted full
transcripts.

Permissions:

- `AI.Conversation.View`

## POST `/ai/conversations/{conversationId}/messages`

Submits a user message and returns a governed AI response.

Permissions:

- `AI.Conversation.Message`

Headers:

- `Idempotency-Key` required.

Request:

```json
{
  "message": "What is our maternity leave policy?",
  "clientMessageId": "client-123",
  "responseMode": "AnswerWithCitations"
}
```

Response includes:

- Answer text.
- Citations.
- Confidence band.
- Refusal/escalation reason where applicable.
- Prompt/model/index/policy versions.
- Audit reference.

Security:

- Prompt injection detection runs before context assembly.
- Memory/cache/retrieval/tool context is reauthorized.
- Output guardrails run before release.
- AI cannot execute business actions.

## POST `/ai/conversations/{conversationId}/messages/stream`

Streams a governed conversation response using Server-Sent Events (SSE). SSE is the
preferred streaming transport for request/response AI interactions because it stays within
HTTP, supports progressive text delivery, and does not introduce bidirectional autonomous
agent behavior.

Permissions:

- `AI.Conversation.Message`

Headers:

- `Idempotency-Key` required.
- `Accept: text/event-stream`

Response:

- `Content-Type: text/event-stream`

Streaming event types:

| Event | Purpose |
|---|---|
| `ai.started` | Stream accepted, request/audit IDs assigned, policy versions resolved. |
| `ai.delta` | Partial answer text. |
| `ai.citation` | Citation metadata when available. |
| `ai.confidence` | Confidence band/components when computed. |
| `ai.warning` | Degraded mode, low confidence, partial context, or escalation warning. |
| `ai.completed` | Final answer metadata, usage/cost summary, audit reference, and terminal status. |
| `ai.error` | Safe error code/message. |
| `ai.cancelled` | Server or client cancellation acknowledged and audited. |

Streaming controls:

- The same security, budget, cache, memory, retrieval, citation, and output controls apply as
  non-streaming messages.
- Partial answer text must not be emitted until tenant, authorization, safety, and minimum
  output checks allow release.
- Citations may be streamed incrementally, but final `ai.completed` includes the complete
  citation set used for released material claims.
- Cancellation records usage, cost, audit, and telemetry up to the cancellation point.
- Telemetry records time-to-first-token, stream duration, token count, cancellation/error
  state, and final release decision.

## POST `/ai/conversations/{conversationId}/reset`

Clears active session memory and eligible continuity context while preserving audit and
conversation metadata.

Permissions:

- `AI.Conversation.Reset`

Headers:

- `Idempotency-Key` required.

Audit:

- `AiConversationReset`

---

# 6. Stateless Ask API

## POST `/ai/ask`

Single-turn governed AI request for approved RAG/read-only answers.

Permissions:

- `AI.Ask`

Headers:

- `Idempotency-Key` required.

Request:

```json
{
  "purposeKey": "PolicySupport",
  "question": "Which holidays apply to Maharashtra employees?",
  "locale": "en-IN",
  "responseMode": "AnswerWithCitations"
}
```

Controls:

- No durable conversation memory is created.
- Same tenant, RBAC/ABAC, safety, budget, cache, retrieval, citation, and output controls as
  conversation messages.
- Response may refuse, caution, or escalate when evidence is insufficient.

## POST `/ai/ask/stream`

Streams a stateless governed AI response using SSE.

Permissions:

- `AI.Ask`

Headers:

- `Idempotency-Key` required.
- `Accept: text/event-stream`

Response:

- `Content-Type: text/event-stream`

Uses the same event model as conversation streaming: `ai.started`, `ai.delta`,
`ai.citation`, `ai.confidence`, `ai.warning`, `ai.completed`, `ai.error`, and
`ai.cancelled`.

Stateless streaming does not create durable conversation memory. It still emits audit,
telemetry, usage, cost, safety, and retention metadata.

---

# 7. Batch AI API

## POST `/ai/batch`

Executes multiple independent governed AI requests in one API call. Batch is for enterprise
efficiency, not for bypassing per-request policy.

Permissions:

- `AI.Batch.Execute`

Headers:

- `Idempotency-Key` required for the batch.

Rules:

- Default maximum batch size: 25 requests.
- Platform maximum batch size: 100 requests, configurable by tenant/service tier.
- Each item is independently validated, authorized, budget-reserved, audited, evaluated for
  safety, and rate-limit counted.
- Partial success is allowed. A failed item does not fail the entire batch unless the
  top-level request is invalid.
- Each item returns its own status, citations, confidence, refusal/escalation reason, and
  audit reference.
- Idempotency applies to the batch key plus item `clientRequestId`.
- Batch execution cannot broaden tenant, role, ABAC, source, memory, or cache scope.
- Streaming is not supported inside batch v1.

Rate-limit and cost behavior:

- A batch consumes one request unit plus per-item AI operation units.
- Provider/token/cost budgets are reserved per item.
- If the tenant or user budget is exhausted mid-batch, remaining items return item-level
  budget errors.

---

# 8. Knowledge APIs

Knowledge APIs are tenant-admin controlled. They never publish an index directly from upload
without validation.

## GET `/ai/knowledge/sources`

Lists authorized knowledge sources and versions.

Permissions:

- `AI.Knowledge.View`

## POST `/ai/knowledge/sources`

Registers a source document or source reference.

Permissions:

- `AI.Knowledge.Manage`

Headers:

- `Idempotency-Key` required.

Request fields:

- `sourceType`
- `title`
- `classification`
- `jurisdiction`
- `locale`
- `effectiveFrom`
- `effectiveTo`
- `ownerUserId`
- `retentionPolicyKey`

Controls:

- File upload endpoints must validate extension, MIME, size, malware scan, hidden text, and
  prompt-injection markers.
- Unknown classification is rejected.

## POST `/ai/knowledge/sources/{sourceId}/versions`

Creates a new source version and starts ingestion staging.

## POST `/ai/knowledge/sources/{sourceId}/versions/{versionId}/validate`

Runs extraction, classification, chunking, prompt-injection, malware, metadata, isolation,
and retrieval validation.

## POST `/ai/knowledge/sources/{sourceId}/versions/{versionId}/publish`

Publishes an approved source version and starts shadow-index build/promotion workflow.

Controls:

- Running AI responses remain pinned to existing index versions.
- Shadow index must pass ADR-030, ADR-034, and SEC-AI-001 tests before alias promotion.

## GET `/ai/knowledge/ingestion-jobs/{jobId}`

Returns job state, validation result, failed item count, evidence references, and next action.

## POST `/ai/knowledge/sources/bulk`

Registers multiple source metadata records.

Permissions:

- `AI.Knowledge.Manage`

Rules:

- Default maximum bulk size: 100 sources.
- Each source is independently validated.
- Partial success is allowed with per-item status and error details.
- No source is published by this endpoint.
- Per-item audit records are produced.

## POST `/ai/knowledge/sources/bulk/validate`

Starts validation jobs for multiple source versions.

## POST `/ai/knowledge/sources/bulk/publish`

Starts publication/index workflows for multiple validated source versions.

## POST `/ai/knowledge/sources/bulk/archive`

Archives or retires multiple approved sources according to retention/legal-hold policy.

## PATCH `/ai/knowledge/sources/bulk/metadata`

Applies approved metadata updates such as owner, jurisdiction, locale, permitted
classification changes, effective dates, and retention policy key.

Bulk knowledge controls:

- Bulk actions preserve all single-source validation, approval, retention, audit, and
  security controls.
- Partial success is explicit and itemized.
- Legal hold, deletion tombstones, source ownership, malware state, and prompt-injection
  validation remain mandatory.
- Bulk publish cannot bypass shadow-index validation or alias promotion rules.

---

# 9. Evaluation APIs

## POST `/ai/evaluations/runs`

Starts an evaluation run for a full AI deployment bundle.

Permissions:

- `AI.Evaluation.Manage`

Headers:

- `Idempotency-Key` required.

Required request fields:

- `useCaseKey`
- `bundleId`
- `datasetVersion`
- `riskTier`
- `reason`

## GET `/ai/evaluations/runs`

Lists evaluation runs with filters for use case, bundle, status, risk tier, and approval
state.

## GET `/ai/evaluations/runs/{runId}`

Returns evaluation summary, metrics, hallucination rate/severity, drift signals, reviewer
quality metrics, promotion eligibility, and evidence links.

Controls:

- Sealed evaluation datasets are not exposed through the API.
- Raw employee data is not returned.

---

# 10. Governance Bundle APIs

## GET `/ai/governance/bundles`

Lists model/prompt/index/cache/memory/evaluation deployment bundles.

Permissions:

- `AI.Governance.View`

## POST `/ai/governance/bundles`

Creates a Draft bundle.

Permissions:

- `AI.Governance.Manage`

Headers:

- `Idempotency-Key` required.

## POST `/ai/governance/bundles/{bundleId}/transitions`

Moves a bundle through the approved lifecycle:

`Draft -> Evaluation -> Approved -> Canary -> Production -> Deprecated -> Retired`

Controls:

- Required transition evidence is validated.
- Governance Board approval is required for significant changes.
- `Canary` and `Production` require rollback bundle.
- `Retired` cannot be reactivated.

---

# 11. Operations and Emergency APIs

## GET `/ai/operations/status`

Returns tenant-safe AI operational status, degraded-mode state, dependency health, active
disablements, policy expiry warnings, and maintenance windows.

Permissions:

- `AI.Operations.View`

## POST `/ai/operations/disablements`

Creates a scoped emergency disablement.

Permissions:

- `AI.Operations.Manage`

Headers:

- `Idempotency-Key` required.

Scopes:

- Global
- Tenant
- Use case
- Provider
- Model
- Prompt bundle
- Index
- Memory
- Cache

Controls:

- Requires reason, severity, approval reference when required, expiry time, and rollback
  condition.
- Fully audited.
- Does not require code deployment.

## POST `/ai/operations/disablements/{disablementId}/release`

Releases an active disablement after validation evidence is recorded.

---

# 12. Cache and DR APIs

## POST `/ai/cache/namespaces/{namespaceId}/rotate`

Rotates a cache namespace after poisoning, policy change, source change, deletion, or
incident.

Permissions:

- `AI.Cache.Manage`

## GET `/ai/dr/exercises`

Lists DR exercises and evidence summaries.

Permissions:

- `AI.Operations.View`

## POST `/ai/dr/exercises`

Starts or records a DR exercise plan.

Permissions:

- `AI.Operations.Manage`

## GET `/ai/retention/reconciliation-jobs/{jobId}`

Returns restore/deletion/legal-hold reconciliation status for AI derived stores.

Permissions:

- `AI.Retention.View`

---

# 13. Rate-Limit and Retry Headers

AI APIs return tenant-safe rate-limit headers where applicable:

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Current request limit for the relevant tenant/user/use-case window. |
| `X-RateLimit-Remaining` | Remaining requests or operation units in the current window. |
| `X-RateLimit-Reset` | UTC epoch seconds when the current window resets. |
| `Retry-After` | Seconds or HTTP date after which retry may be attempted for `429` or temporary `503`. |

Rules:

- Headers do not reveal other tenants' capacity, commercial terms, or provider limits.
- Budget denial may include rate-limit headers when useful, but budget and rate limit remain
  separate controls.
- Streaming responses include rate-limit headers in the initial HTTP response before events
  begin.
- Batch responses include top-level headers plus per-item rate/budget status.
- Clients must use backoff and must not retry idempotent AI requests without the same
  `Idempotency-Key`.

---

# 14. API Versioning and Deprecation Policy

Versioning rules:

- Public AI APIs use URL major versioning: `/api/v1`.
- Non-breaking additions may be added to `v1`: new optional fields, new enum values when
  clients are instructed to handle unknown values, new endpoints, new headers, and new
  response metadata.
- Breaking changes require a new major version such as `/api/v2`.
- Security tightening, tenant-isolation fixes, prohibited-data removal, and incident-driven
  disablement may occur in `v1` when required to protect tenants.
- Provider/model/vector/cache changes remain configuration-driven and should not require API
  version changes unless the external contract changes.

Deprecation and sunset:

- Deprecated endpoints include deprecation metadata in documentation and may return
  `Deprecation` and `Sunset` headers when a retirement date is known.
- Standard enterprise notice target: at least 180 days before removal for generally
  available APIs, unless a critical security/legal issue requires faster action.
- Migration guidance must identify replacement endpoints, behavior differences, data
  migration needs, test guidance, and support timeline.
- Retired endpoints return `410 Gone` with a safe error code and migration reference where
  allowed.
- Preview/internal endpoints must be clearly marked and cannot be used as stable tenant
  integrations.

Compatibility expectations:

- Clients must ignore unknown response fields.
- Clients must tolerate new safe error codes.
- Clients must not depend on ordering of JSON object properties.
- Clients must not parse human-readable `message` text for business logic.

---

# 15. Standard Errors

| HTTP | Meaning |
|---|---|
| 400 | Schema or validation error |
| 401 | Missing or invalid authentication |
| 403 | RBAC/ABAC, tenant, policy, or data-scope denial |
| 404 | Resource not found or not visible to caller |
| 409 | Conflict, idempotency conflict, lifecycle transition conflict |
| 410 | Retired/deleted resource no longer available |
| 422 | Business/policy/evaluation/retention rule failure |
| 423 | Locked due legal hold, incident, maintenance, or lifecycle gate |
| 429 | Rate, quota, or budget limit |
| 503 | AI dependency unavailable or degraded |

Error details include safe machine-readable codes such as:

- `AI_POLICY_DENIED`
- `AI_PERMISSION_DENIED`
- `AI_SAFETY_BLOCKED`
- `AI_BUDGET_EXCEEDED`
- `AI_DEGRADED`
- `AI_INCIDENT_DISABLED`
- `AI_RETENTION_BLOCKED`
- `AI_EVALUATION_REQUIRED`

---

# 16. Events and Audit

AI APIs publish only identifier/version/status metadata through outbox events. Events do not
carry raw prompts, responses, source chunks, vectors, cache entries, or secrets.

Required events include:

- `AiConversationCreated`
- `AiConversationReset`
- `AiRequestCompleted`
- `AiSafetyBlocked`
- `AiStreamStarted`
- `AiStreamCompleted`
- `AiStreamCancelled`
- `AiBatchRequested`
- `AiBatchItemCompleted`
- `AiKnowledgeSourceRegistered`
- `AiKnowledgeBulkOperationRequested`
- `AiKnowledgeVersionPublished`
- `AiIndexPromotionRequested`
- `AiEvaluationRunStarted`
- `AiEvaluationRunCompleted`
- `AiBundleLifecycleTransitioned`
- `AiEmergencyDisablementCreated`
- `AiEmergencyDisablementReleased`
- `AiCacheNamespaceRotationRequested`
- `AiDrExerciseStarted`
- `AiRetentionReconciliationCompleted`

---

# 17. Acceptance Criteria

| ID | Criterion |
|---|---|
| API-AI-AC-001 | Every AI endpoint is represented in `OPENAPI-002-ai-platform-v1.yaml`. |
| API-AI-AC-002 | Every endpoint requires JWT, server-resolved tenant context, RBAC, ABAC, correlation ID, and audit where applicable. |
| API-AI-AC-003 | Critical POST operations require `Idempotency-Key`. |
| API-AI-AC-004 | AI response endpoints include citations, confidence, refusal/escalation metadata, and prompt/model/index/policy versions. |
| API-AI-AC-005 | No API exposes raw vectors, raw cache entries, unrestricted memory, system prompts, provider secrets, hidden reasoning, or cross-tenant diagnostics. |
| API-AI-AC-006 | Operational/destructive APIs require reason, approval reference where required, audit, idempotency, and safe status tracking. |
| API-AI-AC-007 | Knowledge publication uses staged validation and shadow-index promotion; no upload directly activates production RAG. |
| API-AI-AC-008 | Bundle lifecycle transitions enforce Draft/Evaluation/Approved/Canary/Production/Deprecated/Retired rules and rollback evidence. |
| API-AI-AC-009 | Error responses distinguish auth, policy, safety, budget, degraded-mode, retention, lifecycle, and incident-disablement failures. |
| API-AI-AC-010 | API contract supports future provider/vector/cache/model adapters through configuration and registry keys without version change. |
| API-AI-AC-011 | Streaming ask and conversation endpoints use SSE, governed event types, final completion metadata, cancellation/error events, audit, telemetry, and the same safety controls as non-streaming responses. |
| API-AI-AC-012 | Batch AI execution enforces item-level validation, authorization, budget reservation, audit, citations/confidence, partial success, idempotency, and rate-limit behavior. |
| API-AI-AC-013 | API responses expose tenant-safe rate-limit/retry headers including `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After` where applicable. |
| API-AI-AC-014 | API versioning/deprecation policy defines compatibility, breaking-change rules, deprecation notice, sunset handling, and migration expectations. |
| API-AI-AC-015 | Bulk knowledge APIs preserve single-source validation, approval, retention, legal-hold, audit, and shadow-index promotion controls with per-item results. |

---

# 18. Official and Primary References

- OpenAPI Specification v3.0.3:
  `https://spec.openapis.org/oas/v3.0.3.html`
- WHATWG HTML Living Standard - Server-sent events:
  `https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events`
- OWASP API Security Top 10 2023:
  `https://owasp.org/API-Security/editions/2023/en/0x11-t10/`
- RFC 9110 HTTP Semantics:
  `https://www.rfc-editor.org/rfc/rfc9110.html`
- RFC 8594 The Sunset HTTP Header Field:
  `https://www.rfc-editor.org/rfc/rfc8594.html`
- RFC 9457 Problem Details for HTTP APIs:
  `https://www.rfc-editor.org/rfc/rfc9457.html`
- RFC 9562 UUIDs:
  `https://www.rfc-editor.org/rfc/rfc9562.html`

References last validated: 2026-06-27.

---

# Approval

API Governance: Drafted by Codex 2026-06-27  
.NET Architect: ____  
Solution Architect: ____  
Security Architect: ____  
Data Governance/Privacy: ____  
Platform/Operations Architect: ____  
Product/AI Owner: ____  
Product Owner: Approved by Bhajan Lal 2026-06-27

(Status: Approved - owner approved 2026-06-27)
