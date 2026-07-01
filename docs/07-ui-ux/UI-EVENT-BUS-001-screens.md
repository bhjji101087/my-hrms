# UI Design - Event Bus Operations

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 4 of 5 for Event Bus and Outbox.

## UX Goals

Operational users need clear visibility into event health without dealing with broker
internals. The UI must support troubleshooting, replay, and contract review while keeping
tenant data protected.

## Screen A - Event Health Dashboard

Shows outbox pending count, publish latency, consumer lag, retry rate, dead-letter count,
broker status, and event throughput by tenant/module. High-risk conditions link to runbook
and affected events.

## Screen B - Event Catalog

Lists event type, version, publisher, known consumers, schema status, classification,
compatibility, and lifecycle state. Users can open schema and sample payload with masking.

## Screen C - Dead-Letter Queue

Shows failed event metadata, reason, retry history, last error, payload classification, and
recommended action. Replay requires permission, reason, optional approval, and audit.

## Screen D - Replay Request

Guided flow to choose tenant, event type, date range, aggregate, reason, dry-run preview,
approval route, and execution status. Bulk replay is disabled until dry-run passes.

## Screen E - Event Trace

Displays one event from original command through outbox, broker publish, consumer inbox,
side effects, audit records, and downstream events using correlation and causation IDs.

## Acceptance Criteria

1. Support user can identify dead-letter events and failure reasons.
2. Replay requires reason and is audited.
3. Event catalog clearly shows version and compatibility.
4. Sensitive payload fields are masked unless permitted.
5. Event trace reconstructs cross-module flow.

## External References

- OpenTelemetry documentation: https://opentelemetry.io/docs/
- CloudEvents: https://cloudevents.io/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

UX/UI Architect: ____ - Integration Architect: ____ - Product Owner: ____ - Status: Approved
