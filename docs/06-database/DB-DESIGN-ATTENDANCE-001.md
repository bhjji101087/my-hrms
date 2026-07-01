# Database Design - Attendance and First Connector

Module: Attendance
Schema: `attendance`
Phase: 7A / Sprint S6
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Attendance.

## Tables

```text
attendance.AttendancePolicyVersion
  AttendancePolicyVersionId, TenantId, Code, EffectiveFrom, EffectiveTo,
  RuleSetId, CalendarId, Status, audit columns

attendance.AttendanceDevice
  AttendanceDeviceId, TenantId, ProviderCode, DeviceExternalId,
  Name, LocationId, Status, LastSyncAt, ConnectorConfigReference, audit columns

attendance.RawPunch
  RawPunchId, TenantId, EmployeeId, AttendanceDeviceId, ExternalPunchId,
  PunchTime, Direction, SourceType, PayloadHash, IsDuplicate, audit columns

attendance.AttendanceDaySummary
  AttendanceDaySummaryId, TenantId, EmployeeId, AttendanceDate,
  Status, FirstInTime, LastOutTime, WorkMinutes, LateMinutes,
  EarlyLeaveMinutes, ShiftDefinitionVersionId, RuleSetVersionId,
  PayrollImpactStatus, audit columns

attendance.RegularizationRequest
  RegularizationRequestId, TenantId, EmployeeId, AttendanceDate,
  RequestedInTime, RequestedOutTime, Reason, Status,
  WorkflowInstanceId, audit columns

attendance.ConnectorSyncRun
  ConnectorSyncRunId, TenantId, AttendanceDeviceId, StartedAt, CompletedAt,
  Status, RecordsFetched, RecordsAccepted, RecordsRejected,
  CheckpointValue, ErrorSummary, audit columns
```

## Indexes

- `RawPunch`: unique `(TenantId, SourceType, ExternalPunchId)`,
  `(TenantId, EmployeeId, PunchTime)`.
- `AttendanceDaySummary`: unique `(TenantId, EmployeeId, AttendanceDate)`.
- `RegularizationRequest`: `(TenantId, EmployeeId, Status, AttendanceDate)`.
- `ConnectorSyncRun`: `(TenantId, AttendanceDeviceId, StartedAt desc)`.

## Integrity Rules

Raw punches are immutable. Corrections are represented by regularization approvals and
recalculated summaries. Payroll-impacting summary changes are evented and audited.
Shift definitions, employee shift assignment, overrides, and shift resolution history are
defined in `DB-DESIGN-SHIFT-FOUNDATION-001`.

## RLS and Security

All tables include TenantId and RLS. Device connector config stores secret references only.
Manager/team visibility is ABAC-enforced.

## Acceptance Criteria

1. Duplicate external punches are rejected or marked without double counting.
2. Daily summary is rebuildable from raw punches plus approved adjustments.
3. Connector sync runs are auditable and traceable.
4. RLS blocks cross-tenant attendance records.
5. Payroll-impacting changes are identifiable.
6. Attendance summaries can reference the effective shift version used for calculation.

## External References

- SQL Server row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
- RabbitMQ reliability: https://www.rabbitmq.com/docs/reliability

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Phase 7A Shift Foundation Addendum

Attendance database implementation must comply with
`docs/06-database/DB-DESIGN-SHIFT-FOUNDATION-001.md`.

## Approval

Database Architect: ____ - Integration Architect: ____ - Security Architect: ____ - Status: Approved
