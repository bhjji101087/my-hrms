# Technical Design - Workflow Studio

Module: Platform Foundation
Phase: 7A / Sprint S3-S9
Owner: Solution Architect (Agent 6)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Workflow Studio. Implements FEAT-WORKFLOW-001 and ADR-010.

## Architecture

Workflow Studio provides definition authoring and runtime orchestration. Business modules
start workflow instances and react to workflow outcome events. Workflow owns task lifecycle;
modules own business state transitions.

```text
Business Module -> Workflow Runtime -> Task Inbox / SLA / Escalation
        |                 |                    |
        +<- Outcome Event +-> Rule Engine      +-> Audit/Event Bus
```

## Components

- Definition Designer: creates graph/step definition and validates structure.
- Workflow Runtime: starts instances, advances tasks, evaluates conditions, manages state.
- Task Service: assignments, decisions, comments, delegation, reassignment.
- SLA Engine: timers, reminders, escalations, breach events.
- Migration Planner: handles in-flight instance migration with explicit approval.
- Rule Adapter: evaluates routing and condition rules through Rule Engine.
- Event Adapter: publishes workflow events through Outbox.

## Definition Lifecycle

Draft -> Validated -> Review -> Approved -> Published -> Superseded -> Retired.
Published definitions are immutable. New versions are effective-dated.

## API Requirements

APIs under `/api/v1/workflows` cover definition management, instance start/status, task
inbox, decisions, comments, delegation, reassignment, SLA configuration, and history.
OpenAPI must document workflow errors, idempotency, pagination, and task decision schemas.

## Runtime Rules

- Business modules pass business context and required outcome contract.
- Workflow does not directly mutate module records except through documented module command
  callbacks or events.
- Final decision is idempotent.
- Tasks cannot be approved by unauthorized or out-of-scope users.
- Running instances are pinned to workflow definition version.

## Observability

Metrics include started/completed instances, task aging, SLA breach count, escalation count,
decision latency, failed callbacks, and stuck instances. Traces follow correlation ID from
business request to workflow events.

## Acceptance Criteria

1. Workflow runtime supports leave, attendance, payroll, rule, and configuration workflows.
2. Task decisions enforce RBAC, ABAC, delegation, and tenant isolation.
3. SLA escalation and reminder jobs are observable and idempotent.
4. Workflow definitions are immutable after publish.
5. In-flight migration is controlled and audited.

## External References

- OMG BPMN: https://www.omg.org/spec/BPMN/
- OpenTelemetry: https://opentelemetry.io/docs/

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Solution Architect: ____ - .NET Architect: ____ - Security Architect: ____ - Status: Approved
