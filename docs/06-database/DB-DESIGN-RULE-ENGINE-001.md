# Database Design - Rule Engine

Module: Platform Foundation
Schema: `rules`
Phase: 7A / Sprint S3
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Rule Engine.

## Tables

```text
rules.RuleSet
  RuleSetId, TenantId, Code, Name, ModuleScope, Classification,
  OwnerRole, CurrentPublishedVersionId, IsActive, audit columns

rules.RuleSetVersion
  RuleSetVersionId, TenantId, RuleSetId, VersionNumberText,
  EffectiveFrom, EffectiveTo, Status, DefinitionJson, InputSchemaJson,
  OutputSchemaJson, ApprovalWorkflowInstanceId, PublishedBy, PublishedAt,
  DeprecatedAt, audit columns

rules.DecisionTable
  DecisionTableId, TenantId, RuleSetVersionId, HitPolicy,
  TableDefinitionJson, DefaultOutputJson, audit columns

rules.RuleSimulation
  SimulationId, TenantId, RuleSetVersionId, InputContextJson,
  OutputJson, ExplanationJson, ResultStatus, RunBy, audit columns

rules.RuleEvaluationLog
  EvaluationLogId, TenantId, RuleSetId, RuleSetVersionId, ModuleName,
  CorrelationId, ContextHash, ResultHash, DurationMs, OutcomeStatus,
  EvaluatedAt, audit columns
```

## Storage Rules

- Published `RuleSetVersion` records are immutable.
- Rule definitions are stored as structured JSON validated by JSON Schema.
- Runtime evaluation logs store hashes and summary unless detailed evidence is required by
  payroll/compliance policy.
- Rule versions are effective-dated and tenant-scoped.

## Indexes

- `RuleSet`: unique `(TenantId, Code)`.
- `RuleSetVersion`: `(TenantId, RuleSetId, Status, EffectiveFrom)`.
- `RuleEvaluationLog`: `(TenantId, RuleSetId, EvaluatedAt desc)` and `(TenantId, CorrelationId)`.
- `RuleSimulation`: `(TenantId, RuleSetVersionId, CreatedDate desc)`.

## RLS and Security

All tables are tenant-scoped. Payroll and compliance rule definitions may require
additional ABAC. Rule definitions are business-critical configuration and must be audited.

## Retention

Published rule versions used for payroll/compliance must be retained for statutory and
audit periods. Simulation records may have shorter retention unless attached to approval
evidence.

## Acceptance Criteria

1. Rule definitions are versioned, immutable after publish, and effective-dated.
2. Rule evaluation evidence is queryable by correlation ID.
3. JSON schema validation prevents invalid stored definitions.
4. RLS blocks rule visibility across tenants.
5. Payroll-related rule versions cannot be purged while referenced by payroll runs.

## External References

- JSON Schema: https://json-schema.org/
- SQL Server row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - Solution Architect: ____ - Security Architect: ____ - Status: Approved
