# UI Standard - Phase 7A Accessibility and UX State Checklist

Document Owner: UX/UI Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved
> Applies to every Phase 7A UI design. This standard converts the review report's UI
> recommendations into a required checklist.

## 1. Required Screen States

Each Phase 7A screen must define:

- Loading state.
- Empty state.
- Validation error state.
- System error state.
- Permission-denied state.
- Tenant-suspended or feature-disabled state where applicable.
- Pending approval state.
- Locked period state where applicable.
- Export confirmation state for sensitive data.
- Mobile/responsive behavior.

## 2. Accessibility Requirements

Every Phase 7A screen must support:

- Keyboard navigation.
- Visible focus state.
- Screen reader labels for fields, actions, icons, and status chips.
- Error messages associated with fields.
- No color-only status communication.
- Accessible table navigation or card alternative on mobile.
- WCAG 2.2 AA contrast and interaction targets.

## 3. Sensitive Data UX

Screens showing audit, employee, payroll, attendance, leave, export, or report data must
include:

- Masking by default where required.
- Explicit reveal action where allowed.
- Data classification cue for sensitive screens.
- Export confirmation with purpose capture.
- Download audit note for payslips, reports, and evidence exports.

## 4. Approval and Workflow UX

Workflow-backed screens must show:

- Current status.
- Current approver or approver group where permitted.
- SLA/due date.
- Delegation or reassignment marker.
- Comment requirement for reject/return/correction actions.
- Audit/history link.

## 5. Acceptance Requirement

UI development cannot start for a Phase 7A module until its screen designs either include
this checklist directly or explicitly reference this standard.

## External References

- WCAG 2.2: https://www.w3.org/TR/WCAG22/

References last validated: 2026-06-29.

## Approval

UX/UI Architect: ____ - Accessibility Reviewer: ____ - Product Owner: ____ - Status: Approved
