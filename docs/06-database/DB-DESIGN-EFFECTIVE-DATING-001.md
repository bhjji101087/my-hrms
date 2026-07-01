# Database Design - Effective Dating and Bitemporal Core

Module: Platform Foundation
Schema: `core`, `audit`
Phase: 7A / Sprint S2
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Last Updated: 2026-06-28
Version: 1.1
Status: Approved

> Doc 3 of 5 for Effective Dating. Follows DB-DESIGN-001, DATABASE_STANDARDS, and ADR-007.

## Design Principle

Effective dating is a platform pattern, not a module-specific feature. Every business table
that represents a time-changing fact must include valid-time fields and must be eligible
for system-time history when approved by architecture and database review.

The database design must enforce as much integrity as practical. Application validation,
domain services, and workflow approvals complement database constraints; they do not
replace database-level integrity for dates, statuses, tenant isolation, concurrency,
supersession, soft delete, and temporal history.

## Mandatory Columns

In addition to project-wide mandatory columns (`TenantId`, `CreatedBy`, `CreatedDate`,
`ModifiedBy`, `ModifiedDate`, `IsDeleted`, `VersionNumber`), effective-dated tables shall
include:

- `EffectiveFrom date not null`
- `EffectiveTo date null`
- `EffectiveStatus nvarchar(30) not null`
- `ChangeReason nvarchar(500) null`
- `ApprovalReferenceId uniqueidentifier null`
- `SupersededById uniqueidentifier null`

`EffectiveFrom` and `EffectiveTo` are tenant-local business dates. `EffectiveFrom` is
inclusive. `EffectiveTo` is inclusive when present. `EffectiveTo = NULL` is the
platform-wide representation of an active/open-ended record.

All system-generated timestamps, including `CreatedDate`, `ModifiedDate`, audit
timestamps, temporal period columns, outbox timestamps, and scheduler timestamps, must be
stored in UTC using approved SQL Server date/time types. APIs, reports, and scheduled
processing may render tenant-local values, but persisted system time remains UTC.

`VersionNumber` is the optimistic concurrency token for effective-dated entities. The
preferred SQL Server implementation is `rowversion`; an equivalent approved token may be
used only where SQL Server `rowversion` is not practical. Concurrency conflicts must be
detected and reported to the application before any write silently overwrites another
change.

## Business Key Standard

`EntityBusinessKey` is the natural business identifier used to group effective-dated
versions of the same business fact within a tenant. Each effective-dated entity must
explicitly identify its business key during database design and migration review.

Examples:

- Employee Salary: `EmployeeId`
- Employee Assignment: `EmployeeId`
- Organization Unit: `OrganizationUnitId`
- Leave Policy: `PolicyId`

Surrogate primary keys and business keys serve different purposes. A surrogate primary key
uniquely identifies one physical row/version. The business key groups all effective-dated
versions that represent the same real-world business fact. They must not be confused in
indexes, constraints, APIs, or history queries.

## Platform Tables

```text
core.EffectiveDatedEntityRegistration
  RegistrationId, TenantId, EntityName, SchemaName, TableName,
  BusinessKeyColumnNames, SupportsSystemVersioning, AllowsOverlap,
  RequiresApprovalRuleSetId,
  SensitiveHistoryClassification, IsActive, audit columns

core.EffectiveDatedChangeRequest
  ChangeRequestId, TenantId, EntityName, EntityBusinessKey, EntityId, OperationType,
  RequestedEffectiveFrom, RequestedEffectiveTo, Reason, ImpactClassification,
  WorkflowInstanceId, Status, RequestedBy, ApprovedBy, audit columns

core.EffectivePeriodConflict
  ConflictId, TenantId, EntityName, EntityBusinessKey, EntityId, ConflictType,
  ExistingRecordId, ProposedRecordId, ResolutionStatus, audit columns
```

## Constraints and Indexes

- Every effective-dated table must have an index on `(TenantId, EntityBusinessKey,
  EffectiveFrom, EffectiveTo)`.
- Current-record lookup index: `(TenantId, EntityBusinessKey, EffectiveFrom)` including
  `EffectiveTo`.
- Database `CHECK` constraints are required wherever practical. At minimum, effective-dated
  tables must enforce `EffectiveFrom <= EffectiveTo` when `EffectiveTo` is not `NULL`,
  valid `EffectiveStatus` values, and any additional integrity rule that can safely be
  enforced at the database layer.
- Standard platform statuses are `Draft`, `PendingApproval`, `Future`, `Active`,
  `Superseded`, `Corrected`, `Cancelled`, and `Inactive`. Entities that need different
  statuses must use an approved lookup or documented extension, not ad hoc string values.
- Overlap prevention shall be enforced through transaction validation and, where practical,
  filtered unique indexes for open-ended current rows.
- For single-active entities, only one open-ended record may exist for the same
  `(TenantId, EntityBusinessKey)` where `EffectiveTo IS NULL` and `IsDeleted = 0`.
- Inserting a new current or future effective record automatically closes the previous
  open record where the entity does not allow overlapping periods.
- RLS policies must apply to temporal current and history access.

Standard naming:

- `CK_<Table>_EffectivePeriod`
- `CK_<Table>_EffectiveStatus`
- `CK_<Table>_NoSelfSupersession`
- `IX_<Table>_Current`
- `IX_<Table>_EffectivePeriod`
- `UX_<Table>_OpenRecord`
- `FK_<Table>_<ReferencedTable>`

All EF Core migrations must follow the project's database naming conventions. Constraint
and index names must remain stable so support, diagnostics, and automated tests can map
database failures to platform validation errors.

## Supersession Chain Rules

`SupersededById` links an older effective-dated row to the row that superseded it. The
chain preserves correction lineage for audit, payroll explanation, reporting, workflow,
and support.

Rules:

- Superseded records remain immutable and traceable.
- Supersession chains must be preserved even after later corrections.
- A row cannot supersede itself.
- Circular supersession references are prohibited.
- The referenced row must belong to the same tenant and the same effective-dated entity.
- Queries that explain history must be able to traverse the chain from original version to
  latest approved version.

Where SQL Server cannot enforce the complete chain rule with a simple constraint, the
database shall enforce available foreign-key and self-reference checks, while the
Effective Dating Service enforces cross-row and circular-reference validation in the same
transaction.

## Temporal Table Use

SQL Server system-versioned temporal tables are preferred for high-value history such as
employee assignment, salary, policy, role assignment, workflow definition, rule version,
and payroll configuration. Temporal history tables must not be directly modified by
application code.

Temporal period columns must use UTC system time. Temporal current and history tables must
carry tenant isolation metadata and remain compatible with SQL Server Row-Level Security
and EF Core temporal queries.

Entities that cannot use SQL Server temporal tables must use an approved fallback:

- Manual history tables that mirror the current table.
- Audit history tables that can reconstruct prior values.
- Event-based history where immutable events are sufficient.
- Hybrid history that combines valid-time rows, audit, and events.

Fallback tables must preserve tenant isolation, audit references, UTC system timestamps,
retention/legal-hold behavior, and explain-history reconstruction.

## Soft Delete and Historical Records

Soft delete uses `IsDeleted` and does not physically remove effective-dated business
history. Soft-deleted records are hidden from normal current-state queries but remain
queryable through approved history, audit, legal, support, and retention workflows where
the caller has permission.

Temporal history remains available after logical deletion. A soft delete creates a new
system-time version and audit entry; it does not remove historical rows or break
supersession chains. Legal audit history must never be removed through soft delete.
Physical purge, anonymization, archival, or tombstoning may occur only through ADR-022
retention, legal-hold, and deletion governance.

## Retention

Retention follows ADR-022 and legal hold policy. Payroll, compliance, and audit history may
require longer retention than ordinary employee profile history. Purge operations must
preserve lawful audit evidence.

Partitioning should be considered for large temporal history tables and high-volume
history patterns. Payroll, attendance, audit, workflow, event/outbox, and future
integration history are likely candidates. Partitioning is an enterprise-scale
optimization strategy and is not mandatory for initial implementation unless volume,
retention, or performance review requires it.

## Migration Rules

New effective-dated entities must be registered through migration and architecture review.
Existing non-effective-dated tables cannot be converted without migration plan, data
backfill, overlap cleanup, and rollback strategy.

Every migration that introduces an effective-dated entity must define:

- The business key columns.
- Effective-period constraints.
- Status constraints or lookup references.
- Open-ended-record filtered unique index when the entity is single-active.
- Concurrency token configuration.
- RLS behavior for current and history access.
- Temporal table configuration or approved fallback history design.
- Supersession foreign-key and integrity rules.

Bulk effective-dated operations, such as annual salary revisions, organization
restructuring, policy updates, and department transfers, must use the same database
constraints, overlap prevention, approval linkage, audit capture, transaction boundaries,
and concurrency rules as individual updates. Detailed bulk import and processing tables
will be defined in future technical or feature-specific database designs.

## Acceptance Criteria

1. At least one current and one history query are validated under tenant RLS.
2. Period overlap prevention works for employee assignment and policy data.
3. SQL temporal history is enabled for approved high-value tables.
4. Backdated changes are traceable to change request and audit records.
5. Database migration scripts support rollback and data verification.
6. Each effective-dated entity defines its `EntityBusinessKey` and uses it consistently in
   indexes, constraints, history queries, and migrations.
7. Database `CHECK` constraints enforce effective-period validity and allowed status values
   wherever practical.
8. Single-active entities enforce one open-ended record per tenant-scoped business key
   using a filtered unique index or approved equivalent.
9. System timestamps, audit timestamps, and temporal period columns are stored in UTC.
10. Supersession chains remain immutable, traceable, and protected from self-reference and
    circular-reference defects.
11. Soft delete preserves temporal history, legal audit history, and approved historical
    query behavior.
12. Effective-dated entities use `VersionNumber` or an approved row-version mechanism as
    the optimistic concurrency token.
13. Large history tables have documented partitioning guidance where volume or retention
    justifies it.

## External References

- SQL Server temporal tables: https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
- SQL Server row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security

References last validated: 2026-06-28.

## Approval

Database Architect: Approved by Codex 2026-06-28 - Solution Architect: Approved by Codex 2026-06-28 - Security Architect: Approved as aligned with tenant isolation, audit, retention, RLS, and temporal-history controls 2026-06-28 - Status: Approved
