# UI Design - Standard Reports

Module: Reporting
Phase: 7A / Sprint S10
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 4 of 5 for Standard Reports.

## Screen A - Report Catalog

Grouped by People, Leave, Attendance, Payroll, Workflow, Audit, and Administration.
Each report card shows description, data sensitivity, last run, available filters, and
required permission.

## Screen B - Report Parameters

Users select date range/as-of date, legal entity, department, location, manager, employee,
status, pay period, and other report-specific filters. Sensitive reports show privacy and
export warnings.

## Screen C - Report Viewer

Table view with sorting, pagination, column chooser, filter chips, and masked sensitive
columns. The viewer shows report generation time, row count, and source/evidence metadata.

## Screen D - Export Request

Export requires format, purpose, optional approval, expiry notice, and data classification
confirmation. Export progress is asynchronous.

## Screen E - Report Run History

Shows previous runs, parameters, status, row counts, exports, downloads, and audit links.

## Acceptance Criteria

1. Report catalog shows only permitted reports.
2. Filters are clear and prevent overly broad sensitive exports.
3. Viewer supports pagination and masked sensitive columns.
4. Export requires purpose and creates audit.
5. Run history is visible to authorized users.

## External References

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

UX/UI Architect: ____ - Product Owner: ____ - Reporting Analyst: ____ - Status: Approved
