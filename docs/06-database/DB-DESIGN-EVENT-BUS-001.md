# Database Design - Event Bus and Outbox

Module: Platform Foundation
Schema: `integration`
Phase: 7A / Sprint S2
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Event Bus and Outbox.

## Tables

```text
integration.EventContract
  EventContractId, TenantId, EventType, EventVersion, PublisherModule,
  PayloadSchemaJson, Classification, CompatibilityStatus, IsActive, audit columns

integration.OutboxEvent
  OutboxEventId, TenantId, EventId, EventType, EventVersion, AggregateType,
  AggregateId, PayloadJson, PayloadHash, Classification, CorrelationId,
  CausationId, OccurredAt, PublishStatus, RetryCount, NextRetryAt,
  PublishedAt, LastError, audit columns

integration.InboxMessage
  InboxMessageId, TenantId, EventId, ConsumerName, ProcessedAt,
  ProcessingStatus, RetryCount, LastError, audit columns

integration.DeadLetterEvent
  DeadLetterEventId, TenantId, OutboxEventId, EventId, EventType,
  FailureReason, FailurePayloadReference, ReplayStatus, ReplayApprovedBy,
  ReplayReason, audit columns

integration.EventReplayRequest
  ReplayRequestId, TenantId, EventType, FilterJson, Reason,
  Status, RequestedBy, ApprovedBy, StartedAt, CompletedAt, audit columns
```

## Indexes

- `OutboxEvent`: `(PublishStatus, NextRetryAt)`, `(TenantId, AggregateType, AggregateId)`,
  unique `(TenantId, EventId)`.
- `InboxMessage`: unique `(TenantId, EventId, ConsumerName)`.
- `DeadLetterEvent`: `(TenantId, EventType, CreatedDate desc)`.
- `EventContract`: unique `(TenantId, EventType, EventVersion)`.

## Retention

Outbox events can be archived after confirmed publish and retention window. Dead-letter,
replay, and audit-critical integration records follow compliance retention. Payloads with
sensitive data may be minimized or stored through protected references.

## RLS and Security

All tables include tenant filtering. Operational users can see event metadata only within
permissions. Sensitive payload access requires elevated support or security permission and
is audited.

## Migration Rules

Event contract changes require versioned migration and compatibility review. Removing or
renaming events is prohibited without deprecation plan.

## Acceptance Criteria

1. Business transaction and outbox insert are atomic.
2. Duplicate event IDs are rejected.
3. Inbox unique key prevents duplicate consumer side effects.
4. Dead-letter and replay records preserve reason and approval.
5. Tenant RLS applies to event operations.

## External References

- RabbitMQ reliability guide: https://www.rabbitmq.com/docs/reliability
- CloudEvents: https://cloudevents.io/

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - Integration Architect: ____ - Security Architect: ____ - Status: Approved
