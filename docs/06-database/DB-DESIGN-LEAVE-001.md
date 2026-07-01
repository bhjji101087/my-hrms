# Database Design - Leave Management

Module: Leave
Schema: `leave`
Phase: 7A / Sprint S5
Owner: Database Architect (Agent 7)
Created Date: 2026-06-14
Last Updated: 2026-06-28
Version: 2.0
Status: Approved
> Doc 3 of 5 for Leave Management.

## Tables

```text
leave.LeaveType
  LeaveTypeId, TenantId, Code, Name, Unit, PaidFlag, Color,
  CurrentPolicyVersionId, IsActive, audit columns

leave.LeavePolicyVersion
  LeavePolicyVersionId, TenantId, LeaveTypeId, EffectiveFrom, EffectiveTo,
  AccrualRuleSetId, EligibilityRuleSetId, DayCountRuleSetId,
  CarryForwardRuleSetId, ApprovalWorkflowDefinitionId, Status, audit columns

leave.HolidayCalendar
  HolidayCalendarId, TenantId, Code, Name, LocationId, EffectiveFrom, EffectiveTo, audit columns

leave.Holiday
  HolidayId, TenantId, HolidayCalendarId, HolidayDate, Name, HolidayType, audit columns

leave.LeaveRequest
  LeaveRequestId, TenantId, EmployeeId, LeaveTypeId, FromDate, ToDate,
  DurationUnits, Reason, Status, WorkflowInstanceId, IdempotencyKey,
  PayrollImpactStatus, audit columns

leave.LeaveTransaction
  LeaveTransactionId, TenantId, EmployeeId, LeaveTypeId, LeaveRequestId,
  TransactionType, Amount, EffectiveDate, Reason, SourceReference,
  IdempotencyKey, audit columns

leave.LeaveBalanceProjection
  LeaveBalanceProjectionId, TenantId, EmployeeId, LeaveTypeId,
  AvailableAmount, ReservedAmount, UsedAmount, AsOfDate, RebuiltAt, audit columns
```

## Indexes

- `LeaveType`: unique `(TenantId, Code)`.
- `LeavePolicyVersion`: `(TenantId, LeaveTypeId, EffectiveFrom, EffectiveTo)`.
- `LeaveRequest`: `(TenantId, EmployeeId, FromDate, ToDate)`, unique `(TenantId, IdempotencyKey)`.
- `LeaveTransaction`: `(TenantId, EmployeeId, LeaveTypeId, EffectiveDate)`,
  unique `(TenantId, IdempotencyKey)`.
- `LeaveBalanceProjection`: unique `(TenantId, EmployeeId, LeaveTypeId)`.

## Integrity Rules

Balance is never manually overwritten. It is derived from ledger transactions and cached
in projection. Overlap checks run in transaction with date/calendar rules. Policy versions
are effective-dated and immutable after publish.

## RLS and Security

All tables include TenantId and RLS. Balance adjustments, payroll-impacting corrections,
and policy publication require elevated permissions and audit.

## Acceptance Criteria

1. Ledger can rebuild balance projection.
2. Duplicate requests cannot double-reserve balance.
3. Policy versions support historical and future-dated rules.
4. Holiday calendars are tenant/location scoped.
5. RLS blocks cross-tenant leave data.

## External References

- SQL Server temporal tables: https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
- SQL Server row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - Solution Architect: ____ - HR Domain Expert: ____ - Status: Approved
