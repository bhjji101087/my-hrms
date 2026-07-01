# Technical Design - Audit and Time Machine

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: Solution Architect (Agent 6)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Audit and Time Machine. Implements FEAT-AUDIT-001.

## Architecture

Audit is a platform service consumed by all modules through application middleware,
domain-event handlers, and database change capture points. Modules must not write private
audit tables. Time Machine composes effective-dated, temporal, audit, workflow, and event
data into governed read views.

```text
API/Job/Import -> Command Handler -> Domain Change -> Audit Capture -> Audit Store
                                      |                 |
                                      +-> Outbox Event   +-> Time Machine Projections
```

## Components

- Audit Capture Middleware: captures request context, actor, tenant, correlation ID.
- Change Collector: compares old and new values for auditable entities.
- Security Event Collector: captures login, MFA, permission, ABAC, and emergency events.
- Audit Store: append-only persistence in `audit` schema.
- Tamper Evidence Service: hash-chain or SQL ledger integration for high-risk records.
- Time Machine Query Service: reconstructs state as of business date and/or system time.
- Export Evidence Service: watermarks and audits evidence exports.

## Event and API Contracts

Audit APIs shall be under `/api/v1/audit`. They include search, entity history, security
events, export request, export status, and time-machine reconstruction. OpenAPI must
document filters, redaction rules, pagination, and export limits.

Published events include `AuditRecordCreated`, `SecurityEventRecorded`,
`AuditExportRequested`, and `TimeMachineViewRequested`.

## Data Protection

Sensitive fields must be classified. Audit should store enough evidence for accountability
without unnecessarily duplicating secrets or highly sensitive values. Passwords, tokens,
private keys, and secrets are never stored in audit. PII masking and field-level access
rules apply on read.

## Failure Handling

For mandatory audit actions, business commit shall fail if audit persistence fails unless
an approved degraded-mode policy exists. Audit write failures trigger alerts and incident
runbooks. Export generation is asynchronous and idempotent.

## Observability

Metrics include audit write latency, failure rate, queue depth, export duration, tamper
verification failures, and search latency. Logs must not contain sensitive before/after
values outside approved audit storage.

## Extension Points

Modules register auditable entities, field classifications, event mappings, and retention
classes through configuration metadata. Adding a module must not require changing the core
audit engine.

## Acceptance Criteria

1. All Phase 7A modules emit standard audit records through shared services.
2. Time Machine can reconstruct employee, leave, attendance, payroll, workflow, and rule states.
3. Audit read APIs enforce tenant, RBAC, ABAC, field masking, and pagination.
4. Tamper-evidence verification is available for high-risk audit streams.
5. Audit write failures are observable and operationally actionable.

## External References

- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- NIST SP 800-92: https://csrc.nist.gov/pubs/sp/800/92/final
- SQL Server ledger: https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Solution Architect: ____ - Security Architect: ____ - .NET Architect: ____ - Status: Approved
