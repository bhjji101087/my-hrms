# Phase 7A Hardening Backlog - Documentation Review Recommendations

Document Owner: Product Owner / Program Director
Created Date: 2026-06-29
Version: 1.0
Status: Approved
> Source: attached Phase 7A Documentation Review Report reviewed on 2026-06-29.
> Purpose: convert approved-with-recommendations review notes into trackable Phase 7A
> hardening backlog items. This document uses phase-based wording; old launch-scope wording
> must not be used.

## 1. Current Gate Position

The Phase 7A implementation documentation set contains 55 module documents:

- 5 Effective Dating documents are already Approved in the repository.
- 50 module documents remain Draft and require owner/specialist approval.
- The review report found no major architectural blocker.
- Recommendations are enterprise-hardening items that must be triaged before development
  starts or explicitly deferred with owner approval.

## 2. Cross-Cutting Hardening Items

| ID | Item | Owner | Target Doc / Standard | Gate |
|---|---|---|---|---|
| P7A-HARD-001 | Shared API contract standard | Solution Architect | `PHASE-7A-STD-001-api-event-nfr-runbooks.md` | Before development |
| P7A-HARD-002 | Shared event contract standard | Integration Architect | `PHASE-7A-STD-001-api-event-nfr-runbooks.md` | Before development |
| P7A-HARD-003 | Table-level PII/data classification | Database Architect | `DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md` | Before DB implementation |
| P7A-HARD-004 | Migration, rollback, and validation queries | Database Architect | `DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md` | Before DB implementation |
| P7A-HARD-005 | UI accessibility and screen-state checklist | UX/UI Architect | `UI-PHASE-7A-STD-001-accessibility-states.md` | Before UI implementation |
| P7A-HARD-006 | Test traceability matrix | QA Architect | `TEST-PHASE-7A-STD-001-traceability-abuse.md` | Before test execution |
| P7A-HARD-007 | Multi-tenant abuse tests | QA + Security | `TEST-PHASE-7A-STD-001-traceability-abuse.md` | Before release |
| P7A-HARD-008 | Operational mini-runbooks | Module Owners | `PHASE-7A-STD-001-api-event-nfr-runbooks.md` | Before release |
| P7A-HARD-009 | Export/data leakage controls | Security + QA | Test plans and UI docs | Before release |
| P7A-HARD-010 | Rule/config/workflow impact analysis | Solution Architect | Module docs | Before implementation |

## 3. Module-Specific Recommendations

### Audit and Time Machine

- Add tamper-evidence hash chaining or digest signing for high-value audit records.
- Add sensitive audit evidence export approval rules.
- Add audit redaction policy for UI masking versus immutable evidence.
- Add tests for privileged admin actions, impersonation, and failed access attempts.
- Add retention matrix by audit category: security, payroll, employee data, workflow, system.
- Ensure evidence exports require permission, watermarking, reason capture, and export audit.

### Event Bus and Outbox

- Add event ordering rules: per aggregate, per tenant, or best-effort.
- Add poison message policy: retry count, quarantine, owner, SLA.
- Add replay approval flow for sensitive events.
- Add schema compatibility rules: backward compatible, breaking change, deprecation.
- Add payload size limits and PII redaction rules.
- Add consumer idempotency examples and make idempotency mandatory before replay.

### Rule Engine

- Add rule dependency graph and circular dependency detection.
- Add rule priority and conflict resolution model.
- Add sandbox simulation using sample employees and test contexts.
- Add explain-rule-result output contract.
- Add performance guardrails for expensive rule evaluation.
- Add emergency rollback to previous published rule version.
- Require maker-checker and automated validation before high-risk activation.

### Workflow Studio

- Add deadlock and loop prevention.
- Add parallel approval semantics: all-of, any-of, majority, sequential.
- Add escalation calendar behavior for weekends, holidays, and time zones.
- Add delegation conflict rules.
- Add workflow cancellation and resubmission behavior.
- Add workflow migration behavior when definitions change while instances are running.
- Preserve version pinning for existing running instances.

### Configuration-as-Data

- Add configuration dependency validation.
- Add import/export with schema validation.
- Add preview/diff before publish.
- Add tenant-level configuration freeze during payroll close.
- Add rollback to previous published configuration version.
- Add configuration cache invalidation event.
- Require impact analysis before publish.

### Core HR and ESS

- Add employee identity merge/de-duplicate process.
- Add worker lifecycle states: pre-joiner, active, transferred, on notice, exited, rehired.
- Add manager hierarchy effective dating.
- Add legal entity, department, and location change impact events.
- Add document management rules for employee files.
- Add sensitive-field masking by role.
- Ensure Core HR domain events carry version and correlation metadata.

### Leave

- Add leave year/calendar configuration.
- Add carry-forward, encashment, lapse, and negative-balance rules as configuration.
- Add sandwich leave and holiday/weekend treatment.
- Add half-day and hourly leave behavior.
- Add cancellation after approval and after payroll lock.
- Add conflict handling with attendance and payroll.
- Confirm balance is reproducible as of date using ledger and transaction trace.

### Attendance

- Strengthen raw punch versus processed attendance separation.
- Add device/user mapping lifecycle.
- Add duplicate punch detection and late-arriving punch handling.
- Add shift, grace, overtime, night shift, and cross-midnight scenarios.
- Add offline biometric sync handling.
- Add payroll lock interaction and correction path after lock.

### Payroll and India Compliance

- Add payroll source snapshot table details, not only hash/reference.
- Add calculation explainability model: formula, inputs, rule version, intermediate values.
- Add statutory challan/output foundation even if filing automation is out of scope.
- Add payslip access audit and download watermarking.
- Add payroll close calendar and reopen controls.
- Add correction run versus adjustment run semantics.
- Do not start payroll implementation until snapshot, correction, reversal, and explain
  calculation contracts are fully specified.

### Reporting and Analytics

- Add row-level report security model.
- Add export limits and async export for large reports.
- Add report freshness indicators.
- Add semantic metric definitions to avoid inconsistent calculations.
- Add scheduled report delivery permissions as a future-controlled capability.
- Add PII masking and redaction by role.
- Add export and scheduled-delivery security tests.

## 4. Non-Gate / Reference Recommendations

- Market Research Refresh: add assumptions to validate after Phase 7A/post-release customer
  usage.
- Architecture Expert Assessment: convert unresolved recommendations into backlog items or
  ADRs.
- Architecture Decision Template: add security impact, data classification, rollback,
  observability, and cost impact sections.
- Product Requirements Template: add personas, NFRs, event impact, audit impact, security
  impact, and test traceability fields.
- Module Backlog: add dependency map between modules and release gates.

## 5. Recommended Approval Decision Text

```text
Phase 7A Approval Queue Decision:
Approved with Recommendations.

Reason:
All required module document sets are present and aligned. No major architectural blocker
was found in the reviewed documentation. Cross-cutting hardening standards for API
contracts, event contracts, PII classification, migration/rollback, test traceability, and
operational runbooks have been created and must be approved or explicitly deferred before
development starts.

Approval Condition:
Recommendations may be tracked through this backlog or added directly to the module
documents before final sign-off.
```

## Approval

Product Owner: ____ - Solution Architect: ____ - Security Architect: ____ - QA Architect: ____ - Status: Approved
