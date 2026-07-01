# Technical Design - Leave Management

Module: Leave
Phase: 7A / Sprint S5
Owner: .NET Architect (Agent 13)
Created Date: 2026-06-14
Last Updated: 2026-06-28
Version: 2.0
Status: Approved
> Doc 2 of 5 for Leave Management.

## Architecture

Leave is a business module that consumes platform services: Tenant Catalog/RLS, Identity,
Effective Dating, Audit, Event Bus, Rule Engine, Workflow Studio, and Configuration-as-Data.
It owns the `leave` schema and publishes events; it does not own payroll calculation.

```text
Leave API -> Leave Application -> Leave Domain
              |      |       |       |
           Rules Workflow Ledger  Event Bus
```

## Components

- Leave Policy Service: type, eligibility, accrual, carry-forward, day-count policy.
- Leave Request Service: apply, withdraw, cancel, status, idempotency.
- Balance Ledger Service: reservation, debit, release, adjustment, rebuild projection.
- Accrual Job: posts periodic accrual and lapse transactions.
- Calendar Service Adapter: location holidays and working days.
- Payroll Feed Publisher: publishes approved unpaid leave and correction events.

## Key Flow - Apply Leave

1. Resolve tenant, employee, policy, and calendar.
2. Validate dates, overlap, balance, eligibility, and notice through Rule Engine.
3. Create request and reservation ledger transaction in one transaction.
4. Start workflow instance and publish `LeaveRequested`.
5. Return approval tracker and balance impact preview.

## Key Flow - Final Approval

On final workflow approval, convert reservation to debit exactly once, update projection,
audit decision, and publish `LeaveApproved`. Rejection or withdrawal releases reservation.

## API Requirements

APIs under `/api/v1/leave` cover leave types, balances, requests, withdrawal, policy
preview, accrual preview, adjustments, and history. OpenAPI must document idempotency,
date handling, rule errors, and balance response model.

## Security

Permissions include `Leave.Apply`, `Leave.ViewSelf`, `Leave.ViewTeam`, `Leave.Approve`,
`Leave.AdjustBalance`, and `Leave.Configure`. ABAC limits team and HR scope. Balance
adjustments require reason and may require workflow approval.

## Events

`LeaveRequested`, `LeaveApproved`, `LeaveRejected`, `LeaveWithdrawn`,
`LeaveBalanceAdjusted`, `LeavePolicyPublished`, `LeavePayrollImpactChanged`.

## Acceptance Criteria

1. Leave consumes shared Rule Engine and Workflow Studio.
2. Ledger prevents double debit under retry/concurrency.
3. Accrual and carry-forward are effective-dated and auditable.
4. Payroll feed events are emitted after approval/correction.
5. OpenAPI covers leave operations and error cases.

## External References

- RabbitMQ reliability: https://www.rabbitmq.com/docs/reliability
- JSON Schema: https://json-schema.org/
- Keka market reference: https://www.keka.com/

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

.NET Architect: ____ - Solution Architect: ____ - Security Architect: ____ - Status: Approved
