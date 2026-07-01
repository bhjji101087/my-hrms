# Test Plan - Audit and Time Machine

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 5 of 5 for Audit and Time Machine. Covers FEAT/TECH/DB/UI-AUDIT-001.

## Functional Tests

- Employee update creates audit record and field changes.
- Workflow approval records approver, decision, comment, and correlation ID.
- Payroll run creates audit trail for inputs, rule versions, outputs, and approvals.
- Export requires purpose and creates export audit.
- Time Machine reconstructs an employee record for a selected date.

## Security Tests

- Cross-tenant audit search returns no records.
- Sensitive payroll and security fields are masked without permission.
- Audit read activity is audited.
- Impersonation records include `OnBehalfOf`.
- Tamper-evidence validation detects modified records in test fixture.

## Integration Tests

- Audit records correlate with Event Bus outbox events.
- Effective-dated history appears in Time Machine.
- Workflow references appear in audit detail.
- Retention job respects legal hold.
- OpenAPI audit endpoints return standard envelope and pagination.

## Performance Tests

- Search by correlation ID P95 under 500 ms.
- Entity history query P95 under 1 second for normal history depth.
- Export job handles approved large date range asynchronously.

## Negative Tests

- Missing audit context blocks mandatory business operation.
- Attempt to export without purpose returns validation error.
- Unauthorized security event search returns 403.
- Retention job cannot purge legal-hold records.

## Exit Criteria

- 100% of Phase 7A mutating commands emit audit records.
- Zero plaintext secrets in audit storage.
- Audit and Time Machine tests are part of release gate.
- Security Architect signs off high-risk audit handling.

## External References

- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- NIST SP 800-92: https://csrc.nist.gov/pubs/sp/800/92/final

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

QA Architect: ____ - Security Architect: ____ - Product Owner: ____ - Status: Approved
