# Feature Specification - Event Bus and Outbox

Feature Name: Event Bus and Outbox
Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: Product Owner (Agent 2)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 1 of 5 for Event Bus and Outbox. Implements PRD FR-009 and ADR-009.

## Purpose

Phase 7A modules must communicate without tight coupling. Attendance approval should feed
payroll, leave approval should update calendars and reports, payroll completion should
notify employees, and configuration changes should invalidate caches. Event Bus and Outbox
provide reliable event-driven integration.

## Market and Enterprise Context

Enterprise HR suites integrate attendance devices, payroll, notifications, workflow,
reports, and external systems. Customers become frustrated when changes require manual
sync, re-entry, delayed payroll inputs, or brittle point-to-point integrations. A reliable
event backbone is a foundational differentiator for future plug-and-play modules.

## Scope

In scope:
- Transactional outbox for reliable publish after database commit.
- Tenant-aware domain events.
- Event catalog and versioning.
- RabbitMQ first implementation with provider abstraction for Azure Service Bus.
- Idempotent consumers, retries, dead-letter handling, and replay governance.
- OpenTelemetry correlation through APIs, jobs, and events.

Out of scope:
- Public marketplace event subscriptions.
- Real-time analytics streaming platform.
- Direct module-to-module database access.

## Business Requirements

1. All Phase 7A modules shall publish approved domain events through the platform outbox.
2. Events shall include tenant, event type, event version, aggregate ID, correlation ID,
   causation ID, occurred time, and payload classification.
3. Consumers shall be idempotent and independently deployable.
4. Failed events shall move through retry and dead-letter workflows with operational visibility.
5. Event replay shall be controlled, audited, tenant-scoped, and permission-protected.
6. Event schemas shall be versioned and backward-compatible within a major API version.
7. Future modules shall subscribe through declared contracts instead of changing publishers.

## Key Phase 7A Events

- EmployeeCreated, EmployeeAssignmentChanged, EmployeeSalaryChanged
- LeaveRequested, LeaveApproved, LeaveRejected, LeaveCancelled
- AttendancePunchRecorded, AttendanceRegularized, AttendanceApproved
- PayrollRunStarted, PayrollRunCompleted, PayslipPublished
- RuleVersionPublished, WorkflowDefinitionPublished, ConfigurationPublished
- AuditRecordCreated, SecurityEventRecorded

## Acceptance Criteria

1. A database commit and outbox record are saved atomically.
2. A published event reaches at least one consumer and preserves correlation ID.
3. Duplicate delivery does not duplicate payroll, leave, audit, or notification effects.
4. Failed events are visible in an operational screen and can be replayed with approval.
5. Event schemas are documented and versioned.

## External References

- RabbitMQ reliability guide: https://www.rabbitmq.com/docs/reliability
- CloudEvents specification: https://cloudevents.io/
- Azure Service Bus overview: https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview
- OpenTelemetry documentation: https://opentelemetry.io/docs/

References last validated: 2026-06-28.

## Approval

Product Owner: ____ - Solution Architect: ____ - Integration Architect: ____ - Status: Approved
