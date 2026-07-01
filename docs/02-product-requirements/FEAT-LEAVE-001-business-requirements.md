# Feature Specification - Leave Management

Feature Name: Leave Management
Module: Leave
Phase: 7A / Sprint S5
Owner: Product Owner (Agent 2)
Created Date: 2026-06-14
Last Updated: 2026-06-28
Version: 2.0
Status: Approved
> Doc 1 of 5 for Leave Management. Implements PRD FR-004.

## Purpose

Leave Management allows employees to request time off, managers to approve with context,
HR to govern policy, and payroll to receive accurate leave loss-of-pay signals. All leave
types, accruals, carry-forward, eligibility, calendars, and approval rules must be
configuration-driven.

## Market and Enterprise Context

Zoho People, greytHR, Keka, Darwinbox, and BambooHR all position leave as a core employee
self-service and HR policy module. Customers value simple mobile leave requests, accurate
balances, calendar visibility, and configurable approvals. They become frustrated by wrong
balances, rigid policies, unclear approval status, poor holiday handling, and manual payroll
adjustments.

## Scope

In scope:
- Configurable leave types and policies.
- Accrual, carry-forward, lapse, adjustment, reservation, debit, and release ledger.
- Employee apply, withdraw, and request history.
- Manager/HR approvals through Workflow Studio.
- Holiday calendars, weekends, half-day support, and day-count policy.
- Payroll loss-of-pay feed and reporting events.

Out of scope:
- Leave encashment payout automation.
- Comp-off from overtime.
- Multi-country statutory leave packs beyond configurable foundation.

## Business Requirements

1. Tenant admins shall configure leave types and policies without code deployment.
2. Leave rules shall be effective-dated and evaluated through Rule Engine.
3. Leave balances shall be derived from an append-only ledger.
4. Requests shall support apply, withdraw, approve, reject, return, and cancel where policy allows.
5. Approval routing shall use Workflow Studio and support delegation/SLA/escalation.
6. Day count shall use configured work week, holiday calendar, half-day rules, and location.
7. Payroll-impacting approved leave shall emit events for payroll processing.
8. Every leave action and balance mutation shall be audited.

## Acceptance Criteria

1. Tenant admin creates a leave type, accrual policy, and approval workflow without deployment.
2. Employee sees accurate available, used, and reserved balances.
3. Approval debits balance exactly once even if the action is retried.
4. Holiday and weekend handling follows configured calendar.
5. Payroll receives approved unpaid leave signal through event bus.

## External References

- Zoho People leave market reference: https://www.zoho.com/people/
- greytHR market reference: https://www.greythr.com/
- Keka market reference: https://www.keka.com/
- BambooHR market reference: https://www.bamboohr.com/

References last validated: 2026-06-28.

## Approval

Product Owner: ____ - HR Domain Expert: ____ - Solution Architect: ____ - Status: Approved
