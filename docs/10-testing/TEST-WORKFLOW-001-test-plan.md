# Test Plan - Workflow Studio

Module: Platform Foundation
Phase: 7A / Sprint S3-S9
Owner: QA Architect (Agent 21)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 5 of 5 for Workflow Studio.

## Functional Tests

- Create, validate, approve, publish, supersede, and retire workflow definition.
- Start leave approval workflow and complete manager approval.
- Route conditional workflow through HR when rule matches.
- Delegate task and verify assignee changes.
- Escalate overdue task according to SLA.
- Pin running instance to original definition after new version publish.

## Security Tests

- Non-assignee cannot approve task.
- Delegate cannot exceed delegated permission boundaries.
- Cross-tenant task visibility is blocked.
- Payroll workflow requires elevated permission.
- Workflow publish requires approval for high-risk modules.

## Integration Tests

- Leave request starts workflow and receives final outcome.
- Attendance regularization uses workflow.
- Rule publish uses workflow approval.
- Configuration publish uses workflow approval.
- Events and audit records are emitted for decisions and escalations.

## Performance Tests

- Inbox query meets P95 target under large assigned-task volume.
- SLA scheduler handles due tasks without duplicate escalation.
- Workflow start and decision APIs meet API latency targets.

## Negative Tests

- Invalid workflow graph cannot publish.
- Missing assignee rule blocks validation.
- Duplicate decision request is idempotent.
- In-flight migration without approval is rejected.

## Exit Criteria

- Minimum 85% automated coverage.
- All Phase 7A workflow-consuming modules pass integration tests.
- Version pinning, delegation, SLA, and audit tests pass.
- No cross-tenant workflow leakage.

## External References

- OMG BPMN: https://www.omg.org/spec/BPMN/
- OpenTelemetry: https://opentelemetry.io/docs/

References last validated: 2026-06-28.

## Phase 7A Test Hardening Addendum

This test plan must comply with
`docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

QA Architect: ____ - Solution Architect: ____ - Product Owner: ____ - Status: Approved
