# Test Plan - Governed AI Platform

Module: AI / Platform
Owner: QA Architect
Created Date: 2026-06-27
Version: 1.0
Status: Approved

> Doc 5 of 5 required before implementation. Companion docs:
> FEAT-AI-001, TECH-AI-001, DB-DESIGN-AI-001, UI-AI-001.
> No AI implementation may start until all five documents are Approved.

---

# 1. Purpose

This document defines the test strategy for the governed AI platform. The test plan covers
functional behavior, security, tenant isolation, RAG quality, AI evaluation, streaming,
batch operations, knowledge ingestion, cost governance, operations, retention, DR, and UI
accessibility.

---

# 2. Scope

In scope:

- AI conversations and stateless ask.
- Streaming AI responses.
- Batch AI operations.
- Conversation memory and reset.
- Knowledge source registration, validation, indexing, publication, bulk operations, and
  rollback.
- RAG retrieval, citations, confidence, refusal, and escalation.
- Evaluation and bundle promotion.
- Cost ledger, budget reservation, rate limits, and response headers.
- Semantic cache eligibility, invalidation, and disablement.
- Operational disablement, namespace rotation, DR exercises, and retention reconciliation.
- Tenant isolation, RBAC, ABAC, audit, and OpenAPI conformance.

Out of scope:

- Autonomous AI agents.
- AI-driven execution of HRMS business mutations.
- Non-AI feature-specific logic for leave, payroll, ATS, LMS, PMS, or service desk.

---

# 3. Quality Gates

| Gate | Minimum Requirement |
|---|---|
| Unit coverage | At least 85 percent line and branch coverage for AI module code. |
| Critical policy coverage | 95 percent coverage for tenant, authorization, policy, cache eligibility, and output validation services. |
| OpenAPI conformance | All implemented endpoints, schemas, headers, and errors match `OPENAPI-002-ai-platform-v1.yaml`. |
| Security tests | Zero known cross-tenant leakage, unauthorized citation, unsafe memory release, or prompt-injection bypass. |
| RAG quality | Approved threshold for groundedness, citation precision/recall, hallucination rate/severity, and refusal correctness. |
| Accessibility | WCAG 2.2 AA target for AI UI screens. |
| Performance | Meets approved latency, streaming, batch, ingestion, and DR targets. |

---

# 4. Test Environments

Required environments:

- Local developer test environment with fake providers and deterministic clocks.
- Integration environment with SQL Server RLS enabled.
- Qdrant test environment.
- Redis test environment.
- Event bus test environment.
- Staging environment with sandbox AI provider credentials where approved.
- Security/adversarial test environment with isolated tenant test data.

Tests must support deterministic fake LLM, fake embedding, and fake vector adapters so that
core policy behavior can be validated without paid provider dependency.

---

# 5. Test Data

Minimum tenant data:

- Tenant A and Tenant B.
- Employees with different roles, locations, departments, and manager scopes.
- HR Admin, Manager, Employee, AI Operator, Security Reviewer, Product Owner.
- Public HR policy, manager-only policy, HR-only policy, country-specific policy,
  expired policy, legal-hold policy, and deleted policy.
- Prompt-injection sample document.
- Conflicting source document.
- Dataset for RAG evaluation, hallucination testing, citation testing, and refusal testing.
- Provider outage, Qdrant outage, Redis outage, budget exhausted, and AI disabled scenarios.

---

# 6. Functional Test Scenarios

## 6.1 Ask and Conversation

- `Ask_AuthorizedPolicyQuestion_ReturnsCitedAnswer`
- `Ask_NoApprovedSource_ReturnsRefusalWithEscalation`
- `Ask_ConflictingSources_ReturnsSafeClarificationOrEscalation`
- `Ask_ExpiredPolicy_DoesNotUseExpiredSource`
- `Conversation_CreateThenMessage_PreservesPurposeBoundary`
- `Conversation_Reset_ClearsEligibleContextAndKeepsAudit`
- `Conversation_PurposeChanged_ReauthorizesOrRequiresNewConversation`

## 6.2 Streaming

- `AskStream_AuthorizedQuestion_EmitsStartedDeltaCitationConfidenceCompleted`
- `AskStream_CancelledByUser_EmitsCancelledAndAuditEvent`
- `AskStream_OutputFilterBlocksUnsafeDelta_DoesNotLeakUnsafeContent`
- `AskStream_ProviderFails_EmitsErrorWithoutPartialSensitiveLeak`
- `AskStream_FinalEvent_IncludesAuditReference`

## 6.3 Batch

- `Batch_MultipleValidItems_ReturnsOrderedPerItemSuccess`
- `Batch_OneUnauthorizedItem_ReturnsPartialSuccessWithoutLeakingData`
- `Batch_DuplicateIdempotencyKey_DoesNotDoubleCharge`
- `Batch_ExceedsMaxSize_ReturnsValidationError`
- `Batch_RateLimitedItem_ReturnsPerItemRateLimitResult`

## 6.4 Knowledge

- `Knowledge_RegisterSource_CreatesDraftSource`
- `Knowledge_ValidateCleanSource_PassesValidation`
- `Knowledge_ValidatePromptInjectionSource_BlocksPublication`
- `Knowledge_PublishValidatedSource_PromotesShadowIndex`
- `Knowledge_RollbackPublication_RestoresPreviousIndex`
- `Knowledge_BulkRegister_MixedItems_ReturnsPerItemResults`
- `Knowledge_BulkPublish_RequiresAllPerItemApprovals`

## 6.5 Evaluation and Bundle Governance

- `Evaluation_RunApprovedDataset_StoresMetricsAndEvidence`
- `Evaluation_HallucinationThresholdExceeded_BlocksPromotion`
- `Evaluation_ProviderBehaviorDriftDetected_RequiresRevalidation`
- `Bundle_PromoteWithoutApproval_Blocked`
- `Bundle_CanaryRollback_RestoresPreviousProductionBundle`
- `Approval_ExpiredApproval_BlocksProductionPromotion`

## 6.6 Cost, Rate Limits, and Headers

- `UsageLedger_ProviderCall_RecordsTokensCostAndAudit`
- `Budget_Exceeded_FailsClosedBeforeProviderCall`
- `RateLimit_Exceeded_ReturnsHeadersAndRetryAfter`
- `CacheHit_AvoidedProviderCall_RecordsCacheValue`
- `Batch_PerItemUsageLedger_RecordsEachItemSeparately`

## 6.7 Operations, DR, and Retention

- `Disablement_TenantScope_BlocksTenantAiOnly`
- `Disablement_GlobalEmergency_BlocksAllAiWithoutDeployment`
- `Disablement_ReleaseWithoutEvidence_BlockedWhenRequired`
- `NamespaceRotation_ApprovedRequest_RecordsAuditHistory`
- `DrExercise_RestoreVectorIndex_MeetsRpoRtoTarget`
- `Retention_DeletedSource_NotRetrievedByRag`
- `Retention_RestoredSource_BlockedUntilReconciliationPasses`

---

# 7. Security and Adversarial Tests

Required tests:

- Cross-tenant SQL RLS access attempts.
- Cross-tenant vector search attempts.
- Cross-tenant semantic cache key collision attempts.
- Prompt injection in user prompt.
- Prompt injection in source document.
- Sensitive-information disclosure attempts.
- System prompt extraction attempts.
- Provider credential exposure attempts.
- Unauthorized citation source access.
- Memory replay after role change.
- Memory replay after `TenantRoleMatrixChanged`.
- Purpose boundary bypass attempts.
- Batch data-mixing attempts.
- Streaming partial-output leakage attempts.

All security failures must block release.

---

# 8. API and OpenAPI Tests

Required:

- Contract tests generated from `OPENAPI-002-ai-platform-v1.yaml`.
- Response envelope validation.
- Error response validation.
- Pagination validation where applicable.
- Idempotency validation.
- Rate-limit header validation:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
  - `Retry-After`
- SSE content type and event sequence validation.
- API version path validation.
- Deprecation and sunset header behavior when future versions are introduced.

---

# 9. Performance Tests

Minimum performance scenarios:

- Synchronous ask P95 latency under approved target for cached and uncached paths.
- Streaming time-to-first-event under approved target.
- Batch request with maximum configured size.
- Knowledge ingestion for large policy document.
- Bulk knowledge operation with mixed success.
- Vector search latency under tenant filter.
- Redis unavailable fallback path.
- Qdrant unavailable degraded path.
- Provider timeout and retry behavior.
- Audit and usage ledger write under load.

Exact SLO values must align with AI-OPS-001 before implementation.

---

# 10. UI and Accessibility Tests

Required Playwright or equivalent tests:

- Copilot ask and stream.
- Stop/cancel streaming.
- Citation drawer open/close and authorization handling.
- Refusal and escalation state.
- Conversation reset.
- Knowledge source validation and publication flow.
- Bulk operation per-item results.
- Evaluation scorecard and promotion disabled/enabled states.
- Operations disablement creation and release.
- DR/retention evidence screens.
- Keyboard-only operation.
- Screen-reader labels for AI status, citations, confidence, and streaming updates.
- Responsive desktop/tablet/mobile layouts.

Accessibility:

- WCAG 2.2 AA target.
- Focus order.
- Non-color-only status indicators.
- Text overflow checks.
- Error message association with fields.

---

# 11. Data and Migration Tests

Required:

- Migration creates `AI` schema and all tables.
- Mandatory columns exist on tenant-scoped tables.
- RLS policies exist and are active.
- Tenant indexes exist.
- Unique constraints prevent duplicate source codes and invalid version states.
- Soft delete excludes records from active queries.
- Legal hold blocks purge.
- Retention reconciliation updates status and evidence.
- Rollback migrations are reviewed and documented where supported.

---

# 12. Test Automation

Automation layers:

- Unit tests: xUnit for .NET services and deterministic domain logic.
- Integration tests: API + SQL Server RLS + Redis + Qdrant test containers or approved
  equivalent.
- Contract tests: OpenAPI request/response validation.
- E2E tests: Playwright for UI flows.
- Security tests: adversarial prompt suites and tenant isolation suites.
- Performance tests: load tests for ask, stream, batch, ingestion, vector search, and audit.
- DR tests: restore, reconciliation, and evidence checks.

---

# 13. Exit Criteria

AI platform implementation cannot be accepted until:

- All approved acceptance criteria from the four companion docs pass.
- Unit and branch coverage meet project minimums.
- Critical policy services meet enhanced coverage target.
- OpenAPI contract tests pass.
- Security and tenant isolation tests pass with zero critical or high findings.
- RAG quality and hallucination gates meet approved thresholds.
- Accessibility tests meet WCAG 2.2 AA target.
- Performance and degraded-mode tests meet approved targets.
- DR and retention reconciliation tests pass.
- Product Owner, Security, QA, Data Governance, and Operations sign-off is complete.

---

# 14. Official and Primary References

- OpenAPI Specification v3.0.3:
  `https://spec.openapis.org/oas/v3.0.3.html`
- WHATWG Server-Sent Events:
  `https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events`
- OWASP API Security Top 10 2023:
  `https://owasp.org/API-Security/editions/2023/en/0x11-t10/`
- OWASP Top 10 for LLM and Generative AI Applications 2025:
  `https://genai.owasp.org/llm-top-10/`
- NIST AI Risk Management Framework:
  `https://www.nist.gov/itl/ai-risk-management-framework`
- WCAG 2.2:
  `https://www.w3.org/TR/WCAG22/`

References last validated: 2026-06-27.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-27  
QA Architect: Approved as part of owner-approved AI implementation package 2026-06-27  
Solution Architect: Approved as part of owner-approved AI implementation package 2026-06-27  
Security Architect: Approved as part of owner-approved AI implementation package 2026-06-27  
Data Governance/Privacy: Approved as part of owner-approved AI implementation package 2026-06-27  
Platform/Operations Architect: Approved as part of owner-approved AI implementation package 2026-06-27

(Status: Approved - owner approved 2026-06-27)
