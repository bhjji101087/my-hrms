# Database Design - Standard Reports

Module: Reporting
Schema: `reporting`
Phase: 7A / Sprint S10
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Standard Reports.

## Tables

```text
reporting.ReportDefinition
  ReportDefinitionId, TenantId, ReportCode, Name, ModuleScope,
  ParameterSchemaJson, RequiredPermission, Classification,
  CurrentPublishedVersionId, IsActive, audit columns

reporting.ReportDefinitionVersion
  ReportDefinitionVersionId, TenantId, ReportDefinitionId, VersionNumberText,
  EffectiveFrom, EffectiveTo, DefinitionJson, Status, audit columns

reporting.ReportRun
  ReportRunId, TenantId, ReportDefinitionVersionId, RequestedBy,
  ParameterJson, Status, RowCount, StartedAt, CompletedAt, audit columns

reporting.ReportExport
  ReportExportId, TenantId, ReportRunId, ExportFormat, Purpose,
  FileReference, ExpiresAt, DownloadCount, ApprovedBy, audit columns

reporting.EmployeeReportProjection
  ProjectionId, TenantId, EmployeeId, AsOfDate, EmployeeNumber,
  BranchOfficeId, DepartmentId, LocationId, LegalEntityId, ManagerEmployeeId,
  EmploymentStatus, ProjectionVersion, audit columns

reporting.PayrollReportProjection
  ProjectionId, TenantId, PayrollRunId, EmployeeId, PayPeriodId,
  GrossEarnings, TotalDeductions, NetPay, ExceptionStatus,
  RuleVersionSnapshotHash, audit columns
```

## Indexes

- `ReportDefinition`: unique `(TenantId, ReportCode)`.
- `ReportRun`: `(TenantId, RequestedBy, CreatedDate desc)`.
- `ReportExport`: `(TenantId, ReportRunId)`.
- Projections: tenant plus report-specific filter columns such as date, employee, branch,
  org, legal entity, location, pay period, and status.

## RLS and Security

All report definitions, runs, exports, and projections are tenant-scoped. Sensitive
projection fields may be encrypted, masked, or omitted based on report classification.

## Retention

Report run metadata and exports follow classification-specific retention. Export files
expire and access is audited. Rebuildable projections may be refreshed or rebuilt from
source modules/events.

## Acceptance Criteria

1. Report definitions are versioned and tenant-scoped.
2. Exports are traceable, expiring, and audited.
3. Projections are rebuildable.
4. RLS blocks cross-tenant report data.
5. Payroll projection references run and rule evidence.

## External References

- SQL Server row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - Reporting Analyst: ____ - Security Architect: ____ - Status: Approved
