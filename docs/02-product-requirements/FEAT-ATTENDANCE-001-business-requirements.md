# Feature Specification - Attendance and First Connector

Feature Name: Attendance and First Connector
Module: Attendance
Phase: 7A / Sprint S6
Owner: Product Owner (Agent 2)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 1 of 5 for Attendance. Implements PRD FR-005.

## Purpose

Attendance captures work time, punch data, regularization, approval, and payroll-ready
attendance outcomes. Phase 7A must also prove the connector pattern using one attendance
device/provider adapter without hardcoding vendor behavior into core.

## Market and Enterprise Context

HRMS vendors commonly offer biometric integrations, web/mobile attendance, shift/holiday
handling, regularization requests, and payroll linkage. Customer issues often include
missed punches, poor device sync visibility, rigid regularization rules, wrong salary-day
calculation, and difficult connector setup.

## Scope

In scope:
- Web/manual attendance and import.
- One attendance connector adapter.
- Punch records, daily attendance summary, regularization workflow.
- Configurable late/early/absence rules through Rule Engine.
- Phase 7A Shift Foundation: shift definition, employee shift assignment, shift override,
  and shift-aware attendance calculation.
- Leave and holiday awareness.
- Payroll attendance input events.
- Connector health and sync status.

Out of scope:
- Advanced roster planning, auto scheduling, shift swap, workforce demand planning, and
  multi-week roster optimization.
- Offline mobile hardening.
- Multiple connector marketplace.
- Geofencing and face recognition unless approved later.

## Business Requirements

1. Attendance rules shall be tenant-configurable and effective-dated.
2. Punches shall be immutable raw records; corrections create new adjustment records.
3. Employees shall request regularization for missed/incorrect punches.
4. Managers/HR shall approve regularization through Workflow Studio.
5. Attendance outcomes shall feed payroll through event bus.
6. Connector adapter shall be replaceable without changing attendance core logic.
7. Connector failures shall be visible with retry and reconciliation support.
8. Attendance views shall respect tenant, employee, manager, location, and HR scope.
9. Attendance calculation shall use the employee's effective shift for the attendance date
   when Shift Foundation data exists.
10. Shift-aware late, early, absence, overtime, night shift, weekly-off, and payroll-impact
   outcomes shall be rule-driven where enabled by tenant policy.

## Acceptance Criteria

1. One connector imports punches through provider adapter and shows sync health.
2. Employee regularizes missed punch through workflow.
3. Attendance summary respects holiday, leave, and configured rules.
4. Payroll receives approved payable-day/absence signal.
5. Raw punch records are preserved and auditable.
6. Effective-dated employee shift assignment affects attendance calculation correctly.

## External References

- Keka market reference: https://www.keka.com/
- greytHR market reference: https://www.greythr.com/
- RabbitMQ reliability: https://www.rabbitmq.com/docs/reliability
- OpenTelemetry documentation: https://opentelemetry.io/docs/

References last validated: 2026-06-28.

## Approval

Product Owner: ____ - HR Operations Reviewer: ____ - Integration Architect: ____ - Status: Approved
