# UI Design - Attendance and First Connector

Module: Attendance
Phase: 7A / Sprint S6
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 4 of 5 for Attendance.

## Screen A - My Attendance

Employee views daily status, first in, last out, work time, late/early marks, leave/holiday
context, assigned shift, and regularization option. Calendar and list views are available.

## Screen B - Regularization Request

Employee selects date, requested in/out time, reason, and attachment reference where
allowed. The screen shows original punch data, rule impact, and approval preview.

## Screen C - Team Attendance

Manager view with filters for date, status, department, location, missing punch, late, and
pending regularization. Bulk approval follows workflow rules and permissions.

## Screen D - Attendance Device Center

Admin configures first connector adapter, maps device employees, views sync health, last
sync, rejected records, retry status, and reconciliation results.

## Screen E - Attendance Policy Admin

Admin configures late/early/absence rules, workday policy, holiday calendar, shift
foundation references, approval workflow, and effective dates.

## Screen F - Shift Foundation

Admin views shift library, shift definition detail, employee shift assignment, and shift
override screens as defined in `UI-SHIFT-FOUNDATION-001-screens.md`.

## Acceptance Criteria

1. Employee can request regularization with clear original/changed values.
2. Manager sees team attendance only within scope.
3. Device center shows connector sync health and errors.
4. Policy admin validates rules before publish.
5. Payroll impact is visible to authorized payroll/HR users.
6. Attendance screens show expected shift timing compared with actual punches.

## External References

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Keka market reference: https://www.keka.com/
- greytHR market reference: https://www.greythr.com/

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Phase 7A Shift Foundation Addendum

Attendance UI must comply with `docs/07-ui-ux/UI-SHIFT-FOUNDATION-001-screens.md`.

## Approval

UX/UI Architect: ____ - Product Owner: ____ - HR Operations Reviewer: ____ - Status: Approved
