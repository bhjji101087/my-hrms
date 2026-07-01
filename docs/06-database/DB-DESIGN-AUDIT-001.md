# Database Design - Audit and Time Machine

Module: Platform Foundation
Schema: `audit`
Phase: 7A / Sprint S2
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Audit and Time Machine. Follows DB-DESIGN-001, ADR-022, and security standards.

## Tables

```text
audit.AuditRecord
  AuditRecordId, TenantId, CorrelationId, ActorUserId, OnBehalfOfUserId,
  SubjectUserId, ActionType, EntityName, EntityId, ModuleName,
  ChangeReason, SourceType, SourceIpHash, DeviceId, OccurredAt,
  RiskLevel, RetentionClass, HashValue, PreviousHashValue, audit columns

audit.AuditFieldChange
  AuditFieldChangeId, TenantId, AuditRecordId, FieldName,
  OldValueMasked, NewValueMasked, Classification, IsRedacted, audit columns

audit.SecurityEvent
  SecurityEventId, TenantId, CorrelationId, UserAccountId, EventType,
  RiskScore, Decision, Reason, SourceIpHash, DeviceFingerprint,
  OccurredAt, RetentionClass, audit columns

audit.TimeMachineSnapshot
  SnapshotId, TenantId, EntityName, EntityId, BusinessAsOfDate,
  SystemAsOfTime, SnapshotPayloadJson, GeneratedBy, GeneratedAt,
  ExpiresAt, LegalHoldId, audit columns

audit.AuditExportRequest
  ExportRequestId, TenantId, RequestedBy, FilterJson, Purpose,
  Status, FileReference, ApprovedBy, ExpiresAt, audit columns
```

## Storage Rules

- Audit tables are append-only except controlled redaction markers and retention lifecycle
  metadata.
- Sensitive field values are masked, encrypted, or tokenized based on classification.
- Passwords, secrets, keys, and tokens are never persisted.
- Hash chaining is required for high-risk audit classes where enabled.
- Audit export files are stored through approved secure storage with expiry and access logs.

## Indexes

- `AuditRecord`: `(TenantId, EntityName, EntityId, OccurredAt desc)`,
  `(TenantId, ActorUserId, OccurredAt desc)`, `(TenantId, CorrelationId)`.
- `SecurityEvent`: `(TenantId, UserAccountId, OccurredAt desc)`, `(TenantId, EventType, OccurredAt desc)`.
- `AuditExportRequest`: `(TenantId, RequestedBy, CreatedDate desc)`.
- Partition large audit tables by time period and tenant-aware access pattern.

## RLS and Access

All audit tables are tenant-scoped. Additional ABAC filters apply for sensitive subjects,
payroll records, security records, and investigation-only views. Audit read activity must
itself create audit records.

## Retention and Legal Hold

Retention class is set at write time. Legal hold blocks purge. Retention jobs must create
audit records for purge execution, skipped legal-hold records, and errors.

## Acceptance Criteria

1. Audit tables include tenant filtering and performant entity history lookup.
2. High-risk records support tamper-evidence verification.
3. Sensitive values are not stored in plaintext audit fields.
4. Audit export requests are traceable and expiring.
5. Retention and legal hold behavior is testable.

## External References

- SQL Server ledger overview: https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview
- NIST SP 800-92: https://csrc.nist.gov/pubs/sp/800/92/final

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - Security Architect: ____ - Compliance Reviewer: ____ - Status: Approved
