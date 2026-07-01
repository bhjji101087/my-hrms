# Test Plan - Attendance and First Connector

Module: Attendance
Phase: 7A / Sprint S6
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 5 of 5 for Attendance.

## Functional Tests

- Import punches through first connector.
- Record web/manual punch where allowed.
- Calculate daily summary from raw punches and rules.
- Calculate daily summary using employee's effective shift.
- Submit regularization request and approve through workflow.
- Recalculate attendance after approved correction.
- Publish payroll impact event.

## Security Tests

- Employee sees own attendance only.
- Manager sees scoped team attendance.
- Connector config requires admin permission.
- Connector secrets are not exposed.
- Cross-tenant punch import is blocked.

## Integration Tests

- Core HR employee mapping works for connector.
- Leave approved status affects attendance day.
- Holiday calendar affects attendance status.
- Rule Engine calculates late/absence.
- Shift Foundation resolves assigned shift and shift override.
- Payroll consumes attendance summary event.

## Negative Tests

- Duplicate external punch does not double count.
- No assigned shift creates configured default or exception behavior.
- Overnight shift across date boundary calculates correctly.
- Unknown employee/device is rejected to reconciliation queue.
- Regularization outside allowed window is rejected by rule.
- Approval retry is idempotent.
- Connector outage triggers retry and health warning.

## Performance Tests

- Connector sync handles expected punch volume.
- Daily summary rebuild completes within batch window.
- Team attendance page meets P95 target.

## Exit Criteria

- Minimum 85% automated coverage.
- Connector import, reconciliation, regularization, and payroll feed pass E2E.
- Shift-aware attendance and payroll impact tests pass.
- No cross-tenant attendance leakage.
- OpenAPI and UI accessibility tests pass.

## External References

- RabbitMQ reliability: https://www.rabbitmq.com/docs/reliability
- OWASP API Security: https://owasp.org/API-Security/editions/2023/en/0x11-t10/

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Phase 7A Shift Foundation Addendum

Attendance testing must include scenarios from
`docs/10-testing/TEST-SHIFT-FOUNDATION-001-test-plan.md`.

## Approval

QA Architect: ____ - Integration Architect: ____ - Security Architect: ____ - Status: Approved
