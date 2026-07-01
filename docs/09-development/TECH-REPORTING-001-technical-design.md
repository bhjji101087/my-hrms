# Technical Design - Standard Reports

Module: Reporting
Phase: 7A / Sprint S10
Owner: .NET Architect (Agent 13)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Standard Reports.

## Architecture

Reporting uses governed read models populated from module APIs/events and approved database
projections. Reports are not allowed to bypass tenant/security rules or query sensitive
module tables directly from UI.

```text
Module Events/APIs -> Reporting Projections -> Report Service -> API/UI/Export
                             |                    |
                         Security Filter       Audit/Event Bus
```

## Components

- Report Catalog Service: definitions, parameters, permissions, classifications.
- Report Query Service: applies tenant, RBAC, ABAC, filters, pagination, and masking.
- Projection Builder: builds read models from event bus and approved source APIs.
- Export Service: async export with purpose, approval where required, expiry, and audit.
- Reconciliation Service: compares report totals to source modules.

## API Requirements

APIs under `/api/v1/reports` cover catalog, parameters, run, status, export, download, and
report metadata. OpenAPI must document pagination, filtering, export status, and rate
limits.

## Security

Report definitions declare required permissions and field classifications. Runtime filters
apply ABAC based on employee scope, manager hierarchy, branch/office, legal entity, payroll group, and
tenant. Exports create audit records and may require approval for sensitive reports.

## Data Rules

- Report projections are rebuildable.
- As-of reports use Effective Dating service.
- Branch/office reports use Branch / Office scope resolver and cannot expose restricted
  branch values in filters, counts, exports, or projections.
- Payroll reports include pay period, run ID, source snapshot, and rule version evidence.
- Report definitions are configuration-as-data and versioned.

## Observability

Metrics include report run latency, export queue depth, failed exports, row counts,
security-denied count, projection lag, and reconciliation failures.

## Acceptance Criteria

1. Report API applies common security and pagination.
2. Export generation is asynchronous, audited, and expiring.
3. Projection lag is visible.
4. As-of reporting uses effective-dated services.
5. Report definitions can be added through configuration.

## External References

- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- OpenTelemetry: https://opentelemetry.io/docs/
- OWASP API Security: https://owasp.org/API-Security/editions/2023/en/0x11-t10/

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

.NET Architect: ____ - Reporting Analyst: ____ - Security Architect: ____ - Status: Approved
