# UI Design - Payroll and India Compliance

Module: Payroll
Phase: 7A / Sprints S7-S8
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 4 of 5 for Payroll and India Compliance.

## UX Goals

Payroll screens must be careful, dense, and evidence-oriented. Users need validation
clarity, exception handling, approval control, and confidence before publishing payslips.

## Screen A - Payroll Dashboard

Shows current pay period, run status, cutoff, open inputs, validation exceptions, approval
status, publish status, and key totals. Sensitive amounts are visible only to permitted
users.

## Screen B - Salary Structure Builder

Configures components, formulas, eligibility, taxable class, statutory flags, effective
dates, and approval route. Formula editing links to Rule Engine and simulation.

## Screen C - Payroll Run Workbench

Run dry calculation, review employee-level exceptions, compare variance, inspect source
snapshot, open calculation explanation, submit for approval, lock, and publish.

## Screen D - Statutory Configuration

Admin configures PF, ESI, PT, LWF, TDS, and Form 16 data rules with effective dates,
official source reference, validation tests, and compliance approval.

## Screen E - Employee Payslip

Employee views published payslip, earnings, deductions, net pay, statutory details, and
download action. Payslip download is audited.

## Screen F - Payroll Corrections

Authorized payroll users create correction/reversal requests with reason, affected period,
impact preview, and approval workflow.

## Acceptance Criteria

1. Payroll workbench clearly separates dry run, locked, approved, and published states.
2. Calculation explanation is available for authorized payroll users.
3. Statutory config requires source reference and approval.
4. Employee can view only own published payslip.
5. Payroll correction flow captures reason and audit.

## External References

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Income Tax Department: https://www.incometax.gov.in/iec/foportal/
- greytHR market reference: https://www.greythr.com/
- Keka market reference: https://www.keka.com/

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

UX/UI Architect: ____ - Product Owner: ____ - Payroll Domain Expert: ____ - Status: Approved
