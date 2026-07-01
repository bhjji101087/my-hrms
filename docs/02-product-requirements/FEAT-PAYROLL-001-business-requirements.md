# Feature Specification - Payroll and India Compliance

Feature Name: Payroll and India Compliance
Module: Payroll
Phase: 7A / Sprints S7-S8
Owner: Product Owner (Agent 2)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 1 of 5 for Payroll. Implements PRD FR-006.

## Purpose

Payroll must calculate accurate salary, deductions, statutory contributions, reimbursements,
taxable values, payslips, and payroll outputs using governed rules and auditable source
data. Phase 7A focuses on India-first payroll and compliance foundation.

## Market and Enterprise Context

India HRMS vendors such as greytHR, Keka, Zoho Payroll/People, and Darwinbox emphasize
payroll automation, statutory compliance, payslips, leave/attendance integration, and tax
declarations. Customers are highly irritated by wrong statutory calculations, manual Excel
workarounds, unclear payslip logic, failed month-end runs, and weak auditability.

## Scope

In scope:
- Salary structures and salary components.
- Effective-dated compensation assignments.
- Payroll calendar, pay periods, payroll run, dry run, lock, approval, publish.
- Earnings, deductions, reimbursements, arrears, recovery, and loss of pay.
- FBP/flexible benefits foundation.
- Mid-cycle CTC/salary revision handling.
- India statutory configuration for PF, ESI, PT, LWF, TDS, Form 16 data foundation.
- Payslip generation and payroll reports.

Out of scope:
- Multi-country payroll packs.
- Direct bank file integration.
- Full tax filing automation unless separately approved.
- Expense/travel module.

## Business Requirements

1. Payroll formulas shall use Rule Engine and effective-dated rule versions.
2. Payroll runs shall be reproducible from locked source data, rule versions, and period.
3. Payroll shall consume Core HR, Leave, Attendance, and Configuration-as-Data through
   approved APIs/events/read models.
4. Statutory rules shall be configurable and effective-dated; no rates or thresholds shall
   be hardcoded in application logic.
5. Production statutory rule activation shall require payroll/compliance approval.
6. Payroll run lifecycle shall support draft, dry run, validation, approval, lock, publish,
   correction, and reversal where allowed.
7. Payslips shall be generated only after payroll approval and publish.
8. Every calculation, override, approval, and output shall be audited.

## Acceptance Criteria

1. Payroll dry run calculates sample employees using Core HR, Leave, Attendance, and rules.
2. Mid-cycle salary revision produces correct period split using effective dating.
3. Statutory components are calculated through approved effective-dated rule sets.
4. Payroll approval locks inputs and publishes payslips.
5. Payroll run can be explained by source data, rule version, and audit evidence.

## External References

- EPFO official portal: https://www.epfindia.gov.in/site_en/index.php
- ESIC official portal: https://www.esic.gov.in/
- Income Tax Department official portal: https://www.incometax.gov.in/iec/foportal/
- greytHR market reference: https://www.greythr.com/
- Keka market reference: https://www.keka.com/

References last validated: 2026-06-28.

## Approval

Product Owner: ____ - Payroll Domain Expert: ____ - Compliance Reviewer: ____ - Status: Approved
