# Test Plan - Effective Dating and Bitemporal Core

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Last Updated: 2026-06-28
Version: 1.1
Status: Approved

> Doc 5 of 5 for Effective Dating. Covers FEAT/TECH/DB/UI-EFFECTIVE-DATING-001.

## Scope

Validate future-dated, current, backdated, corrected, cancelled, and historical records
across API, database, UI, audit, events, rules, workflow, payroll, and reports.

This test plan validates shared platform behavior. It must be reusable for HR, Payroll,
Leave, Attendance, Workflow, Rules, Configuration, and future effective-dated entities
without introducing module-specific business logic.

## Functional Tests

- Create future-dated employee assignment and verify activation by date.
- Correct historical salary and verify old and new versions remain traceable.
- Cancel pending future change before activation.
- Prevent overlapping periods for a single-active employee assignment.
- Retrieve employee and policy data using `asOfDate`.
- Route sensitive correction through workflow approval.
- Verify open-ended active records use `EffectiveTo = NULL`.
- Verify creating a current or future record closes the previous open record where the
  entity follows a single-active-period model.
- Verify status transitions for Current, Future, Historical, Corrected, Superseded, and
  Cancelled versions.

## Bitemporal Time Travel Tests

- Validate business-date queries independently from system-time queries.
- Query the same entity for the same `asOfDate` at two different system times and verify
  that "what was true" and "what the system knew then" are reconstructed correctly.
- Verify backdated corrections change future business-date answers without rewriting the
  earlier system-known record.
- Verify explain-history responses include business-valid value, system-known value,
  changed by, changed at, reason, approval reference, impacted modules, audit reference,
  and correlation ID.
- Verify temporal fallback providers produce the same explain-history behavior as SQL
  Server temporal tables.

## Time Zone and Calendar Boundary Tests

- Validate tenant-local effective dates against UTC system timestamps.
- Verify scheduled activation works correctly when the tenant time zone differs from the
  server, worker, or user browser time zone.
- Test date boundaries around daylight saving transitions for tenants in affected regions.
- Test leap-year dates, including February 29.
- Test month-end, quarter-end, financial-year-end, and calendar-year-end boundaries.
- Verify adjacent periods where the previous `EffectiveTo` is the tenant-local date
  immediately before the next `EffectiveFrom`.
- Verify invalid boundary values are rejected consistently across UI, API, service, and
  database paths.

## Database Tests

- Temporal table current/history queries return expected values.
- RLS blocks current and historical rows from another tenant.
- Period validation prevents overlap under concurrent writes.
- Migration enables system versioning without data loss.
- Retention job respects legal hold and protected history.
- Database `CHECK` constraints reject invalid effective periods and invalid status values.
- Filtered unique indexes or approved equivalents prevent more than one open-ended active
  record for single-active entities.
- `EntityBusinessKey` groups all versions of the same business fact without confusing it
  with the surrogate primary key.
- UTC system timestamps are stored for audit, temporal period columns, and system events.

## Optimistic Concurrency Tests

- Simulate simultaneous updates to the same effective-dated chain and verify stale
  `VersionNumber` or row-version tokens are rejected.
- Verify concurrent future-dated changes cannot silently overwrite each other.
- Verify concurrent backdated corrections require conflict resolution instead of silent
  merge.
- Verify conflict responses include enough safe information for user or workflow
  reconciliation.
- Verify idempotency keys prevent duplicate writes during retry.

## Rollback and Transaction Recovery Tests

- Force failure after period validation but before commit and verify no partial records are
  persisted.
- Force failure after record write but before audit or outbox persistence and verify the
  full transaction rolls back.
- Force failure during previous-open-record closure and verify the new row is not committed
  without the closure.
- Verify retry after rollback produces one consistent effective-dated chain.
- Verify recovery jobs do not create duplicate audit records or events.

## Supersession Chain Tests

- Apply multiple successive corrections to the same business key and verify the full
  supersession chain remains traceable.
- Verify superseded records remain immutable and read-only.
- Verify self-supersession and circular supersession attempts are rejected.
- Verify explain-history and compare views can traverse from original version to latest
  approved version.

## Soft Delete Behavior Tests

- Soft-delete an effective-dated record and verify normal current queries exclude it.
- Verify temporal history, audit history, and approved historical queries still show the
  deleted record where the caller has permission.
- Verify soft delete creates audit and system-time evidence.
- Verify legal hold prevents purge or anonymization while allowing authorized historical
  reconstruction.
- Verify soft delete does not break supersession chains.

## Security Tests

- Employee sees permitted self history only.
- Manager sees team history only.
- Payroll-impacting change requires elevated permission.
- Sensitive history fields are masked when ABAC denies access.
- Audit records include before/after values, reason, approver, and correlation ID.
- Unauthorized users cannot access `asOfDate`, explain-history, compare, correction, bulk,
  or audit drawer data.
- Cross-tenant requests cannot infer existence of another tenant's historical records.

## Integration Tests

- Rule Engine evaluates policy as of the correct date.
- Workflow uses version pinned to effective date.
- Payroll run uses salary as of pay period.
- Event Bus emits effective-dated change events once.
- Reports reconstruct historical state.

## Bulk Effective-Dated Operation Tests

- Validate large change sets before execution and report success, warning, conflict, and
  error counts.
- Verify bulk operations follow the same effective-date validation, overlap prevention,
  approval, audit, RBAC, ABAC, tenant isolation, and event rules as individual changes.
- Verify chunked execution commits successful chunks and isolates failed items for review.
- Verify partial failures do not leave inconsistent effective-dated chains.
- Verify retry and recovery use idempotency keys and batch checkpoints.
- Verify progress tracking reports queued, validating, awaiting approval, processing,
  partially failed, completed, cancelled, and failed states.
- Verify performance remains within approved batch-size and SLA limits for mass updates.

## API Contract Tests

- Validate OpenAPI examples for as-of reads, future-dated writes, backdated corrections,
  cancellation, supersession, compare, and explain-history operations.
- Test valid and invalid `asOfDate` values, including missing, malformed, out-of-range, and
  unauthorized historical date requests.
- Verify API rejects invalid effective periods, missing reasons, missing approvals,
  unsupported zero-length periods, overlapping periods, stale concurrency tokens, and
  malformed payloads.
- Verify error responses use the platform error envelope with validation details,
  correlation ID, and safe messages.
- Verify permission failures return the correct unauthorized or forbidden response without
  leaking sensitive history.

## Event Bus Reliability Tests

- Verify effective-dated changes write audit and outbox records in the same transaction.
- Verify dispatcher retries failed publication without duplicating business changes.
- Verify duplicate delivery is safely ignored by idempotent consumers.
- Verify event ordering within a tenant-scoped aggregate or business key where broker
  sequencing is configured.
- Verify dead-letter handling captures tenant, correlation, error, retry, and event
  metadata.
- Verify consumers achieve exactly-once effective business effect through idempotency,
  even when delivery is at-least-once.

## UI Tests

- History Timeline displays Current, Future, Historical, Corrected, Superseded, and
  Cancelled versions with standard labels, semantic tokens, icons, and accessible text.
- Compare Versions View shows old value, new value, changed by, reason, and effective date
  for each changed field.
- As-Of Mode shows a persistent "Viewing Historical Data" indicator and return-to-current
  action.
- Change Impact Panel displays Informational, Warning, Payroll Impact, and Compliance
  Impact levels without color-only signaling.
- Effective Date Preview shows activation date and which current record will close.
- Real-time overlap detection blocks submit until conflicts are resolved.
- Historical versions are read-only; Copy Previous Version and Restore as New Change
  create new effective-dated versions.
- Unsaved effective-dated changes warn before navigation away.
- Audit Information Drawer shows changed by, approved by, reason, workflow, change
  request, audit reference, and timestamps.
- Responsive behavior works for Timeline, Compare View, Date Picker, Impact Panel, Audit
  Drawer, and Bulk Validation Summary on mobile, tablet, and desktop.
- Keyboard accessibility, focus order, screen-reader labels, live regions, touch target
  sizes, localization, RTL readiness, and WCAG 2.2 AA compliance are verified.

## Negative Tests

- Reject invalid dates, missing `EffectiveFrom`, invalid `EffectiveTo`, unsupported
  zero-length periods, and malformed date formats.
- Reject missing reason for backdated or sensitive corrections.
- Reject missing approval when tenant policy requires approval.
- Reject overlapping periods for single-active entities.
- Reject unauthorized access to history, correction, compare, bulk, audit, or as-of
  endpoints.
- Reject invalid state transitions such as cancelled to active without a new change,
  historical edit, self-supersession, and circular supersession.
- Reject malformed API requests, invalid status values, invalid business keys, stale
  `VersionNumber`, and duplicate non-idempotent submissions.
- Verify failed validation never writes partial audit, outbox, current, or history data.

## Performance Tests

- Current as-of lookup P95 under 200 ms for indexed entities.
- High-volume employee history query paginates correctly.
- Backdated correction impact analysis completes within approved SLA.
- Long-running historical queries provide progress or safe timeout behavior.
- High-volume temporal history tables remain queryable with approved indexes and
  partitioning strategy where required.
- Bulk operations meet approved chunk-size, retry, and progress-update expectations.
- Reports and analytics consume `asOfDate` without module-specific query behavior.

## Scalability and Large Data Volume Tests

- Seed large effective-dated histories across multiple tenants and verify tenant isolation,
  pagination, filtering, and query plans.
- Validate high-volume temporal history retrieval for payroll, attendance, audit, workflow,
  and future effective-dated entities.
- Verify long-running explain-history and compare operations do not block normal current
  record reads.
- Verify archival and retention policies do not degrade active as-of query performance
  beyond approved thresholds.

## Disaster Recovery and Backup Validation

- Restore a backup containing current, temporal history, audit, outbox, inbox, and
  supersession data and verify historical reconstruction still works.
- Verify restored data preserves tenant isolation and RBAC/ABAC behavior.
- Verify temporal history and audit evidence remain recoverable after restore operations.
- Verify tombstone, legal hold, and retention evidence remains consistent after restore.
- Verify event replay after restore does not duplicate effective-dated business effects.

## Regression Test Suite

Every new effective-dated entity must be registered into a shared regression suite before
implementation is considered complete. The suite must automatically validate:

- Business key grouping.
- Open-ended record rule.
- Effective-period boundary behavior.
- As-of query behavior.
- Bitemporal reconstruction.
- Overlap prevention.
- Concurrency conflict handling.
- Audit and approval evidence.
- RLS and RBAC/ABAC enforcement.
- Event publication and idempotent consumption.
- UI timeline and explain-history behavior where the entity has a UI surface.

## Exit Criteria

- Minimum 85% automated coverage on platform services.
- Zero cross-tenant leakage in temporal history tests.
- All overlap, correction, and audit scenarios pass.
- OpenAPI examples for as-of reads and correction commands are validated.
- Bitemporal, time zone, concurrency, rollback, supersession, soft delete, bulk, API,
  event reliability, UI, negative, scalability, DR, and regression scenarios pass.
- Every effective-dated entity included in implementation has passed the shared regression
  suite.

## External References

- SQL Server temporal tables: https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

References last validated: 2026-06-28.

## Approval

QA Architect: Approved by Codex 2026-06-28 - Solution Architect: Approved by Codex 2026-06-28 - Product Owner: Approved by Bhajan Lal 2026-06-28 - Status: Approved
