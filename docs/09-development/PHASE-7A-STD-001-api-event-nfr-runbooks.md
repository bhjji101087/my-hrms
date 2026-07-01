# Phase 7A Standard - API, Event, NFR, and Runbook Hardening

Document Owner: Solution Architect / Integration Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved
> Applies to all Phase 7A module technical designs unless a stricter module document
> overrides it. This document converts the Phase 7A documentation review recommendations
> into a shared implementation standard.

## 1. API Contract Standard

Every Phase 7A API must follow `docs/20-standards/API_STANDARDS.md` and the following
enterprise additions:

- Base path: `/api/v1/...`.
- OpenAPI documentation is mandatory before development.
- Every response includes or propagates `CorrelationId`.
- Errors use the platform error envelope with ProblemDetails-compatible fields.
- Critical `POST`, `PUT`, `PATCH`, decision, publish, import, export, replay, payroll,
  and correction operations require `Idempotency-Key`.
- List APIs support pagination, sorting, filtering, and maximum page-size limits.
- Export APIs use asynchronous jobs for large/sensitive exports and define export limits.
- Tenant isolation behavior must be explicit: return `403` for authenticated-but-forbidden
  access and `404` where hiding cross-tenant resource existence is required by security
  policy.
- All mutating APIs must write audit records and produce events where the module contract
  requires them.

## 2. Event Contract Standard

Every Phase 7A domain event must include:

- `EventId`
- `EventName`
- `EventVersion`
- `TenantId`
- `CorrelationId`
- `CausationId`
- `ActorId`
- `ActorType`
- `SourceModule`
- `AggregateType`
- `AggregateId`
- `SchemaVersion`
- `OccurredAt`
- `IdempotencyKey`
- `ReplaySafety`
- `PiiClassification`

## 3. Event Governance

- Event ordering is guaranteed only where explicitly documented. Default is best-effort
  across aggregates; per-aggregate ordering must be preserved where payroll, ledger,
  workflow, or audit correctness depends on it.
- Consumers must be idempotent. Replay cannot be enabled for a consumer until idempotency
  tests pass.
- Breaking schema changes require a new event version and deprecation plan.
- Event payloads must be minimized; sensitive PII should use references where practical.
- Poison messages must move to dead-letter/quarantine after configured retry count.
- Dead-letter replay requires permission, reason, approval where sensitive, and audit.

## 4. Non-Functional Targets

Each module must define measurable targets before implementation:

- API P95 latency for normal user operations.
- Background job SLA and maximum retry window.
- Event publish latency and dead-letter response SLA.
- Maximum export size and timeout.
- Search/report query performance target.
- Payroll or batch run size target where applicable.
- Availability/degraded-mode behavior.
- Observability metrics, alerts, and dashboard expectations.

## 5. Operational Mini-Runbook Standard

Each module must include, directly or by reference, mini-runbooks for likely production
incidents:

- Symptoms and detection signal.
- Immediate containment.
- Owner and escalation path.
- Data safety checks.
- Replay, rollback, or compensating action.
- Customer communication trigger.
- Audit/evidence capture.
- Exit criteria and post-incident review.

Required Phase 7A runbook topics:

- Event bus dead-letter spike.
- Payroll run failure.
- Rule activation rollback.
- Workflow timer backlog.
- Report export failure.
- Audit search performance degradation.
- Connector sync failure.
- Configuration publish rollback.

## 6. Approval Requirement

This standard must be approved before Phase 7A development starts. Any module-specific
exception requires an ADR or explicit approval note in that module's technical design.

## External References

- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- CloudEvents: https://cloudevents.io/
- RabbitMQ reliability guide: https://www.rabbitmq.com/docs/reliability
- OpenTelemetry documentation: https://opentelemetry.io/docs/

References last validated: 2026-06-29.

## Approval

Solution Architect: ____ - Integration Architect: ____ - Security Architect: ____ - Status: Approved
