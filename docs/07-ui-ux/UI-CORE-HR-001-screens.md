# UI Design - Core HR and Employee Self-Service

Module: Core HR
Phase: 7A / Sprint S4
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 4 of 5 for Core HR and ESS.

## Screen A - Employee Directory

Searchable tenant-scoped directory with filters for status, branch/office, department, location, manager,
legal entity, grade, and worker type. Rows show only permitted fields. Mobile view becomes
compact profile cards.

## Screen B - Employee Profile

Tabs: Overview, Job, Personal, Documents, Leave/Attendance summary, Payroll summary link,
History, Audit. Sensitive fields require permission and may be masked by default.

## Screen C - Assignment History

Timeline of job, manager, branch/office, department, location, grade, and legal entity changes. Supports
as-of view, version compare, and approved correction workflow.

## Screen D - ESS Profile

Employee self-service view with editable fields controlled by configuration. Submitted
changes show workflow status and history.

## Screen E - Organization Explorer

Tree and list view for org units and manager hierarchy with effective-date selector.

## Screen F - Admin Reference Data

Branches/offices, legal entities, locations, departments, designations, grades, cost centers, and employee
number series. Changes are effective-dated and audited.

## Acceptance Criteria

1. Employee directory respects role and scope.
2. Employee profile hides sensitive fields without permission.
3. ESS change request starts workflow and shows tracker.
4. Assignment history clearly shows effective periods.
5. Org explorer can view hierarchy as of selected date.
6. Branch/office assignment is visible and editable only within authorized scope.

## External References

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- BambooHR market reference: https://www.bamboohr.com/
- Zoho People market reference: https://www.zoho.com/people/

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Phase 7A Branch / Office Addendum

Core HR UI must comply with `docs/07-ui-ux/UI-BRANCH-001-screens.md` where employee branch
assignment and branch-scoped administration are exposed.

## Approval

UX/UI Architect: ____ - Product Owner: ____ - HR Domain Expert: ____ - Status: Approved
