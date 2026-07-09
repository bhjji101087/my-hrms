# Product Requirements Document (PRD)

## Document Information

- **Product Name:** Enterprise AI-Driven HRMS Platform (working title)
- **Module:** Platform Phased Delivery
- **Version:** 1.1
- **Author:** Product Owner (Agent 2)
- **Created Date:** 2026-06-14
- **Status:** Approved

> Built on approved Phase 1 inputs: `docs/01-market-research/competitor-analysis-india.md`
> (v1.2) and `docs/03-gap-analysis/competitor-gap-analysis.md` (v1.0). This PRD defines
> the phased product scope; module-level detail belongs in per-feature specs.
>
> **v1.1 change:** incorporated `docs/05-architecture/ARCH-REVIEW-001` §9. Phase 7A
> must start with the full platform foundation group, not directly with business modules:
> **Tenant Catalog + RLS (FR-015), Identity + RBAC/ABAC (FR-002), Effective-dating/
> bitemporal core (FR-014), Audit/Time Machine (FR-008), Event Bus (FR-009), Rule Engine
> (FR-013), Workflow Engine/Studio (FR-007), and Configuration-as-Data**. Leave,
> Attendance, Payroll, Compliance, and future modules depend on these foundations.
> Delegation/proxy approvals added to FR-007 scope.
>
> 2026-06-16 refresh: added missing modules/features from Phase 1 market review and
> organized them into phased delivery. Approved by the owner on 2026-06-17.

---

# Business Objective

Win the **underserved 50–2,000-employee Indian mid-market** with an HRMS whose
differentiators are **true no-code configurability** and **reliability**, not module
count. The gap analysis validated that customers churn on *friction* (support, the
configuration ceiling) — not missing features. The first development phase must prove we remove that
friction while matching greytHR-grade India payroll & statutory compliance.

# Business Value

* **Lower total cost of change** — HR configures workflows/forms/policies without vendor
  tickets (attacks validated pain P2, the #1 differentiator).
* **Trust** — accurate payroll/compliance + zero-regression releases + responsive support
  (attacks pains P1, P3, P5).
* **Expansion-ready** — multi-tenant, white-label, and a country-plugin path (UAE/USA/UK)
  without core changes.
* **AI leverage** — an affordable RAG HR assistant for a tier that lacks deep AI today.

# Stakeholders

* HR Admin / HR Operations (primary buyer & power user)
* Payroll Team
* People Manager (approver, team insights)
* Employee (ESS / mobile)
* Tenant Admin (configuration, branding, RBAC/ABAC)
* Platform Owner / Reseller (white-label)

# User Personas

## Persona 1 — Priya, HR Operations Lead (mid-market, ~600 employees)
- **Role:** Owns payroll runs, leave/attendance policy, statutory filings.
- **Goals:** Run error-free monthly payroll; change a policy without raising a vendor
  ticket; pass PF/ESI/PT/TDS audits.
- **Pain Points:** Current tool needs support tickets for small config changes; FBP &
  mid-cycle CTC revisions are manual; slow support during payroll week.

## Persona 2 — Rohan, Engineering Manager (approver)
- **Role:** Approves leave, regularisations; needs team visibility.
- **Goals:** Fast approvals on mobile; see who's on leave / attendance exceptions.
- **Pain Points:** HRMS built for HR, not managers; clunky mobile app.

## Persona 3 — Anita, Employee
- **Role:** Applies leave, downloads payslips, asks policy questions.
- **Goals:** Self-serve answers ("how many leaves left?", "maternity policy?"), reliable
  mobile experience.
- **Pain Points:** Logs in only when forced; emails HR for policy answers.

## Persona 4 — Sameer, Tenant Admin
- **Role:** Configures the platform for the company.
- **Goals:** Build approval workflows, custom fields, branding, roles — without code.
- **Pain Points:** "No-code" tools that hit a wall and require the vendor.

---

# Functional Requirements

Priority uses MoSCoW. **Must** = required for the first development phase. Acceptance criteria are summarised; each FR gets a
full Feature Spec (`docs/19-templates/FEATURE_REQUIREMENTS_TEMPLATE.md`) before build.

> **FR numbering is not the implementation sequence.** FR numbers are stable requirement
> identifiers. Delivery order is controlled by the roadmap, dependency graph, phase gate,
> and sprint plan. For example, FR-015 appears last in this list because it was added as
> a later foundational requirement, but it is built first because Tenant Catalog + RLS
> must exist before tenant-safe modules can be developed.

### FR-001 — Multi-tenant foundation & tenant isolation
- **Priority:** Must
- **Description:** Every entity is tenant-scoped; no cross-tenant access; per-tenant
  module/feature enablement via flags.
- **Acceptance Criteria:** A user in Tenant A can never read/write Tenant B data
  (verified by security tests); modules can be toggled per tenant without deployment.

### FR-002 — Identity, AuthN & RBAC + ABAC
- **Priority:** Must
- **Description:** JWT auth (Entra ID/Google/Okta later); role-based + attribute-based
  access (e.g. "manager sees only their department"). Includes branch/office scope
  decisions for complete tenant admins, branch admins, managers, payroll, HR, auditors,
  jobs, reports, exports, workflows, and AI retrieval.
- **Acceptance Criteria:** Access decisions honour both role and attributes (department/
  location/BU/branch/office); every denied case is auditable.

### FR-003 — Core HR & Employee Master + ESS
- **Priority:** Must
- **Description:** Employee records, org/department/location structure, documents,
  branch/office assignment, self-service profile.
- **Acceptance Criteria:** CRUD with audit trail; soft delete; ESS edit with approval.

### FR-004 — Leave Management (configurable)
- **Priority:** Must
- **Description:** Leave types, balances, accrual rules, holiday calendars; multi-level
  approval via the workflow engine (no hardcoded rules).
- **Acceptance Criteria:** A new leave type + approval chain can be created by a Tenant
  Admin **with no code/deploy**; balances and carry-forward compute correctly.

### FR-005 — Attendance & Time + device connector framework
- **Priority:** Must (manual/web/mobile + ≥1 biometric connector); Should (full marketplace)
- **Description:** Attendance via web/mobile/manual/CSV; plug-and-play connector for at
  least one biometric vendor (ZKTeco or eSSL) as the framework proof. Includes Phase 7A
  Shift Foundation: shift definitions, effective-dated employee shift assignment, shift
  override, and shift-aware attendance/payroll impact.
- **Acceptance Criteria:** Admin adds a device (vendor → IP → save) with no custom code;
  punches sync and feed payroll; attendance summary uses the employee's effective shift
  for the attendance date.

### FR-006 — Payroll + India statutory compliance
- **Priority:** Must
- **Description:** Salary structures/components, formula engine, payroll run, payslips;
  PF, ESI, PT (state-wise), LWF, TDS, Form 16; **FBP and mid-cycle CTC revisions** (the
  validated payroll-depth gap P3).
- **Acceptance Criteria:** A correct monthly run for a sample tenant produces compliant
  payslips and statutory outputs; FBP declaration and a mid-cycle revision process
  **without manual workarounds**.

### FR-007 — Workflow Studio (no-code engine) ⭐ core differentiator
- **Priority:** Must
- **Description:** Visual builder for approval chains, conditional logic, dynamic forms/
  custom fields, and notifications — reusable across leave, attendance, expense, etc.
  Includes **delegation / proxy approvals** (act-on-behalf during approver absence) and
  SLA-driven escalations. Running instances pin their definition version (no silent
  re-point). See ARCH-REVIEW-001 §2; engine choice in ADR-010.
- **Acceptance Criteria:** A non-technical admin builds a multi-level conditional approval
  (e.g. "sick leave > 5 days → HR approval") **without code**; it executes correctly and
  is versioned/auditable; an absent approver's tasks route to their delegate; SLA breach
  triggers the configured escalation.

### FR-008 — Audit logging & "time machine" history
- **Priority:** Must
- **Description:** Every create/update/delete/login/approval captured with before/after
  values, actor, time, reason.
- **Acceptance Criteria:** Any record's change history is viewable (old→new, who, when).

### FR-009 — Notifications & event bus
- **Priority:** Must
- **Description:** Event-driven notifications (email/in-app); events like LeaveApproved,
  PayrollProcessed published for downstream consumers.
- **Acceptance Criteria:** Approving leave emits an event that triggers notification +
  audit without synchronous coupling.

### FR-010 — White-label & per-tenant branding
- **Priority:** Should
- **Description:** Logo, theme/colours, custom domain, email templates per tenant.
- **Acceptance Criteria:** Two tenants render distinct branding from configuration only.

### FR-011 — Affordable RAG HR Assistant
- **Priority:** Should (later phase; thin slice in Phase 7A if capacity allows)
- **Description:** Employees ask NL questions answered from tenant policies/handbook via
  RAG (e.g. leave balance, maternity policy).
- **Acceptance Criteria:** Answers cite the source policy doc; no cross-tenant leakage.

### FR-012 — Reporting & exports
- **Priority:** Should (standard reports Must; NL/AI report builder = Could/later)
- **Description:** Standard payroll/leave/attendance reports + CSV/Excel export; ad-hoc
  builder later.
- **Acceptance Criteria:** Core statutory/operational reports available with filters.

### FR-013 — Business Rule Engine (core) ⭐ foundation
- **Priority:** Must
- **Description:** Generic, rules-as-data engine consumed by Leave, Payroll, Workflow
  routing, and form validation. Rules are versioned, effective-dated, and evaluated via a
  safe expression language (no arbitrary code). See ARCH-REVIEW-001 §3; model in ADR-011.
- **Acceptance Criteria:** A statutory/leave/payroll rule (e.g. a PT slab or accrual rule)
  is defined as data, versioned, effective-dated, and produces correct outcomes with no
  code deploy; published rulesets are immutable; a mid-cycle change creates a new
  effective-dated version rather than editing the live one.

### FR-014 — Effective-dated / bitemporal core ⭐ foundation
- **Priority:** Must
- **Description:** Core entities (employee, org, salary, policy assignments) support
  past-dated corrections and future-dated changes with full history and "as-of" queries.
  See ARCH-REVIEW-001 §1C; strategy in ADR-007.
- **Acceptance Criteria:** A future-dated salary change applies automatically on its
  effective date; a back-dated correction is recorded without losing prior history; an
  "as-of <date>" query returns the values that were valid then.

### FR-015 — Tenant Catalog + Row-Level Security ⭐ foundation
- **Priority:** Must
- **Description:** A tenant catalog maps each tenant to its placement (pool/shard, region)
  and entitlements; all data access flows through a tenant-context resolver with a
  repository-injected tenant predicate (ADR-037) **and** SQL Server Row-Level Security as
  defense-in-depth. Enables future
  dedicated-DB / data-residency placement without code change. See ARCH-REVIEW-001 §4;
  model in ADR-005. Includes explicit Branch / Office Hierarchy and Scoped Administration
  inside a tenant. (Extends FR-001.)
- **Acceptance Criteria:** A deliberately missing tenant filter in code is still blocked
  by RLS (verified by test); a tenant can be repointed to a dedicated DB via catalog
  configuration with no application code change; tenant admins can administer all
  branches/offices while branch admins are restricted to assigned branch/office scope.

## Full-Product Module Scope by Phase

The product is not delivered in one go. Phase 7A proves the foundations and highest-risk
operational flows. Later modules must plug into the platform engines without changing
core logic.

| Phase | Module scope | Why this phase |
|---|---|---|
| Phase 7A | Platform foundation group first: Tenant Catalog + RLS, Branch / Office Hierarchy and Scoped Administration, Identity + RBAC/ABAC, Effective Dating, Audit/Time Machine, Event Bus, Rule Engine, Workflow Studio, Configuration-as-Data; then Core HR, Leave, Attendance with Shift Foundation, Payroll/India Compliance, standard reports | Foundation and trust layer; highest dependency and compliance risk |
| Phase 7B | White-label, SSO/OIDC, notification preferences, config sandbox->promotion, document/letter/e-sign, HR service desk, onboarding/offboarding basics, provider/integration health, implementation wizard | Converts platform into deployable customer experience and reduces support/setup friction |
| Phase 7C | RAG HR assistant, richer reports/BI, compliance intelligence, mobile reliability hardening, attendance connector expansion, scheduled/saved reports | Improves intelligence, reliability, and self-service after core operations are stable |
| Phase 7D | Recruitment/ATS, advanced onboarding, performance/goals/OKRs, LMS, engagement/surveys/recognition | Adds talent-suite breadth once core employee/payroll data is stable |
| Phase 7E | Advanced roster/workforce scheduling, shift swap, workforce demand planning, expense/travel/reimbursements, asset and IT requests, compensation review, multi-entity org graph UI | Adds workforce operations and finance-adjacent workflows |
| Later phases | Workforce planning/forecasting, integration marketplace, contingent workforce, multi-country payroll plugins, advanced manager intelligence | Enterprise expansion and ecosystem capabilities |

### Missing Modules Added to Product Scope

- Recruitment / ATS
- Onboarding and offboarding / exit / FNF
- Performance / goals / OKRs
- Learning / LMS
- Engagement / pulse surveys / recognition
- HR service desk / case management
- Document management / letters / e-signature
- Branch / Office Hierarchy and Scoped Administration
- Shift Foundation in Phase 7A; advanced roster/workforce scheduling in Phase 7E
- Expense / travel / reimbursements
- Asset and IT request management
- Compensation review / salary revision cycles
- Advanced reports / BI / semantic reporting
- Integration marketplace
- Workforce planning / forecasting
- Contingent workforce
- Multi-country payroll plugins
- Provider and integration health center
- Implementation and configuration operations

### Extension Rule for Future Modules

Future modules must be **open for extension and closed for changes to existing core**:

- New modules register through a module manifest, feature flag, permissions, routes,
  navigation metadata, API contracts, event subscriptions, and database migrations.
- New modules reuse platform engines: Identity, RBAC/ABAC, Workflow, Rules, Forms,
  Reports, Audit, Notification, Search, AI/RAG, and Event Bus.
- New module behavior must be configured through metadata, rules, workflow definitions,
  templates, extensions, plugins, and provider adapters.
- Existing core modules must not be modified for customer-specific requirements.
- Cross-module communication must happen through published APIs/events, not direct table
  reads or hidden coupling.

---

# Non Functional Requirements

- **Performance:** Core screens < 2s P95; payroll run for 2,000 employees within agreed
  batch window.
- **Scalability:** Multi-tenant to thousands of tenants; modular monolith (ADR-004) with
  schema-per-module for future extraction.
- **Extensibility:** New modules and customer-specific behavior must be added through
  configuration, extensions, plugins, provider adapters, public APIs, and events without
  modifying existing core modules.
- **Security:** OWASP Top 10 defended; tenant isolation; AES-256 at rest, TLS in transit;
  per `SECURITY_STANDARDS.md`.
- **Availability:** Target 99.9%; **zero-regression release discipline** (validated pain
  P5) — no breaking changes to live payroll workflows.
- **Accessibility:** WCAG-compliant; keyboard + screen-reader; mobile-first.
- **Localization:** English + Hindi at launch (Arabic-ready); no hardcoded text.
- **Auditability:** Every business action logged (FR-008).
- **Reliability of support (product-enabling):** in-app help + status visibility (ops SLA
  is a go-to-market commitment, tracked outside this PRD).

---

# Dependencies

- **Internal:** Architecture (Phase 3), Database design (Phase 3), Security design,
  API specs (Phase 5), UX/UI (Phase 4). No build until those are approved (Rule 1).
- **External:** SQL Server, Redis, Elasticsearch, Azure Blob, RabbitMQ/Service Bus;
  biometric device SDKs (ZKTeco/eSSL); model-switchable LLM providers for FR-011
  through the approved AI/provider abstraction direction.

---

# Risks

| Risk | Mitigation |
|---|---|
| Workflow Studio (FR-007) is the differentiator **and** the hardest to build | Spike/prototype early in Phase 3; Solution Architect feasibility vs ADR-004 before committing a Phase 7A delivery date |
| India statutory rules change (wage code, IT rules) | Rules-as-data + compliance engine updates, not code/tickets |
| Scope creep back toward "module count" | Enforce the OUT-of-scope list; changes require PRD revision + approval |
| AI moving target (Darwinbox Agentic AI) | Position FR-011 as *affordable RAG for mid-market*, not "first to AI" |
| Unvalidated Tier-3 bets pull focus | Keep them out of Phase 7A; validate via 5–10 buyer interviews (gap analysis §5) |

---

# Success Metrics

- **KPIs:** ≥1 config change type (workflow/form/field) done by a tenant admin with
  **zero vendor involvement** (proves the wedge); payroll accuracy ≥ 99.9%.
- **Adoption:** Employee mobile MAU; % leave/approvals done on mobile; ESS self-serve rate.
- **Performance:** P95 page < 2s; payroll batch within window; ≥ 99.9% uptime.
- **Quality:** Zero payroll-breaking regressions per release; ≥ 85% test coverage.

---

# Approval

Product Owner: ____ · Project Manager: ____ · Solution Architect: ____ · HR Expert: ____
(Status: Draft → Approved)
