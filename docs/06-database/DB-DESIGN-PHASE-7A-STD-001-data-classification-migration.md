# Database Standard - Phase 7A Data Classification, Migration, and Rollback

Document Owner: Database Architect / Security Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved
> Applies to every Phase 7A database design. This standard strengthens table-level data
> governance, rollout safety, rollback planning, and post-deployment validation.

## 1. Table-Level Data Classification

Every Phase 7A table must be classified before implementation using this minimum matrix:

```text
Table:
PII Level: None / Low / Medium / High / Payroll-Sensitive
Encryption: At rest / Field-level / File encryption / Secret reference
Masking Required: Yes / No
Export Allowed: Yes / No / Approval Required
Retention Class:
Legal Hold Eligible: Yes / No
Audit Required: Yes / No
```

## 2. Classification Guidance

- Payroll results, payslips, salary assignments, statutory data, and tax data are
  `Payroll-Sensitive`.
- Authentication, security events, audit investigations, emergency access, and privileged
  administrative actions are `High`.
- Employee master, attendance, leave, manager hierarchy, and document metadata are at least
  `Medium` unless field-level review allows lower classification.
- Operational metadata without employee or tenant-sensitive content may be `Low`.
- Pure reference configuration may be `None` only after security review.

## 3. Migration Standard

Every Phase 7A database change must include:

- EF Core migration name and purpose.
- Forward migration approach.
- Backfill rules and data defaulting.
- Zero-downtime deployment concern.
- Index creation strategy for large tables.
- RLS policy validation.
- Audit/temporal/ledger impact.
- Rollback or compensating migration.
- Post-deployment validation query.

## 4. Rollback and Compensating Action

Data-destructive rollback is not allowed for business data. If a migration cannot be safely
rolled back, the design must define a compensating migration and operational containment
steps.

## 5. Validation Queries

Every module database implementation must provide validation queries for:

- TenantId presence and RLS policy binding.
- Required indexes.
- Effective-date overlap checks where applicable.
- Orphaned foreign keys or missing references.
- Classification-sensitive fields.
- Migration row counts and backfill completion.

## 6. Approval Requirement

Database implementation cannot start until each module database design either includes the
classification/migration matrix directly or explicitly references this standard.

## External References

- SQL Server row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
- SQL Server temporal tables: https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
- SQL Server ledger overview: https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview

References last validated: 2026-06-29.

## Approval

Database Architect: ____ - Security Architect: ____ - Compliance Reviewer: ____ - Status: Approved
