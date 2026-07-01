# Module Backlog - Phased Product Delivery

Document Owner: Product Owner (Agent 2)
Created Date: 2026-06-16
Version: 1.0
Status: Draft

> Purpose: capture the full-product module backlog identified from Phase 1 market
> research refresh and organize it into phased delivery. This is not a build permission.
> Each module still needs the required 5-doc set before development.

---

## 1. Delivery Principle

Everything is delivered in phases. No module is built "in one go." Every future module
must be added through platform extension contracts so existing core modules remain
closed for modification.

Future modules must reuse:

- Tenant catalog and feature flags
- Identity, RBAC, ABAC, and audit
- Effective-dated core records
- Workflow Studio
- Rule Engine
- Configuration-as-Data
- Dynamic forms
- Reports and analytics
- Notifications
- Search
- AI/RAG
- Event bus
- Provider abstraction
- Public APIs and OpenAPI contracts

---

## 2. Phase Backlog

| Phase | Module / Feature | Priority | Notes |
|---|---|---|---|
| Phase 7A | Tenant catalog + RLS | Must | Foundation for isolation and placement |
| Phase 7A | Identity + RBAC/ABAC | Must | Foundation for every module |
| Phase 7A | Effective Dating / bitemporal core | Must | Foundation for employee, org, salary, policy, and payroll history |
| Phase 7A | Audit / Time Machine | Must | Tamper-resistant traceability for every business action |
| Phase 7A | Event Bus + Outbox | Must | Decouples modules and enables event-driven workflows |
| Phase 7A | Rule Engine | Must | No hardcoded business rules |
| Phase 7A | Workflow Studio | Must | Core differentiator and shared approval/process engine |
| Phase 7A | Configuration-as-Data | Must | Workflows, rules, forms, reports, navigation, permissions, and notifications are metadata-driven |
| Phase 7A | Core HR + ESS | Must | Employee master and self-service base |
| Phase 7A | Leave | Must | First configurable workflow proof |
| Phase 7A | Attendance + 1 connector | Must | Device framework proof |
| Phase 7A | Payroll + India compliance | Must | Trust milestone |
| Phase 7A | Standard reports | Must | Operational and statutory reporting |
| Phase 7B | White-label | Should | Tenant/reseller readiness |
| Phase 7B | SSO/OIDC | Should | Enterprise readiness |
| Phase 7B | Config sandbox -> production | Should | Safe customer self-configuration |
| Phase 7B | Document/letter/e-sign | Should | Offer letters, salary letters, policy acknowledgements |
| Phase 7B | HR service desk | Should | Table-stakes employee request handling |
| Phase 7B | Onboarding/offboarding basics | Should | Task templates, documents, IT/manager handoffs |
| Phase 7B | Provider/integration health center | Should | Device, email/SMS/push, webhook health |
| Phase 7B | Implementation wizard | Should | Setup checklist, templates, migration validation |
| Phase 7C | RAG HR assistant | Should | Grounded answers with citations |
| Phase 7C | Richer reporting/BI | Should | Saved views, scheduled reports, semantic layer |
| Phase 7C | Compliance intelligence | Should | Deadline alerts, predictive checks |
| Phase 7C | Mobile reliability hardening | Should | Offline/retry, telemetry, clear sync status |
| Phase 7C | Attendance connector expansion | Should | Connector #2-3 after framework proof |
| Phase 7D | Recruitment/ATS | Next | Hiring pipeline through onboarding |
| Phase 7D | Advanced onboarding | Next | Zero-touch onboarding and provisioning |
| Phase 7D | Performance/goals/OKRs | Next | Review cycles, goals, calibration |
| Phase 7D | LMS/learning | Next | Training assignment and compliance learning |
| Phase 7D | Engagement/surveys/recognition | Next | Pulse, eNPS, recognition |
| Phase 7A | Shift Foundation | Must | Shift definitions, effective-dated employee shift assignment, shift override, attendance/payroll impact |
| Phase 7E | Advanced roster/workforce scheduling | Next | Shift swaps, auto scheduling, capacity planning, demand planning |
| Phase 7E | Expense/travel/reimbursements | Next | Claims, approvals, payroll integration |
| Phase 7E | Asset and IT requests | Next | Allocation, return, maintenance |
| Phase 7E | Compensation review | Next | Salary revision cycles, merit matrix, letters |
| Phase 7E | Multi-entity org graph UI | Next | Parent/subsidiary/entity visibility |
| Later phases | Workforce planning/forecasting | Later | Scenario planning and budget forecasting |
| Later phases | Integration marketplace | Later | Connector marketplace and app ecosystem |
| Later phases | Contingent workforce | Later | Contractors, interns, vendors, freelancers |
| Later phases | Multi-country payroll plugins | Later | Country-specific compliance packs |
| Later phases | Advanced manager intelligence | Later | Risk, workload, and planning insights |

---

## 3. Required 5-Doc Set Per Module

Each module must have these approved before development:

- Business Requirements
- Technical Design
- Database Design
- UI Design
- Test Cases

Owner approval is required before any module enters development.

---

## 4. Extension Acceptance Checklist

A future module is ready for architecture review only when it defines:

- Module manifest
- Feature flags and entitlements
- Tenant isolation model
- RBAC/ABAC permissions
- Audit events
- API/OpenAPI contracts
- Domain events
- Workflow/rule/form/report metadata
- UI navigation/widget metadata
- Search/report/AI hooks
- Provider adapters, if applicable
- Data migration and rollback plan

---

## 5. Phase Dependency Map

| Gate | Must be completed before | Reason |
|---|---|---|
| Tenant Catalog + RLS | All modules | Tenant isolation, data placement, feature entitlement |
| Identity + RBAC/ABAC | All modules | Authentication, authorization, scoped access |
| Effective Dating | Core HR, Leave, Attendance, Payroll, Reporting | Historical accuracy and as-of calculations |
| Audit / Time Machine | All mutating modules | Traceability, investigation, compliance evidence |
| Event Bus + Outbox | Leave, Attendance, Payroll, Reporting, Notifications | Decoupled module communication |
| Rule Engine | Leave, Attendance, Payroll, Workflow, Configuration | No hardcoded business rules |
| Workflow Studio | ESS, Leave, Attendance, Payroll, Rule/Config publishing | Approval, delegation, SLA, escalation |
| Configuration-as-Data | All current and future modules | Open for extension without core code changes |
| Core HR + ESS | Leave, Attendance, Payroll, Reporting | Employee master and organization source |
| Leave | Payroll and Reports | Leave balance, unpaid leave, absence evidence |
| Attendance | Payroll and Reports | Payable days, absence, regularization evidence |
| Payroll + India Compliance | Reports and Release Gate | Trust milestone and statutory correctness |
| Standard Reports | Release Gate | Operational visibility and customer acceptance |

No downstream module may enter development until its upstream gate documents are Approved.

---

## Approval

Product Owner: ____ · Solution Architect: ____ · Database Architect: ____ ·
Security Architect: ____ · QA Architect: ____  (Status: Draft -> Approved)
