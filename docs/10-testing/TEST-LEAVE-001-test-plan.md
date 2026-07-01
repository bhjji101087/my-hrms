# Test Plan - Leave Management

Module: Leave
Phase: 7A / Sprint S5
Owner: QA Architect (Agent 21)
Created Date: 2026-06-14
Last Updated: 2026-06-28
Version: 2.0
Status: Approved
> Doc 5 of 5 for Leave Management.

## Functional Tests

- Configure leave type, policy, rule references, and workflow.
- Apply leave within balance and approve through workflow.
- Withdraw pending leave and release reservation.
- Accrual job posts monthly ledger transactions.
- Carry-forward and lapse run at configured period boundary.
- Balance adjustment requires reason and audit.

## Security Tests

- Employee sees own requests and balances only.
- Manager approves only scoped team requests.
- HR can adjust balance only with permission.
- Cross-tenant leave requests are blocked.
- Sensitive comments/attachments follow permission rules.

## Integration Tests

- Rule Engine validates eligibility, day count, and balance policy.
- Workflow Studio routes approvals and handles delegation/SLA.
- Event Bus publishes leave events.
- Payroll consumes unpaid leave impact event.
- Reports reflect approved leave and balances.

## Negative Tests

- Insufficient balance rejected where policy disallows negative balance.
- Overlapping request rejected.
- Duplicate idempotency key does not double reserve.
- Approval retry does not double debit.
- Backdated correction without permission/reason rejected.

## Performance Tests

- Apply and approve APIs meet P95 target.
- Accrual job handles tenant employee volume.
- Team calendar loads within target under normal team size.

## Exit Criteria

- Minimum 85% coverage; ledger/rules minimum 90%.
- Zero double-debit or cross-tenant leakage.
- Payroll impact scenarios pass.
- OpenAPI and E2E apply-to-approve path pass.

## External References

- RabbitMQ reliability: https://www.rabbitmq.com/docs/reliability
- OWASP API Security: https://owasp.org/API-Security/editions/2023/en/0x11-t10/

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

QA Architect: ____ - Product Owner: ____ - Security Architect: ____ - Status: Approved
