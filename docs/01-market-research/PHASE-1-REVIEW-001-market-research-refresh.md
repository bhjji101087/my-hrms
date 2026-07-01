# Phase 1 Review - Market Research Refresh

Document Owner: Codex Review Agent
Created Date: 2026-06-16
Version: 1.0
Status: Draft

> Purpose: review the approved Phase 1 market research against current vendor portals
> and customer-review evidence, then identify missing modules, customer happiness
> signals, irritation points, and feature refinements for the HRMS platform.

---

## 1. Review Verdict

The Phase 1 documents are directionally strong. They correctly identify the main wedge:
true no-code configurability, India payroll/compliance depth, tenant isolation,
workflow/rule engines, and affordable RAG-based AI.

However, the market research should be strengthened in three areas:

1. Add a broader module coverage matrix across Indian and global vendors.
2. Separate "differentiator" features from "table-stakes" modules.
3. Convert customer irritation themes into product-grade refinement requirements.

The biggest conclusion is still valid: customers are not only asking for more modules.
They are asking for modules that are easier to configure, safer to change, more reliable
on mobile, better supported, and less dependent on vendor tickets.

---

## 2. Sources Reviewed

### Official vendor/product portals

- greytHR: https://www.greythr.com/
- Keka: https://www.keka.com/
- HROne: https://hrone.cloud/hr-software/
- Darwinbox: https://darwinbox.com/
- Zoho People: https://www.zoho.com/people/features.html
- factoHR: https://factohr.com/hr-software/
- Zimyo: https://www.zimyo.com/
- Qandle: https://www.qandle.com/
- BambooHR: https://www.bamboohr.com/
- Workday HCM: https://www.workday.com/en-us/products/human-capital-management/overview.html
- SAP SuccessFactors: https://www.sap.com/products/hcm.html
- UKG: https://www.ukg.com/

### Customer-review and comparison sources

- Capterra greytHR reviews: https://www.capterra.com/p/150850/greytHR/reviews/
- GetApp Keka reviews: https://www.getapp.com/hr-employee-management-software/a/keka/reviews/
- G2 Darwinbox reviews: https://www.g2.com/products/darwinbox/reviews
- G2 Zoho People reviews: https://www.g2.com/products/zoho-people/reviews
- SoftwareSuggest HROne reviews: https://www.softwaresuggest.com/hrone/reviews
- Gartner Peer Insights greytHR: https://www.gartner.com/reviews/product/greythr

> Note: review portals contain mixed-quality data and some pages vary by region, date,
> and reviewer type. Treat this as directional evidence, not final statistical proof.

---

## 3. Vendor Module Coverage - What Exists in the Market

| Module / Capability | India SMB/Mid Vendors | Enterprise Vendors | Status for Our Docs |
|---|---|---|---|
| Core HR / employee master | Common | Common | Covered |
| ESS / MSS self-service | Common | Common | Covered |
| Leave management | Common | Common | Covered |
| Attendance / time | Common | Common | Covered |
| Payroll | Common in India vendors | Common, often country-specific | Covered |
| India statutory compliance | Strong in India vendors | Weak/partner-led for global vendors | Covered |
| Recruitment / ATS | Common in Keka, HROne, Darwinbox, Zoho/BambooHR ecosystem | Common | Deferred; should be documented as a full later phase |
| Onboarding | Common | Common | Under-documented |
| Offboarding / exit / FNF workflow | Present in stronger suites | Common | Under-documented |
| Performance / PMS / goals | Common | Common | Deferred; needs stronger feature plan |
| LMS / learning | Present in several suites | Common | Deferred; needs later-phase docs |
| Engagement / pulse / surveys | Increasingly common | Common | Missing as explicit product module |
| HR service desk / cases | Common enough to be table-stakes | Common | Demoted as differentiator, but should still be included |
| Expense / travel / reimbursements | Common in broader suites | Common | Present in master plan, missing from phased product detail |
| Assets / IT requests | Present in some Indian suites | Common via integrations | Missing from phased product detail |
| Document management / letters / e-sign | Common | Common | Under-documented |
| Shift foundation + advanced roster/workforce scheduling | Common in attendance-heavy products | Strong in UKG-like systems | Split required: Shift Foundation in Phase 7A; advanced roster later |
| Analytics / dashboards | Common, quality varies | Strong | Covered, but needs deeper semantic/reporting roadmap |
| Workforce planning / forecasting | Rare in SMB tools | Stronger in enterprise | Identified correctly as opportunity |
| Integration marketplace | Partial | Common ecosystem approach | Identified, but needs module-level plan |
| AI assistant / AI workflows | Emerging in enterprise | Increasingly common | Covered; positioning needs affordability and grounding |
| Multi-entity / org graph | Partial in SMB, stronger in enterprise | Common | Identified, but needs validation and data model plan |
| Contingent workforce | Weak in SMB | Better in enterprise | Identified as unvalidated; keep as later phase |

---

## 4. What Customers Like

### 4.1 Payroll and compliance reliability

Customers value products that reduce monthly payroll anxiety: salary processing,
statutory deductions, payslips, tax forms, and compliance reports. This supports the
current requirement that India payroll and compliance must be deep, not superficial.

Product implication:
- Payroll should include pre-run validation, variance checks, statutory calendars,
  retro/mid-cycle changes, FBP, reconciliation, and approval checkpoints.

### 4.2 Simple ESS and mobile access

Employees and managers like products when leave, attendance, payslips, approvals, and
basic profile changes are easy on mobile.

Product implication:
- Mobile is not a "nice to have." It needs strict reliability, offline/error recovery,
  quick approvals, clear status, and fast login.

### 4.3 Modern UI and low learning curve

Keka, BambooHR, Darwinbox, and Zoho People are repeatedly valued for cleaner UX, role
dashboards, and self-service flows.

Product implication:
- Our approved UI direction is correct, but every dense admin screen needs guided setup,
  templates, previews, and clear error states.

### 4.4 Broad suite coverage

Customers like not having to run many tools for recruitment, onboarding, performance,
learning, expense, documents, and HR tickets.

Product implication:
- The "full-product launch" strategy should include full module documentation, even if
  implementation is phased.

### 4.5 Configurability when it works

Enterprise buyers value configurable workflows, custom fields, policies, roles, and
reports.

Product implication:
- Workflow Studio and Rule Builder remain the strongest differentiators, but they must
  include sandbox, simulation, versioning, rollback, and impact analysis.

---

## 5. What Customers Are Irritated By

### 5.1 Support delays and weak escalation

Review evidence frequently points to support delays, slow issue resolution, or unclear
escalation paths. This is a market-wide trust problem.

Refined feature requirement:
- Add in-app support status, ticket severity, SLA timer, escalation path, product status
  page, and release-impact notices.

### 5.2 Configuration ceiling

Customers get irritated when "configurable" still means vendor tickets for conditional
approval, validation, policy changes, role scoping, reports, or custom fields.

Refined feature requirement:
- No-code configuration must cover forms, workflows, rules, reports, dashboards,
  navigation, notifications, roles, and tenant branding.
- Add config sandbox -> compare diff -> approve -> promote -> rollback.

### 5.3 Mobile app and attendance reliability

Common pain themes include login issues, punch sync failures, geolocation/facial issues,
device connector instability, and slow mobile flows.

Refined feature requirement:
- Attendance needs device health monitoring, sync retry, duplicate punch handling,
  offline capture, shift-aware regularization, and clear employee-visible status.

### 5.4 Payroll edge cases

Customers dislike manual workarounds for FBP, mid-cycle CTC changes, arrears, proration,
retro changes, variable pay, multi-state PT, and corrections after payroll lock.

Refined feature requirement:
- Payroll must include simulation, dry run, variance report, correction workflow,
  effective-dated salary changes, payroll lock, exception queue, and audit trail.

### 5.5 Implementation complexity

Large suites often become powerful but heavy. Setup takes too long, and configuration
is difficult for non-technical HR teams.

Refined feature requirement:
- Add onboarding wizard, setup checklists, policy templates, workflow templates,
  migration validators, sample payroll runs, and readiness score.

### 5.6 Reporting gaps

Customers are often forced back to Excel for attrition, attendance trends, payroll
exceptions, compliance gaps, and manager views.

Refined feature requirement:
- Reports need saved views, scheduled reports, role-secured data marts, export history,
  natural-language report drafting, and row-level permission enforcement.

### 5.7 Pricing/add-on confusion

Customers often dislike unclear module add-ons and hidden costs.

Refined feature requirement:
- Tenant entitlements should be transparent: enabled modules, limits, usage, billing
  drivers, and upcoming renewal impact.

---

## 6. Comparison Against Our Existing Documents

### Strongly covered already

- Multi-tenant platform foundation
- Tenant isolation and RLS
- RBAC + ABAC + audit
- Rule Engine
- Workflow Studio
- Dynamic forms and configuration
- India payroll/compliance
- Attendance connector framework
- RAG AI assistant with citations
- White-labeling
- Event-driven architecture
- Effective-dated/bitemporal data

### Correctly identified, but needs stronger documentation

- Recruitment / ATS
- Onboarding and offboarding
- Performance / goals / OKRs
- LMS / learning
- Workforce planning
- Multi-entity / org graph
- Integration marketplace
- HR service desk
- Reporting and analytics
- Mobile-first employee app

### Missing or under-emphasized modules/features

1. **Engagement module** - pulse surveys, recognition, announcements, employee mood,
   eNPS, feedback loops.
2. **Document and letter management** - offer letters, salary letters, policy
   acknowledgements, e-signature, document expiry, document templates.
3. **Shift foundation and workforce scheduling** - Phase 7A needs shift definitions,
   employee shift assignment, and attendance/payroll impact; later phases need roster
   planning, shift swaps, overtime planning, weekly-off rules, and location-based schedules.
4. **Expense, travel, and reimbursements** - claims, approvals, policy checks, payroll
   integration.
5. **Asset and IT request management** - asset allocation, return, maintenance,
   onboarding/offboarding task links.
6. **Compensation management** - salary revision cycles, merit matrix, bonus, variable
   pay, increment letters.
7. **Case management / HR service desk** - ticket categories, SLA, knowledge base,
   employee request tracking.
8. **Implementation and configuration operations** - tenant setup wizard, config
   templates, sandbox promotion, config diff, rollback, release preview.
9. **Provider and integration health center** - device sync, email/SMS/push provider
   health, webhook delivery, retry queues.
10. **Admin transparency** - feature entitlements, limits, usage, audit of config changes,
    admin activity history.

---

## 7. Recommended Updates to Phase 1 Documents

### Update 1 - Add a broader module matrix

Add a table that compares at least these vendors:

- greytHR
- Keka
- HROne
- Darwinbox
- Zoho People
- factoHR
- Zimyo
- Qandle
- BambooHR
- Workday
- SAP SuccessFactors
- UKG

Include modules beyond payroll/leave/attendance: ATS, onboarding, PMS, LMS, engagement,
service desk, expense, assets, documents, workforce scheduling, analytics, AI, and
integration marketplace.

### Update 2 - Split features into three buckets

Use these buckets in Phase 1:

- **Table-stakes:** payroll, leave, attendance, ESS, reports, HR service desk,
  onboarding, document management.
- **Differentiators:** no-code Workflow Studio, Rule Engine, compliance intelligence,
  mobile reliability, RAG AI, sandbox-to-production configuration, provider health.
- **Strategic later phases:** workforce planning, marketplace, advanced analytics,
  manager intelligence, multi-country payroll plugins.

### Update 3 - Add customer-happiness criteria

For each module, define what "good" means from a customer perspective.

Examples:

- Payroll: zero manual correction for standard edge cases.
- Attendance: visible sync status and no lost punches.
- Leave: policy rules configurable without vendor tickets.
- Mobile: approval/apply flows under one minute.
- Reports: no forced Excel export for common HR questions.

### Update 4 - Add irritation-to-feature mapping

Turn each pain into a feature refinement:

| Irritation | Product refinement |
|---|---|
| Slow support | SLA ticketing, escalation, status page |
| Config needs vendor | No-code config + sandbox + rollback |
| Mobile bugs | Offline/retry, native-like flows, telemetry |
| Payroll manual edge cases | Simulation, exception queue, effective-dated rules |
| Reporting exports | Saved views, scheduled reports, semantic query layer |
| Device sync failures | Connector health, retries, duplicate detection |
| Implementation drag | Setup wizard, templates, migration validator |

### Update 5 - Add primary research before final sign-off

Phase 1 should include 5-10 buyer interviews from the target segment:

- HR head at 100-500 employees
- HR ops/payroll lead at 500-2,000 employees
- Finance/payroll controller
- Line manager
- Employee self-service user
- IT/admin owner

Interview goals:

- Validate module priority.
- Validate willingness to pay for no-code configuration.
- Identify payroll/attendance edge cases.
- Rank customer irritation severity.
- Confirm whether service desk, engagement, expense, and assets are required for launch.

---

## 8. Recommended Missing Modules for Future Documentation

Create separate feature-document sets for:

1. Recruitment / ATS
2. Onboarding
3. Offboarding / exit / FNF
4. Performance / goals / OKRs
5. Learning / LMS
6. Engagement / surveys / recognition
7. HR service desk / case management
8. Document management / letters / e-sign
9. Expense / travel / reimbursements
10. Asset and IT request management
11. Shift Foundation in Phase 7A; advanced roster/workforce scheduling later
12. Compensation review / salary revision
13. Advanced reports / analytics / BI
14. Integration marketplace
15. Workforce planning / forecasting

These should not all be built first, but they should be acknowledged in the full-product
phase plan so the product does not look like only payroll, leave, and attendance.

---

## 9. Product Refinement Recommendations

### Highest priority refinements

1. Make **configuration operations** a first-class module: sandbox, diff, approval,
   promotion, rollback, audit.
2. Make **mobile reliability** a measurable product requirement, not just UI intent.
3. Make **payroll edge-case handling** explicit: arrears, retro, FBP, mid-cycle CTC,
   proration, lock/unlock, correction workflow.
4. Make **attendance connector reliability** explicit: health, retry, duplicate handling,
   offline capture, and reconciliation.
5. Add **implementation success tooling**: setup wizard, templates, migration validation,
   readiness score.
6. Add **HR service desk** as table-stakes, even if not a differentiator.
7. Add **document/letter/e-sign management** as a core HR adjacent module.
8. Add **engagement** as a later-phase module because competitors increasingly include it.

### Positioning refinement

Current positioning should remain:

> Configurable, India-compliance-strong, AI-native People Operations Platform.

But the sharper customer promise should be:

> "Change HR policies, workflows, payroll rules, reports, and employee journeys without
> vendor tickets - with payroll-grade audit, rollback, and compliance safety."

---

## 10. Action Items

1. Update `competitor-analysis-india.md` with the broader module matrix.
2. Update `competitor-gap-analysis.md` with irritation-to-feature mapping.
3. Add feature backlog entries for the missing modules in `docs/21-product-backlog/`.
4. Add primary-research interview plan and questionnaire in `docs/17-meeting-notes/` or
   `docs/01-market-research/`.
5. Reconcile the phased delivery roadmap so later phases explicitly include the missing
   table-stakes modules.

---

## 11. Assumptions to Validate After Phase 7A / Post-Release

- Customers can configure common HR, leave, attendance, payroll, workflow, and reporting
  changes without vendor tickets.
- Payroll-grade audit, rollback, and explainability are strong enough to reduce manual
  spreadsheet reconciliation.
- Workflow Studio and Rule Engine are understandable for tenant administrators without
  daily developer support.
- Attendance connector reliability and reconciliation are strong enough for payroll trust.
- Standard reports cover the first operational needs before advanced BI is introduced.
- Later modules such as HR service desk, documents/e-sign, onboarding, engagement, expense,
  assets, recruitment, performance, and LMS are prioritized correctly by real customer demand.

---

## Approval

Product Owner: ____ · HR Domain Expert: ____ · Competitor Gap Analyst: ____ ·
Solution Architect: ____  (Status: Draft -> Approved)
