# Technical Design - Configuration-as-Data

Module: Platform Foundation
Phase: 7A / Sprint S3
Owner: Solution Architect (Agent 6)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Configuration-as-Data.

## Architecture

Configuration is managed through a registry, schema validator, lifecycle workflow, and
runtime resolver. Modules declare configuration schemas and extension points through
manifests. Consumers request configuration through typed providers instead of reading
tables directly.

```text
Admin UI/API -> Config Lifecycle -> Schema Validation -> Approval -> Published Version
                                                     |
Runtime Module -> Configuration Provider -> Cache -> Published Config
```

## Components

- Configuration Registry: domain, schema, owner, lifecycle, sensitivity.
- Module Manifest Registry: module metadata, dependencies, features, APIs, events, UI slots.
- Feature Flag Service: tenant-aware flag evaluation using OpenFeature-style concepts.
- Schema Validator: JSON Schema validation and dependency checks.
- Impact Analyzer: identifies affected modules, caches, reports, rules, and workflows.
- Runtime Resolver: returns effective published configuration by tenant/date/context.
- Promotion Service: controlled export/import and rollback.

## Lifecycle

Draft -> Validated -> Review -> Approved -> Published -> Superseded -> Retired.
Published versions are immutable. Rollback publishes a new version pointing to a prior
approved payload.

## Runtime Rules

- Modules never branch on tenant name or customer-specific code.
- Configuration is cached by tenant, domain, version, and effective date.
- Sensitive configuration is encrypted or secret-referenced.
- Provider credentials are never stored in plain configuration payloads.

## API Requirements

APIs under `/api/v1/configuration` cover schema registry, configuration versions,
validation, impact analysis, approval submission, publish, rollback, export, and import.
OpenAPI must document schema payloads and error responses.

## Observability

Metrics include config resolution latency, cache hit rate, validation failures, publish
count, rollback count, and runtime missing-config failures. Publish events invalidate
caches through Event Bus.

## Acceptance Criteria

1. Runtime services resolve effective published configuration through shared provider.
2. Feature flags are evaluated by tenant and context.
3. Invalid JSON payload cannot be published.
4. Configuration publish emits event and invalidates cache.
5. Future module manifests can register without modifying existing core modules.

## External References

- OpenFeature specification: https://openfeature.dev/specification/
- JSON Schema: https://json-schema.org/
- OpenTelemetry: https://opentelemetry.io/docs/

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Solution Architect: ____ - .NET Architect: ____ - Security Architect: ____ - Status: Approved
