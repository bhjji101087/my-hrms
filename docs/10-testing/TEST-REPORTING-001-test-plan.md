# Test Plan - Standard Reports

Module: Reporting
Phase: 7A / Sprint S10
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 5 of 5 for Standard Reports.

## Functional Tests

- Report catalog lists permitted Phase 7A reports.
- Employee master report filters by branch/office/department/location/legal entity.
- Leave balance report reconciles with leave ledger projection.
- Attendance exception report reflects approved summaries.
- Payroll register reconciles with payroll run totals.
- Workflow aging report shows pending tasks and SLA status.
- Audit activity report returns authorized records.

## Security Tests

- Unauthorized report is hidden and API returns forbidden.
- Manager report scope includes team only.
- Payroll fields are masked without permission.
- Export requires purpose and permission.
- Branch admin cannot export another branch's data.
- Cross-tenant report data is blocked.

## Integration Tests

- Projections update from Event Bus.
- As-of report uses Effective Dating service.
- Export creates audit record.
- Report definition is loaded through Configuration-as-Data.
- OpenAPI report endpoints validate examples.

## Negative Tests

- Overly broad sensitive export requires approval or is blocked.
- Invalid filter returns validation error.
- Expired export cannot be downloaded.
- Projection lag is visible when data is not current.

## Performance Tests

- Standard report viewer P95 under target with pagination.
- Export job handles approved large report asynchronously.
- Projection rebuild completes within operational window.

## Exit Criteria

- Minimum 85% automated coverage.
- Report totals reconcile with source modules.
- All sensitive report security tests pass.
- Export audit and expiry behavior pass.

## External References

- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- OWASP API Security: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

QA Architect: ____ - Reporting Analyst: ____ - Security Architect: ____ - Status: Approved
