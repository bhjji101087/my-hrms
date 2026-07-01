# Database Design - Configuration-as-Data

Module: Platform Foundation
Schema: `config`
Phase: 7A / Sprint S3
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Configuration-as-Data.

## Tables

```text
config.ModuleManifest
  ModuleManifestId, TenantId, ModuleCode, ModuleName, Version,
  DependencyJson, FeatureJson, ApiContractRef, EventContractRef,
  UiExtensionJson, IsActive, audit columns

config.ConfigurationSchema
  ConfigurationSchemaId, TenantId, DomainCode, SchemaVersion,
  JsonSchema, SensitivityClass, OwnerRole, IsActive, audit columns

config.ConfigurationItem
  ConfigurationItemId, TenantId, DomainCode, ScopeType, ScopeId,
  CurrentPublishedVersionId, IsActive, audit columns

config.ConfigurationVersion
  ConfigurationVersionId, TenantId, ConfigurationItemId, VersionNumberText,
  EffectiveFrom, EffectiveTo, Status, PayloadJson, PayloadHash,
  ApprovalWorkflowInstanceId, PublishedBy, PublishedAt, audit columns

config.FeatureFlag
  FeatureFlagId, TenantId, FlagKey, Description, DefaultValue,
  EvaluationRuleSetId, CurrentPublishedVersionId, IsActive, audit columns

config.ConfigurationImportExport
  TransferId, TenantId, TransferType, SourceEnvironment, TargetEnvironment,
  PayloadReference, Status, RequestedBy, ApprovedBy, audit columns
```

## Indexes

- `ConfigurationItem`: unique `(TenantId, DomainCode, ScopeType, ScopeId)`.
- `ConfigurationVersion`: `(TenantId, ConfigurationItemId, Status, EffectiveFrom)`.
- `FeatureFlag`: unique `(TenantId, FlagKey)`.
- `ModuleManifest`: unique `(TenantId, ModuleCode, Version)`.

## Storage Rules

Published versions are immutable. Secrets are stored as references to approved secret
storage, not plaintext. Payloads are validated against registered JSON Schema before
approval and publish.

## RLS and Security

Configuration is tenant-scoped. Sensitive provider and security configuration requires
additional ABAC. Configuration read/write is audited, including export/import.

## Retention

Published configuration versions needed for payroll, compliance, workflow, and audit must
be retained for the same period as dependent business records.

## Acceptance Criteria

1. Tenant-specific configuration versions are immutable after publish.
2. Feature flags are unique and auditable per tenant.
3. Schema validation metadata is retained.
4. Configuration import/export is traceable.
5. RLS blocks cross-tenant configuration access.

## External References

- JSON Schema: https://json-schema.org/
- OpenFeature specification: https://openfeature.dev/specification/

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - Solution Architect: ____ - Security Architect: ____ - Status: Approved
