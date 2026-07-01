# UI Design - Leave Management

Module: Leave
Phase: 7A / Sprint S5
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-14
Last Updated: 2026-06-28
Version: 2.0
Status: Approved
> Doc 4 of 5 for Leave Management.

## Screen A - Apply Leave

Employee selects leave type, date range, half-day/full-day, reason, and attachment
reference where configured. The screen shows available balance, calculated days, holiday
impact, overlap warning, rule feedback, and approval preview before submit.

## Screen B - My Leave

Shows balance summary, reserved amount, used amount, upcoming requests, history, and
ledger drill-down. Withdraw action is shown only when policy and status allow it.

## Screen C - Team Leave Calendar

Manager view of team leave with privacy-aware labels, conflict hints, and approval actions.
ABAC controls which employees and details are visible.

## Screen D - Approval Task

Approver sees request details, balance, overlap/team calendar context, rule warnings, SLA,
delegation details, and decision buttons. Reject and return require comments.

## Screen E - Leave Policy Admin

Admin configures leave types, accrual, eligibility, carry-forward, day-count rules,
holiday calendars, workflow, and effective dates. Publish requires validation and impact
review.

## Screen F - Balance Adjustment

HR user enters adjustment, reason, effective date, employee, leave type, and optional
approval route. Screen shows before/after projected balance.

## Acceptance Criteria

1. Apply screen gives clear balance and rule feedback before submission.
2. Approval screen provides enough context for manager decision.
3. Admin can configure policy without visible technical details.
4. Balance ledger is available to authorized users.
5. Mobile views support apply, history, and approval.

## External References

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Zoho People market reference: https://www.zoho.com/people/
- greytHR market reference: https://www.greythr.com/

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

UX/UI Architect: ____ - Product Owner: ____ - HR Domain Expert: ____ - Status: Approved
