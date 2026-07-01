# Technical Design - Attendance and First Connector

Module: Attendance
Phase: 7A / Sprint S6
Owner: .NET Architect (Agent 13)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Attendance.

## Architecture

Attendance owns punch ingestion, attendance calculation, regularization, and payroll input
events. Device/provider integration is implemented through connector adapters registered
by Configuration-as-Data.

```text
Connector/Web/API -> Punch Ingestion -> Attendance Engine -> Daily Summary
                           |                 |              |
                      Raw Punch Store      Rules        Payroll Events
                                        Shift Resolver
```

## Components

- Punch Ingestion Service: validates, deduplicates, stores raw punches.
- Connector Adapter Framework: provider-neutral import, health, retry, mapping.
- Attendance Calculation Engine: derives day status from rules, leave, holiday, and punches.
- Shift Resolver: resolves the employee's effective shift for the attendance date using
  Shift Foundation.
- Regularization Service: employee correction requests and workflow.
- Payroll Feed Publisher: publishes attendance outcomes.
- Reconciliation Service: identifies missing punches, duplicates, and sync gaps.

## Connector Strategy

First connector must implement a provider adapter interface: authenticate, fetch punches,
map employee/device IDs, checkpoint, retry, health check, and reconcile. Vendor-specific
logic stays in adapter, not core attendance domain.

## API Requirements

APIs under `/api/v1/attendance` cover punches, summaries, regularization, approvals,
connector configuration, sync status, reconciliation, shift definition/assignment
integration, and payroll impact preview. OpenAPI must document import idempotency,
connector health responses, and shift-related error responses.

## Security

Permissions include `Attendance.ViewSelf`, `Attendance.ViewTeam`, `Attendance.Manage`,
`Attendance.Regularize`, `Attendance.Approve`, and `Attendance.ConfigureConnector`.
Connector secrets use secure secret storage references.

## Events

`AttendancePunchRecorded`, `AttendanceSummaryCalculated`, `AttendanceRegularizationRequested`,
`AttendanceRegularizationApproved`, `AttendancePayrollImpactChanged`,
`AttendanceConnectorSyncFailed`, `EmployeeShiftAssigned`, `ShiftPayrollImpactChanged`.

## Observability

Metrics: punch ingestion count, duplicate count, connector sync lag, failed syncs,
regularization aging, calculation duration, payroll-feed publish latency.

## Acceptance Criteria

1. Connector adapter imports punches idempotently.
2. Raw punch data remains immutable.
3. Attendance summary calculation uses effective-dated rules.
4. Regularization uses Workflow Studio.
5. Payroll impact events are generated after approved summary changes.
6. Attendance summary uses the effective employee shift where Shift Foundation data exists.

## External References

- RabbitMQ reliability: https://www.rabbitmq.com/docs/reliability
- OpenTelemetry: https://opentelemetry.io/docs/
- JSON Schema: https://json-schema.org/

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Phase 7A Shift Foundation Addendum

Attendance must comply with `docs/09-development/TECH-SHIFT-FOUNDATION-001-technical-design.md`.
Full roster planning remains out of scope for Phase 7A.

## Approval

.NET Architect: ____ - Integration Architect: ____ - Security Architect: ____ - Status: Approved
