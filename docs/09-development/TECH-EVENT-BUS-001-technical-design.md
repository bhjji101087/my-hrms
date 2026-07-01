# Technical Design - Event Bus and Outbox

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: Integration Architect (Agent 15)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Event Bus and Outbox. Implements FEAT-EVENT-BUS-001 and ADR-009.

## Architecture

Phase 7A uses a transactional outbox with RabbitMQ as the first broker. Broker access is
hidden behind an `IEventBus` abstraction so Azure Service Bus can be adopted later without
changing module code.

```text
Module Command -> DB Transaction -> Domain Change + OutboxEvent
                                      |
                              Outbox Publisher -> RabbitMQ -> Consumers
                                                         |
                                               Inbox/Idempotency Store
```

## Components

- Event Contract Registry: event name, version, schema, publisher, consumers, retention.
- Outbox Writer: stores event in same transaction as business change.
- Outbox Publisher Worker: publishes pending events with retry and backoff.
- Broker Adapter: RabbitMQ first, Azure Service Bus later through the same interface.
- Inbox Store: prevents duplicate consumer side effects.
- Dead-Letter Manager: stores failure reason, retry count, and replay status.
- Event Replay Service: controlled tenant-scoped replay.

## Event Contract Standard

Events should align with CloudEvents-style metadata:

- `eventId`, `eventType`, `eventVersion`
- `tenantId`, `aggregateType`, `aggregateId`
- `occurredAt`, `correlationId`, `causationId`
- `producer`, `payloadSchema`, `classification`
- `payload`

## Reliability Rules

- At-least-once delivery is assumed; consumers must be idempotent.
- Publishing from application code directly to broker is prohibited.
- Consumers must not perform cross-module writes without a documented command boundary.
- Long-running consumers use checkpointing and retry policy.
- Dead-letter replay requires permission, reason, and audit.

## Security

Events are tenant-scoped. Sensitive payloads should carry references or minimized fields,
not unnecessary PII. Broker credentials are stored in approved secret storage. Consumers
re-validate authorization when acting on protected data.

## Observability

Metrics: outbox pending count, publish latency, consumer lag, retry count, dead-letter
count, replay count, broker availability, event processing duration. Distributed tracing
uses correlation and causation IDs.

## Acceptance Criteria

1. RabbitMQ adapter works through `IEventBus`; module code has no broker-specific calls.
2. Outbox publisher resumes safely after process restart.
3. Consumer idempotency blocks duplicate side effects.
4. Dead-letter and replay operations are audited.
5. Event contracts are documented for OpenAPI/event catalog review.

## External References

- RabbitMQ reliability guide: https://www.rabbitmq.com/docs/reliability
- CloudEvents: https://cloudevents.io/
- OpenTelemetry: https://opentelemetry.io/docs/

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Integration Architect: ____ - Solution Architect: ____ - .NET Architect: ____ - Status: Approved
