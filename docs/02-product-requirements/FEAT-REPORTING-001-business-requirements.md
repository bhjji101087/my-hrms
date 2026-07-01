# Feature Specification - Standard Reports

Feature Name: Standard Reports
Module: Reporting
Phase: 7A / Sprint S10
Owner: Product Owner (Agent 2)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 1 of 5 for Standard Reports. Implements PRD FR-012.

## Purpose

Phase 7A must deliver reliable standard operational and statutory reports for Core HR,
Leave, Attendance, Payroll, Workflow, Audit, and tenant administration. Reports must be
tenant-safe, permission-aware, export-controlled, and based on governed read models.

## Market and Enterprise Context

HR customers expect ready-made reports for employee lists, headcount, leave balances,
attendance exceptions, payroll registers, payslip status, statutory outputs, and audit.
Common irritation comes from slow exports, inconsistent numbers, missing filters, and
reports that expose data beyond the user's scope.

## Scope

In scope:
- Standard report catalog for Phase 7A modules.
- Tenant, role, ABAC, and field-level security.
- Filtered views, pagination, export, and audit.
- As-of reporting for effective-dated data.
- Event-fed reporting projections where appropriate.
- OpenAPI report catalog and run APIs.

Out of scope:
- Advanced BI semantic layer.
- Custom report designer.
- Scheduled reports and dashboard marketplace unless approved later.

## Standard Report Set

- Employee master report.
- Headcount by branch/office/department/location/legal entity.
- Employee movement report.
- Leave balance report.
- Leave transaction ledger report.
- Attendance daily summary report.
- Attendance exception report.
- Payroll register.
- Payslip publish status report.
- Statutory payroll output summaries.
- Workflow task aging report.
- Audit activity report.

## Business Requirements

1. Reports shall use governed read models or approved APIs, not direct unsafe table reads.
2. Reports shall respect tenant, RBAC, ABAC, data classification, and field masking.
3. Exports shall be permission-protected, purpose-captured, and audited.
4. Reports shall support filters, pagination, sorting, and date/as-of parameters.
5. Payroll and statutory reports shall show source period and rule version evidence.
6. Report definitions shall be configuration-driven where possible.
7. Branch/office scope shall apply to filters, counts, exports, and projected report data.

## Acceptance Criteria

1. Standard Phase 7A report catalog is available to authorized users.
2. Manager report scope returns only permitted team data.
3. Payroll report export requires permission and creates audit record.
4. As-of employee report returns historical organization assignment correctly.
5. Report numbers reconcile with source module data.
6. Branch administrators cannot view or export another branch's restricted report data.

## External References

- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- OWASP API Security: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

References last validated: 2026-06-28.

## Approval

Product Owner: ____ - Reporting Analyst: ____ - Security Architect: ____ - Status: Approved
