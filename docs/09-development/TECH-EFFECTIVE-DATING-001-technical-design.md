# Technical Design - Effective Dating and Bitemporal Core

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: Solution Architect (Agent 6)
Created Date: 2026-06-28
Last Updated: 2026-06-28
Version: 1.1
Status: Approved

> Doc 2 of 5 for Effective Dating. Implements FEAT-EFFECTIVE-DATING-001 and ADR-007.

## Design Goals

Provide one reusable platform capability for effective-dated data so Core HR, Leave,
Attendance, Payroll, Workflow, Rule Engine, Configuration-as-Data, Audit, and Reports use
the same lifecycle, validation, query, and correction model.

## Architecture

The platform shall expose an internal `IEffectiveDatedRepository<T>` and
`IAsOfQueryService` used by modules through application services. SQL Server temporal
tables are preferred for system-time history where table shape supports it. Valid-time
periods are modelled explicitly through `EffectiveFrom` and `EffectiveTo`.

```text
API -> Application Service -> Effective Dating Service -> Repository -> SQL Server
                                      |                     |
                                      +-> Audit/Event Bus   +-> Temporal History
```

## Core Components

- Effective Dating Service: validates periods, schedules changes, closes old versions,
  and supports correction workflows.
- As-Of Query Service: resolves records for a business date and optional system time.
- Period Validator: prevents overlaps and open-ended duplicates.
- Impact Analyzer: identifies payroll, workflow, rule, reporting, or compliance impact.
- Change Approval Adapter: routes sensitive corrections through Workflow Studio.
- Concurrency Guard: verifies `rowversion` or equivalent concurrency tokens before write.
- Bulk Operation Processor: executes approved large-scale effective-dated changes in
  chunks with progress tracking and retry support.
- Temporal History Provider: abstracts SQL Server temporal tables and approved fallback
  history mechanisms.
- Explain History Builder: produces a standard business-valid and system-known response.
- Event Publisher: writes `EffectiveDatedRecordChanged` and module-specific events through
  the Outbox pattern.

## API Requirements

Business APIs shall support optional `asOfDate` where historical reads are useful.
Administrative APIs shall support future-dated create/update, backdated correction,
supersede, cancel future change, and explain-history operations. OpenAPI must document
date semantics clearly. Critical write operations must accept idempotency keys and the
expected concurrency token when updating an existing effective-dated chain.

## Data and Transaction Rules

- A change creates a new version rather than overwriting business history.
- Backdated changes must run in a transaction with impact analysis and audit capture.
- Current record means `EffectiveFrom <= businessDate` and `EffectiveTo is null or >=
  businessDate`.
- System-time history is used for "what did the system know then"; valid-time history is
  used for "what was true then."
- Idempotency keys are required for correction commands submitted by clients or jobs.
- Each write transaction must persist the new effective-dated row, closure of affected
  rows, audit entry, and outbox event atomically.

## Date and Time Semantics

`EffectiveFrom` and `EffectiveTo` represent tenant-local business dates, stored as DATE
values by default. They do not represent the user's browser time zone, the application
server's local time zone, or an instant in UTC. Modules use the tenant's approved time
zone and calendar context when interpreting scheduled future changes, payroll periods,
workflow evaluations, reports, rules, and analytics.

System, audit, integration, and temporal-history timestamps represent instants and are
stored in UTC where applicable. API responses may render localized display values, but the
persisted system-time values remain UTC so historical reconstruction is consistent across
regions, workers, and integrations.

Sub-day business effective periods are out of scope for the default platform model. Any
entity requiring DATETIME-style valid time must define that exception in approved feature,
technical, database, API, and test documentation before implementation.

## Effective-Date Boundary Rules

All effective-dated entities use the same valid-time boundary rules unless an approved
exception exists:

- `EffectiveFrom` is inclusive.
- `EffectiveTo` is inclusive when present.
- `EffectiveTo = NULL` means the period is open-ended.
- A record is active for `asOfDate` when `EffectiveFrom <= asOfDate` and
  (`EffectiveTo is NULL` or `EffectiveTo >= asOfDate`).
- Adjacent periods are valid when the previous `EffectiveTo` is the tenant-local date
  immediately before the next `EffectiveFrom`.
- For single-active entities, overlap exists when two periods for the same tenant-scoped
  business key share any valid date.
- Creating a new current or future record for a single-active entity closes the previous
  open record by setting `EffectiveTo` to the date immediately before the new
  `EffectiveFrom`.
- `EffectiveFrom <= EffectiveTo` is required when `EffectiveTo` is not `NULL`.
- Zero-length periods are rejected unless the entity explicitly supports same-day
  point-in-time business validity through approved design documentation.

The Period Validator must apply these rules consistently for API requests, service calls,
workflow actions, imports, scheduled jobs, and direct repository writes.

## Concurrency and Conflict Resolution

Effective-dated write paths use optimistic concurrency. SQL Server `rowversion` is the
default concurrency token; an equivalent approved token may be used by adapters that do
not store data in SQL Server.

Before persisting a change, the Effective Dating Service shall:

- Load the target effective-dated chain using tenant context and the expected business key.
- Verify the submitted `rowversion` or equivalent token for the row or chain being changed.
- Re-run overlap, boundary, open-ended, approval, and impact validations against the latest
  committed state.
- Reject the write if the chain changed after the client or job read it.

Conflict behavior is standardized:

- User/API writes return a concurrency conflict response and the latest safe summary needed
  for reconciliation.
- Automated jobs may retry only when the command is idempotent and all validations pass
  against the latest state.
- Backdated corrections, payroll-impacting changes, and approved workflow actions are not
  silently merged; they require user or workflow reconciliation after a conflict.
- Lost updates are prevented for future-dated records, current records, and historical
  corrections by requiring the concurrency check and idempotency key before commit.

## Bulk Effective-Dated Operations

The platform shall support a reusable bulk-operation design for large effective-dated
changes such as annual salary revisions, company-wide policy changes, organization
restructuring, shift calendar updates, and holiday calendar updates.

Bulk operations are modelled as governed jobs with:

- A tenant-scoped batch ID, operation type, initiator, reason, approval reference, and
  idempotency key.
- Pre-validation of the requested change set before execution begins.
- Chunked execution by configurable batch size and tenant-scoped business key range.
- One transaction per chunk, with each affected row change, audit entry, and outbox event
  committed atomically.
- Item-level status tracking for pending, succeeded, failed, skipped, retried, and
  cancelled records.
- Partial failure handling that preserves successful committed chunks and isolates failed
  items for review or retry.
- Retry and recovery using idempotency keys, batch state, chunk sequence, and last
  committed checkpoint.
- Progress tracking for total records, processed records, success count, failure count,
  current chunk, started at, updated at, completed at, and cancellation state.

Bulk operations must use the same Effective Dating Service, Period Validator, Impact
Analyzer, Change Approval Adapter, audit capture, RBAC, ABAC, tenant isolation, and Outbox
Publisher as individual updates. Bulk implementation details, import formats, and UI flows
will be finalized in a future feature or technical design where needed.

## Temporal History Fallback Strategy

SQL Server temporal tables are the preferred system-time mechanism for effective-dated
entities whose table shape supports temporal history. Some entities may require a fallback
because of storage limitations, integration boundaries, high-volume append-only behavior,
or module-specific persistence constraints.

Supported fallback approaches are:

- Manual history tables that mirror the current table and store previous row versions with
  system-valid timestamps, user, reason, and correlation metadata.
- Audit history tables for entities where full row reconstruction can be derived from
  audited field changes.
- Event-based history where immutable domain events are sufficient to reconstruct the
  system-known state.
- Hybrid approaches that combine valid-time rows, audit metadata, and events for
  reconstruction.

Fallback implementations must expose the same `ITemporalHistoryProvider` contract as SQL
Server temporal tables. They must support tenant filtering, RBAC/ABAC, audit references,
retention/legal-hold policy, explain-history operations, and acceptance tests proving that
historical reconstruction remains consistent.

## Explain History Response Contract

Explain-history operations shall return a common response shape across modules. The
contract is logical and may be represented in REST, internal DTOs, reports, or audit views.

Required fields:

- Entity name and tenant-scoped business key.
- `asOfDate` used for valid-time evaluation.
- Optional system-known timestamp used for bitemporal reconstruction.
- Business-valid value for the requested date.
- System-known value for the requested system time, when requested.
- Effective period: `EffectiveFrom`, `EffectiveTo`, and open-ended indicator.
- Correction reason or change reason.
- Changed by and changed at UTC.
- Approval reference, when approval was required.
- Impacted downstream modules such as Payroll, Workflow, Reporting, Notifications, or
  integrations.
- Audit reference and correlation ID.
- Source history provider, such as temporal table, manual history, audit, event, or hybrid.

The response must be tenant-scoped, RBAC/ABAC-filtered, and safe for the caller's
permission level. Sensitive fields may be redacted while preserving the explanation
metadata needed for audit and support.

## Event Ordering and Delivery Guarantees

Effective-dated writes publish events through the transactional Outbox pattern approved in
ADR-009. The database transaction writes the effective-dated change, audit record, and
outbox message together. A dispatcher publishes from the outbox only after the transaction
commits.

Event guarantees:

- Delivery is at-least-once; consumers must be idempotent.
- Ordering is guaranteed only within a tenant-scoped aggregate or business key where the
  selected broker supports sessions or equivalent sequencing.
- Global ordering across tenants, modules, or unrelated entities is not guaranteed.
- Events include event ID, tenant ID, aggregate type, aggregate ID or business key, event
  type, schema version, aggregate version or sequence number, effective period, correlation
  ID, causation ID, idempotency key, and occurred-at UTC timestamp.
- Duplicate event protection is based on event ID, idempotency key, aggregate version, and
  consumer processed-message records.
- Consumers must ignore or safely reconcile stale events when a later aggregate version has
  already been processed.
- Dispatcher retry uses bounded retries with backoff and monitoring.
- Poison messages move to a dead-letter queue with tenant, correlation, error, and retry
  metadata for controlled replay or remediation.
- Payroll, Workflow, Reporting, Notifications, and integrations consume the same event
  contract and must not rely on module-specific side channels for effective-dated changes.

## Security and Governance

All queries must be tenant-scoped and pass RBAC/ABAC checks. Sensitive history can be more
restricted than current data. Backdated or payroll-impacting changes require reason and
may require maker-checker approval based on tenant policy.

## Observability

Capture correlation ID, tenant ID, entity name, operation type, period changed, impact
classification, approval reference, and latency. Alerts shall trigger for period overlap
exceptions, failed temporal-history writes, and repeated backdated corrections.
Bulk jobs shall also expose progress, failure count, retry count, current chunk, and
recovery state. Event dispatch metrics shall include outbox lag, publish retries,
dead-letter count, duplicate suppressions, and consumer idempotency failures.

## Extension Points

Future modules register effective-dated entities through metadata: entity name, date
columns, overlap policy, approval policy, audit classification, and event mapping. Core
services remain closed for direct module modification.

## Acceptance Criteria

1. Shared services handle future, current, and backdated changes for at least three modules.
2. As-of query behavior is identical across API, reporting, rule, and payroll consumers.
3. Sensitive corrections route through Workflow Studio without module-specific code.
4. Temporal history can reconstruct previous persisted values.
5. OpenAPI documents `asOfDate` and correction endpoints.
6. Concurrent updates using stale `rowversion` or equivalent tokens are rejected before
   commit and cannot overwrite future-dated or backdated corrections.
7. Valid-time boundaries use DATE values, inclusive `EffectiveFrom`, inclusive
   `EffectiveTo`, `EffectiveTo = NULL` for open-ended records, and shared overlap rules.
8. Bulk effective-dated operations execute in chunks, track progress, support retry and
   recovery, and report partial failures without bypassing validation, approval, audit, or
   event publication.
9. Entities that cannot use SQL Server temporal tables expose an approved temporal-history
   fallback through the same history provider contract.
10. Explain-history responses include business-valid value, system-known value, reason,
    changed-by/changed-at, approval reference, impacted modules, audit reference, and
    correlation ID.
11. Effective-dated events are persisted through the Outbox pattern, carry ordering and
    idempotency metadata, retry safely, and support dead-letter handling.

## External References

- SQL Server temporal tables: https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
- EF Core temporal tables: https://learn.microsoft.com/en-us/ef/core/providers/sql-server/temporal-tables
- Microsoft row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security

References last validated: 2026-06-28.

## Approval

Solution Architect: Approved by Codex 2026-06-28 - .NET Architect: Approved by Codex 2026-06-28 - Security Architect: Approved as aligned with tenant, audit, RBAC/ABAC, and event-governance controls 2026-06-28 - Status: Approved
