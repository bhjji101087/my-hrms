# Test Plan - Payroll and India Compliance

Module: Payroll
Phase: 7A / Sprints S7-S8
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 5 of 5 for Payroll and India Compliance.

## Functional Tests

- Configure salary structure and components.
- Assign salary effective-dated to employee.
- Run payroll dry run and review exceptions.
- Calculate LOP from approved leave and attendance data.
- Calculate mid-cycle CTC revision split.
- Approve and publish payroll run.
- Generate and view payslip.

## Statutory Tests

- PF/ESI/PT/LWF/TDS applicability uses effective-dated approved rules.
- Statutory rule source reference and approval are mandatory.
- Form 16 data foundation matches payroll/taxable output expectations.
- State-specific professional tax rules are selected by jurisdiction configuration.

## Security Tests

- Employee views own payslip only.
- Payroll admin scope is restricted by branch/office, legal entity, and payroll group.
- Sensitive payroll data is masked without permission.
- Unauthorized correction, publish, or statutory config is rejected.
- Cross-tenant payroll access is blocked.

## Integration Tests

- Core HR assignment and salary as-of pay period.
- Leave unpaid days feed payroll.
- Attendance payable days feed payroll.
- Shift-aware attendance summary feeds payroll where configured.
- Rule Engine evaluates formulas and statutory rules.
- Workflow approves run and corrections.
- Audit and events capture run lifecycle.

## Negative Tests

- Payroll cannot publish with unresolved critical exceptions.
- Published run cannot be overwritten.
- Duplicate publish request is idempotent.
- Missing source snapshot blocks calculation.
- Backdated salary change after lock requires correction workflow.

## Performance Tests

- Payroll dry run completes within agreed batch window.
- Calculation explanation query is responsive for one employee.
- Payslip generation handles tenant pay period volume.

## Exit Criteria

- Minimum 85% automated coverage; calculation engine minimum 90%.
- Payroll sample pack signed off by payroll/compliance reviewer.
- Zero unauthorized payroll visibility.
- OpenAPI and E2E payroll-run lifecycle pass.

## External References

- EPFO: https://www.epfindia.gov.in/site_en/index.php
- ESIC: https://www.esic.gov.in/
- Income Tax Department: https://www.incometax.gov.in/iec/foportal/

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Phase 7A Shift and Branch Addendum

Payroll testing must include shift-aware attendance impact from
`TEST-SHIFT-FOUNDATION-001` and branch-scope authorization from `TEST-BRANCH-001`.

## Approval

QA Architect: ____ - Payroll Domain Expert: ____ - Security Architect: ____ - Status: Approved
