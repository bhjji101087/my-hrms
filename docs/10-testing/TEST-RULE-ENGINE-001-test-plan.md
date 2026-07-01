# Test Plan - Rule Engine

Module: Platform Foundation
Phase: 7A / Sprint S3
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 5 of 5 for Rule Engine.

## Functional Tests

- Create, validate, approve, publish, deprecate, and retire rule set version.
- Evaluate leave eligibility rule with positive and negative contexts.
- Evaluate payroll formula using effective-dated salary component data.
- Evaluate workflow routing rule and return approver group.
- Simulate rule with sample input and capture explanation.

## Security Tests

- Attempt to execute unsupported function is rejected.
- Unauthorized user cannot publish rule.
- Cross-tenant rule access is blocked.
- Sensitive context fields are masked in logs and UI.
- Rule tampering after publish is blocked.

## Integration Tests

- Leave consumes eligibility and accrual rules.
- Attendance consumes late/regularization rules.
- Payroll consumes component and statutory applicability rules.
- Workflow consumes routing conditions.
- Audit records rule publish and runtime version evidence.

## Performance Tests

- Cached published rule evaluation meets low-latency target.
- Complex decision table respects timeout and complexity limits.
- Bulk payroll run evaluates rules within payroll batch window.

## Negative Tests

- Invalid JSON schema blocks save.
- Overlapping effective versions block publish.
- Missing required input returns controlled validation error.
- Retired rule version cannot be used for new calculations.

## Exit Criteria

- Minimum 85% coverage; 90% for evaluator and validator.
- No arbitrary code execution path exists.
- Payroll sample calculations are reproducible by rule version.
- Rule simulation and approval evidence pass E2E tests.

## External References

- CEL: https://cel.dev/
- OMG DMN: https://www.omg.org/spec/DMN/
- OWASP API Security: https://owasp.org/API-Security/editions/2023/en/0x11-t10/

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

QA Architect: ____ - Solution Architect: ____ - Security Architect: ____ - Status: Approved
