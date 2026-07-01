# UI Design - Governed AI Platform

Module: AI / Platform
Owner: UI Architect
Created Date: 2026-06-27
Version: 1.0
Status: Approved

> Doc 4 of 5 required before implementation. Companion docs:
> FEAT-AI-001, TECH-AI-001, DB-DESIGN-AI-001, TEST-AI-001.
> No AI implementation may start until all five documents are Approved.

---

# 1. Purpose

This document defines the user-facing and administrator-facing AI screens required for the
governed AI platform. The design must feel like an enterprise HRMS operations product, not
a marketing page or experimental chatbot.

The AI experience must make governance visible in practical ways: citations, confidence,
source freshness, refusal reasons, user permissions, audit references, and operational
state.

---

# 2. Design Inputs

Required inputs:

- `DESIGN-SYSTEM-001-foundations.md`
- `DESIGN-SPEC-002-people-ops-platform.md`
- `FEAT-AI-001-business-requirements.md`
- `TECH-AI-001-ai-platform-technical-design.md`
- `API-SPEC-002-ai-platform-v1.md`
- `OPENAPI-002-ai-platform-v1.yaml`
- `AI-OPS-001-enterprise-ai-operations.md`
- `SEC-AI-001-ai-security-extension.md`

---

# 3. Personas

| Persona | Primary Need |
|---|---|
| Employee | Ask policy questions and understand answers quickly. |
| Manager | Get team-scope answers without unauthorized data exposure. |
| HR Administrator | Manage knowledge sources and AI answer quality. |
| AI Governance Reviewer | Review evaluations, bundle approvals, and promotion evidence. |
| Platform Operator | Monitor health, disable unsafe AI paths, and manage recovery. |
| Tenant Administrator | Configure allowed AI use cases and provider settings. |

---

# 4. Navigation

AI surfaces appear in two places:

1. Copilot panel available from approved employee, manager, and admin work areas.
2. AI Administration area under Platform Administration.

AI Administration sections:

- Knowledge
- Evaluations
- Bundles
- Operations
- Cost and Usage
- DR and Retention
- Settings

Access to each section is permission-gated.

---

# 5. Screen A - AI Copilot Panel

Purpose: let users ask authorized HR questions and receive cited AI answers.

Users:

- Employee
- Manager
- HR Administrator

APIs:

- `POST /api/v1/ai/ask`
- `POST /api/v1/ai/ask/stream`
- `POST /api/v1/ai/conversations`
- `POST /api/v1/ai/conversations/{conversationId}/messages`
- `POST /api/v1/ai/conversations/{conversationId}/messages/stream`
- `POST /api/v1/ai/conversations/{conversationId}/reset`

Required UI elements:

- Purpose selector when more than one approved purpose is available.
- Message input with clear submit and stop controls.
- Streaming answer area with progressive text.
- Stop/cancel button for active streaming.
- Citation chips linked to source drawer.
- Confidence indicator.
- Refusal/escalation notice when answer cannot be safely provided.
- Audit reference after completion where user role permits viewing it.
- Conversation reset action.

States:

- Loading.
- Streaming.
- Completed.
- Cancelled.
- Refused.
- Escalated to HR.
- No permission.
- AI disabled for tenant/use case.
- Provider unavailable.

Rules:

- The UI must not display hidden prompt content, provider secrets, raw tool output, or raw
  vector payloads.
- The user must be able to distinguish AI-generated text from system or HR-authored text.
- Citations must stay visible or reachable after answer completion.

---

# 6. Screen B - Citation and Source Drawer

Purpose: allow users to inspect why an AI answer was given.

Required UI elements:

- Source title.
- Source version.
- Effective date.
- Page or section anchor.
- Last validated/publication date.
- Classification label where allowed.
- Excerpt limited to authorized content.
- Open source action where permission allows.

States:

- Citation available.
- Source no longer available.
- User no longer authorized.
- Source superseded by newer version.
- Source under legal hold or retention restriction.

Rules:

- Source drawer must re-check authorization before display.
- Source drawer cannot reveal citations that were filtered from the answer.

---

# 7. Screen C - Knowledge Management

Purpose: let authorized HR admins manage AI knowledge sources.

Users:

- HR Administrator
- Knowledge Steward
- Tenant Administrator

APIs:

- `GET /api/v1/ai/knowledge/sources`
- `POST /api/v1/ai/knowledge/sources`
- `POST /api/v1/ai/knowledge/sources/bulk`
- `POST /api/v1/ai/knowledge/sources/{sourceId}/versions`
- `POST /api/v1/ai/knowledge/sources/{sourceId}/versions/{versionId}/validate`
- `POST /api/v1/ai/knowledge/sources/{sourceId}/versions/{versionId}/publish`
- bulk validation, publication, archival, and metadata endpoints

Required UI elements:

- Source list with status, owner, classification, locale, effective date, validation status.
- Filters for source type, status, owner, and classification.
- Source detail panel with versions and publication history.
- Upload/link source version action.
- Bulk operation toolbar for approved bulk actions.
- Validation result panel with actionable errors.
- Shadow-index status and publication readiness.
- Rollback action where permitted.

States:

- Empty source catalog.
- Uploading.
- Validating.
- Validation failed.
- Shadow index building.
- Ready for publication.
- Published.
- Archived.
- Rollback available.

Rules:

- Bulk actions require confirmation and show per-item results.
- Publication requires approval state and validation evidence.
- The UI must clearly separate Draft, Validated, Published, Archived, Deprecated, and
  Retired states.

---

# 8. Screen D - Evaluation and Bundle Governance

Purpose: review AI bundle readiness before canary or production promotion.

Users:

- Product Owner
- AI Governance Reviewer
- Security Reviewer
- Operations Reviewer

APIs:

- `GET /api/v1/ai/evaluations/runs`
- `POST /api/v1/ai/evaluations/runs`
- `GET /api/v1/ai/bundles`
- `POST /api/v1/ai/bundles/{bundleId}/promote`

Required UI elements:

- Bundle lifecycle stage: Draft, Evaluation, Approved, Canary, Production, Deprecated,
  Retired.
- Bundle composition: model, prompt, safety, memory, cache, index, evaluation dataset.
- Evaluation scorecard.
- Hallucination rate and severity.
- Citation quality.
- Refusal correctness.
- Reviewer agreement and consistency.
- Provider behavior drift signal.
- Approval expiry date and reason.
- Rollback target.
- Promotion decision panel.

States:

- Evaluation not started.
- Evaluation running.
- Failed gate.
- Approved for canary.
- Canary active.
- Production active.
- Rollback required.

Rules:

- Promotion controls are disabled until required approvals and evidence exist.
- Risk owner must be visible for higher-risk use cases.

---

# 9. Screen E - AI Operations Console

Purpose: help operators keep AI safe and available.

Users:

- Platform Operator
- SRE
- Security Operator

APIs:

- `GET /api/v1/ai/operations/status`
- `POST /api/v1/ai/operations/disablements`
- `DELETE /api/v1/ai/operations/disablements/{disablementId}`
- `POST /api/v1/ai/cache/namespaces/{namespaceId}/rotate`

Required UI elements:

- Overall AI health summary.
- Provider status.
- Qdrant/vector status.
- Redis/cache status.
- Evaluation status.
- Budget/rate-limit status.
- Disablement list.
- Disablement create form with scope, reason, severity, expiry, and evidence.
- Namespace rotation history and evidence.
- Link to relevant runbook.

States:

- Healthy.
- Degraded.
- Disabled by policy.
- Emergency disabled.
- Incident active.
- Recovery in progress.

Rules:

- Disablement changes require reason and audit evidence.
- Emergency disablement must be fast, but still audited.
- Release from disablement must show validation evidence where policy requires it.

---

# 10. Screen F - Cost and Usage

Purpose: show product and operations teams how AI is being used and controlled.

Users:

- Product Owner
- Tenant Administrator
- Finance Operator
- Platform Operator

Required UI elements:

- AI adoption rate.
- Successful AI resolution rate.
- Human escalation rate.
- Cost per successful AI request.
- Token and provider usage.
- Cache avoided provider calls.
- Budget consumption.
- Rate-limit events.
- Tenant/use-case filters.

Rules:

- Financial values must be permission-gated.
- Usage dashboards cannot expose prompt content or employee-sensitive details.

---

# 11. Screen G - DR and Retention Status

Purpose: provide operational evidence for disaster recovery and governed deletion.

Users:

- Platform Operator
- Data Governance
- Security Reviewer

APIs:

- `GET /api/v1/ai/dr/exercises`
- `POST /api/v1/ai/dr/exercises`
- `GET /api/v1/ai/retention/reconciliation-jobs`
- `POST /api/v1/ai/retention/reconciliation-jobs`

Required UI elements:

- DR exercise list.
- RPO/RTO target and result.
- Pass/fail status.
- Evidence link.
- Retention reconciliation job list.
- Deleted, held, blocked, and restored item counts.
- Reconciliation failure detail.

Rules:

- Restored AI content remains unavailable until reconciliation passes.
- Legal hold status must be visible to authorized reviewers only.

---

# 12. Screen H - AI Settings

Purpose: tenant-level configuration entry point for approved AI capabilities.

Users:

- Tenant Administrator
- Platform Administrator

Required UI elements:

- Enabled AI use cases.
- Provider adapter selection where tenant is allowed to choose.
- Model assignment summary.
- Memory mode.
- Cache eligibility summary.
- Knowledge connector summary.
- Rate-limit and budget policy references.
- Feature flags.

Rules:

- Settings are configuration references, not hardcoded behavior.
- Provider changes must route through evaluation and approval where required.

---

# 13. Accessibility and Usability

The AI UI must target WCAG 2.2 AA.

Required:

- Keyboard operation for ask, stop, reset, source drawer, tabs, filters, and tables.
- Clear focus state.
- Screen-reader labels for confidence, citations, and AI status.
- Non-color-only state indicators.
- Loading and streaming states announced politely.
- Responsive layouts for desktop, tablet, and mobile.
- No text overflow in buttons, tables, badges, or status chips.
- Localized labels and date/time formats.

---

# 14. Audit and Trust UX

The UI must help users trust the system without exposing internal secrets.

Show:

- Citation availability.
- Confidence.
- Source freshness.
- Refusal reason.
- Escalation path.
- Last updated/publication state.
- Audit reference where authorized.

Do not show:

- Hidden system prompts.
- Provider credentials.
- Raw provider traces.
- Raw vectors.
- Unauthorized source excerpts.
- Cross-tenant metadata.

---

# 15. Acceptance Criteria

| ID | Criterion |
|---|---|
| UI-AI-AC-001 | Copilot supports synchronous and streaming answers with stop/cancel, citations, confidence, refusal, and escalation states. |
| UI-AI-AC-002 | Citation drawer rechecks authorization and displays only permitted source evidence. |
| UI-AI-AC-003 | Knowledge Management supports source versions, validation results, publication readiness, rollback, and governed bulk operations. |
| UI-AI-AC-004 | Evaluation and Bundle Governance displays lifecycle stage, scorecard, approvals, expiry, risk owner, and rollback target. |
| UI-AI-AC-005 | Operations Console supports scoped emergency disablement, release evidence, namespace rotation history, and runbook links. |
| UI-AI-AC-006 | Cost and Usage dashboard shows adoption, escalation, resolution, cache value, token usage, and budget status without exposing sensitive content. |
| UI-AI-AC-007 | DR and Retention Status shows recovery and reconciliation evidence required by governance. |
| UI-AI-AC-008 | AI Settings are permission-gated and configuration-driven. |
| UI-AI-AC-009 | All AI screens meet WCAG 2.2 AA target and responsive layout requirements. |
| UI-AI-AC-010 | UI never exposes system prompts, provider secrets, raw vectors, unauthorized citations, or cross-tenant data. |

---

# 16. Official and Primary References

- WCAG 2.2:
  `https://www.w3.org/TR/WCAG22/`
- WHATWG Server-Sent Events:
  `https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events`
- OpenAPI Specification v3.0.3:
  `https://spec.openapis.org/oas/v3.0.3.html`
- NIST AI Risk Management Framework:
  `https://www.nist.gov/itl/ai-risk-management-framework`

References last validated: 2026-06-27.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-27  
UI Architect: Approved as part of owner-approved AI implementation package 2026-06-27  
Accessibility Reviewer: Approved as part of owner-approved AI implementation package 2026-06-27  
Security Architect: Approved as part of owner-approved AI implementation package 2026-06-27  
Solution Architect: Approved as part of owner-approved AI implementation package 2026-06-27

(Status: Approved - owner approved 2026-06-27)
