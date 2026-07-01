# Technical Design - Payroll and India Compliance

Module: Payroll
Phase: 7A / Sprints S7-S8
Owner: .NET Architect (Agent 13)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Payroll and India Compliance.

## Architecture

Payroll is a business-critical module that consumes effective-dated source data and
published rules. It owns payroll runs, calculation results, payslips, statutory outputs,
and reconciliation evidence. Payroll does not directly modify Core HR, Leave, or Attendance.

```text
Payroll Run -> Source Snapshot -> Rule Evaluation -> Calculation Ledger -> Approval -> Payslip
                    |                  |                 |
              Core/Leave/Attendance  Rule Engine      Audit/Event Bus
```

## Components

- Payroll Calendar Service: pay periods, cutoffs, locks.
- Salary Structure Service: component groups, formulas, eligibility.
- Payroll Source Snapshot Service: locks Core HR, Leave, Attendance, and component inputs.
- Shift-aware Attendance Input Adapter: consumes approved attendance summaries calculated
  from effective employee shift assignment.
- Calculation Engine: evaluates earnings, deductions, arrears, LOP, statutory components.
- Statutory Rule Pack Service: India PF/ESI/PT/LWF/TDS effective-dated rules.
- Payroll Run Service: dry run, validation, approval, lock, publish, correction.
- Payslip Service: payslip data and file generation.
- Reconciliation Service: variance and exception checks.

## API Requirements

APIs under `/api/v1/payroll` cover salary structures, salary assignments, declarations,
pay periods, payroll runs, run validation, approval, publish, payslips, statutory outputs,
and reconciliation. OpenAPI must document idempotency, async run status, validation errors,
and explain-calculation responses.

## Calculation Rules

- All formulas are stored in Rule Engine and version-pinned per run.
- Statutory values are effective-dated and reviewed before publish.
- Payroll source snapshot is immutable after lock.
- Overrides require reason, permission, and audit.
- Corrections create adjustment entries; they do not overwrite published run evidence.

## Security

Permissions include `Payroll.View`, `Payroll.Manage`, `Payroll.Run`, `Payroll.Approve`,
`Payroll.PublishPayslip`, `Payroll.Configure`, and `Payroll.SensitiveView`. Payroll data is
highly sensitive and requires strict ABAC by tenant, branch/office, legal entity, payroll
group, and role.

## Events

`PayrollRunCreated`, `PayrollRunCalculated`, `PayrollRunValidationFailed`,
`PayrollRunApproved`, `PayrollRunPublished`, `PayslipPublished`,
`PayrollCorrectionCreated`.

## Observability

Track run duration, calculation errors, statutory validation failures, exception count,
approval aging, payslip generation failures, and payroll event publish latency.

## Phase 7A Shift and Branch Addendum

Payroll must consume approved Shift Foundation and Branch / Office scope documents:
`TECH-SHIFT-FOUNDATION-001` and `TECH-BRANCH-001`. Payroll calculations use shift-aware
attendance summaries and enforce branch/office scope with payroll group and legal entity.

## Acceptance Criteria

1. Payroll run is reproducible from source snapshot and rule versions.
2. India statutory rules are effective-dated and approval-controlled.
3. Mid-cycle salary revision and LOP are calculated correctly in sample scenarios.
4. Published payroll cannot be silently overwritten.
5. Explain-calculation API returns calculation lineage for authorized users.

## External References

- EPFO: https://www.epfindia.gov.in/site_en/index.php
- ESIC: https://www.esic.gov.in/
- Income Tax Department: https://www.incometax.gov.in/iec/foportal/
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

.NET Architect: ____ - Payroll Domain Expert: ____ - Security Architect: ____ - Status: Approved
