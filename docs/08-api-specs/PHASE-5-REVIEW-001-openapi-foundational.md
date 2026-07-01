# Phase 5 Review - Foundational OpenAPI Package

Document Owner: API Governance Expert / .NET Architect
Review Date: 2026-06-22
Version: 1.0
Status: Approved
Approved By: Bhajan Lal (Product Owner)
Approved Date: 2026-06-22

---

## Purpose

Prepare the Phase 5 API Design package for owner review and approval.

This package translates the approved Phase 2 product scope, Phase 3 architecture, and
Phase 4 UI alignment into versioned REST/OpenAPI contracts.

---

## Documents in Scope

| Document | Status |
|---|---|
| `docs/08-api-specs/API-SPEC-001-foundational.md` | Approved |
| `docs/08-api-specs/OPENAPI-001-foundational-v1.yaml` | Approved |

---

## API Scope Covered

The foundational OpenAPI package covers:

- Auth and current user context.
- Identity roles and permissions.
- Tenant profile, feature flags, branding, and config promotion.
- Employee directory, employee details, effective-dated employee updates, and org chart.
- Leave balances, leave types, leave requests, and withdrawal.
- Workflow tasks, approvals, workflow definitions, validation, publish, and instances.
- Rule sets, validation, test execution, and publish.
- Provider registry, tenant provider configuration, test connection, activation, and health.
- Global search.
- Notifications.
- Audit / Time Machine change history.

---

## Explicitly Out of Scope

These require separate OpenAPI files after their own phase or feature gates:

- Attendance APIs.
- Payroll and India compliance APIs.
- Reporting/BI advanced APIs.
- AI/RAG APIs, until Phase 6 AI Strategy and ADR-019 are approved.
- Later-phase modules such as ATS, LMS, PMS, service desk, assets, travel, and expense.

---

## Governance Checks

| Check | Result |
|---|---|
| Base path uses `/api/v1` | Pass |
| REST naming used, no verb-style endpoint names | Pass |
| JWT security defined | Pass |
| Tenant context assumed server-side, not trusted from request body | Pass |
| RBAC/ABAC permissions documented through `x-permissions` / notes | Pass |
| Idempotency header required on critical mutating endpoints | Pass |
| Correlation ID documented | Pass |
| Pagination used on list endpoints | Pass |
| Audit/domain events noted through extensions | Pass |
| Provider Management aligned to ADR-027 | Pass |
| AI APIs excluded until Phase 6 | Pass |

---

## Validation Note

Structural checks were performed locally: the OpenAPI file has required top-level sections,
44 documented paths, 53 operations, components, security schemes, no AI paths, and no tab
characters.

Full semantic OpenAPI linting should be run with a dedicated OpenAPI validator once a
validator package/tool is added to the workspace.

---

## Approval

.NET Architect: ____  
API Governance: ____  
Solution Architect: ____  
Security Architect: ____  
Product Owner: Bhajan Lal · Approved 2026-06-22
