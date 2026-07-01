# Test Plan - Core HR and Employee Self-Service

Module: Core HR
Phase: 7A / Sprint S4
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 5 of 5 for Core HR and ESS.

## Functional Tests

- Create employee with primary assignment.
- Update assignment with future effective date.
- Backdate manager change with approval and reason.
- Submit ESS profile update and approve through workflow.
- Search employee directory by department and location.
- Search employee directory by branch/office.

## Security Tests

- Employee views self data only.
- Manager sees team members only.
- HR access is limited by branch/office, legal entity, and location where configured.
- Sensitive fields are masked without permission.
- Cross-tenant employee access is blocked.

## Integration Tests

- Employee creation emits event.
- Assignment change updates reporting projection.
- Payroll retrieves assignment as-of pay period.
- Leave and Attendance consume employee status.
- Audit captures field-level changes.

## Performance Tests

- Employee directory search P95 under target for tenant scale.
- Manager hierarchy rebuild meets operational target.
- Branch/office assignment as-of query returns correct historical branch.
- Profile screen loads paginated history efficiently.

## Negative Tests

- Duplicate employee number rejected.
- Overlapping assignment periods rejected.
- ESS update without configured editable field rejected.
- Unauthorized backdated correction rejected.

## Exit Criteria

- Minimum 85% automated coverage.
- Effective dating, audit, events, workflow, and security scenarios pass.
- No cross-tenant data exposure.
- OpenAPI examples validate successfully.

## External References

- OWASP API Security: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Phase 7A Branch / Office Addendum

Core HR testing must include branch-scope scenarios from
`docs/10-testing/TEST-BRANCH-001-test-plan.md`.

## Approval

QA Architect: ____ - Product Owner: ____ - Security Architect: ____ - Status: Approved
