# Database Design - Payroll and India Compliance

Module: Payroll
Schema: `payroll`
Phase: 7A / Sprints S7-S8
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Payroll and India Compliance.

## Tables

```text
payroll.PayrollCalendar
  PayrollCalendarId, TenantId, LegalEntityId, Code, Name, Frequency,
  TimeZone, IsActive, audit columns

payroll.PayPeriod
  PayPeriodId, TenantId, PayrollCalendarId, PeriodStart, PeriodEnd,
  CutoffDate, Status, LockedAt, audit columns

payroll.SalaryComponent
  SalaryComponentId, TenantId, Code, Name, ComponentType, TaxabilityClass,
  RuleSetId, IsStatutory, IsActive, audit columns

payroll.SalaryStructureVersion
  SalaryStructureVersionId, TenantId, Code, EffectiveFrom, EffectiveTo,
  DefinitionJson, Status, ApprovalWorkflowInstanceId, audit columns

payroll.EmployeeSalaryAssignment
  EmployeeSalaryAssignmentId, TenantId, EmployeeId, SalaryStructureVersionId,
  EffectiveFrom, EffectiveTo, CtcAmount, ApprovalReferenceId, audit columns

payroll.PayrollRun
  PayrollRunId, TenantId, PayPeriodId, RunType, Status, SourceSnapshotHash,
  RuleVersionSnapshotJson, ApprovedBy, PublishedAt, audit columns

payroll.PayrollRunEmployee
  PayrollRunEmployeeId, TenantId, PayrollRunId, EmployeeId, GrossEarnings,
  TotalDeductions, NetPay, TaxableIncome, ExceptionStatus, audit columns

payroll.PayrollRunComponent
  PayrollRunComponentId, TenantId, PayrollRunEmployeeId, SalaryComponentId,
  Amount, CalculationTraceReference, RuleSetVersionId, audit columns

payroll.StatutoryRuleVersion
  StatutoryRuleVersionId, TenantId, StatutoryType, JurisdictionCode,
  EffectiveFrom, EffectiveTo, RuleSetVersionId, SourceReference,
  ApprovalWorkflowInstanceId, Status, audit columns

payroll.Payslip
  PayslipId, TenantId, PayrollRunEmployeeId, FileReference, PublishedAt,
  ViewedAt, Status, audit columns
```

## Indexes

- `PayPeriod`: unique `(TenantId, PayrollCalendarId, PeriodStart, PeriodEnd)`.
- `EmployeeSalaryAssignment`: `(TenantId, EmployeeId, EffectiveFrom, EffectiveTo)`.
- `PayrollRun`: `(TenantId, PayPeriodId, Status)`.
- `PayrollRunEmployee`: unique `(TenantId, PayrollRunId, EmployeeId)`.
- `PayrollRunComponent`: `(TenantId, PayrollRunEmployeeId, SalaryComponentId)`.

## Integrity Rules

Published payroll runs are immutable. Corrections create adjustment runs or correction
records. Source snapshots and rule-version snapshots must be retained. Statutory rule
versions are effective-dated and approval-controlled.

## RLS and Security

Payroll tables are tenant-scoped and require strict ABAC by payroll group, branch/office,
legal entity, role, and data sensitivity. Payslip access is employee-self or permitted
payroll/HR scope.

## Retention

Payroll and statutory records follow India statutory, tax, audit, and tenant retention
policy. Legal hold blocks purge.

## Acceptance Criteria

1. Payroll run data is reproducible and immutable after publish.
2. Salary assignment supports effective-dated CTC revisions.
3. Statutory rule versions are traceable to source reference and approval.
4. Payslip records link to exact run employee result.
5. RLS and ABAC block unauthorized payroll visibility.
6. Payroll run evidence can trace shift-aware attendance impact where configured.

## External References

- EPFO: https://www.epfindia.gov.in/site_en/index.php
- Income Tax Department: https://www.incometax.gov.in/iec/foportal/
- SQL Server temporal tables: https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - Payroll Domain Expert: ____ - Security Architect: ____ - Status: Approved
