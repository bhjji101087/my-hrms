# Test Plan - Event Bus and Outbox

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 5 of 5 for Event Bus and Outbox.

## Functional Tests

- Business command writes outbox event in same transaction.
- Publisher publishes pending event after commit.
- Consumer processes event and records inbox message.
- Event catalog validates schema version.
- Dead-letter screen displays failed event metadata.

## Reliability Tests

- Application crash after DB commit but before publish eventually publishes event.
- Broker outage leaves events pending and resumes publishing after recovery.
- Duplicate event delivery does not duplicate consumer side effects.
- Consumer failure retries then dead-letters according to policy.
- Replay processes approved events and records audit trail.

## Security Tests

- Cross-tenant event operations are blocked by RLS and ABAC.
- Sensitive event payload fields are masked in UI and API.
- Replay without permission or reason is rejected.
- Broker credentials are not exposed in logs.

## Integration Tests

- Leave approval event updates reporting projection.
- Attendance approval event creates payroll input candidate.
- Payroll completion event publishes payslip notification trigger.
- Configuration publication event invalidates relevant caches.

## Performance Tests

- Outbox publish latency meets sprint S2 operational target.
- Consumer lag remains within target under Phase 7A event volume.
- Dead-letter search remains responsive under retained data volume.

## Exit Criteria

- Event Bus supports at-least-once delivery with idempotent consumers.
- All Phase 7A event contracts are listed and versioned.
- Operational dashboard and replay workflow pass E2E tests.
- Zero cross-tenant event visibility in automated security tests.

## External References

- RabbitMQ reliability guide: https://www.rabbitmq.com/docs/reliability
- CloudEvents: https://cloudevents.io/
- OpenTelemetry: https://opentelemetry.io/docs/

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

QA Architect: ____ - Integration Architect: ____ - Product Owner: ____ - Status: Approved
