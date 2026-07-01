# UI Design - Branch / Office Hierarchy and Scoped Administration

Module: Platform Foundation / Core HR / Identity
Phase: Phase 7A / Sprint S1-S4
Owner: UX/UI Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 4 of 5 for Branch / Office Hierarchy and Scoped Administration.

---

# 1. UX Goal

Make branch/office scope visible and understandable without exposing unauthorized data.
Complete tenant administrators can operate across all branches. Branch administrators see
only their assigned branch/office scope unless policy grants child-branch visibility.

---

# 2. Screens

## Screen A - Branch / Office Directory

- Tree and table view of branches/offices.
- Filters by status, branch type, region, legal entity, and location.
- Visible only according to tenant and branch-scope permissions.
- Complete tenant admin sees full hierarchy.
- Branch admin sees assigned scope and allowed child branches.

## Screen B - Branch / Office Detail

- Profile, parent branch, legal entity, location, time zone, working calendar, status.
- Tabs: employees, admins, policies, audit, integrations.
- Sensitive tabs hidden when permission is missing.

## Screen C - Branch Scope Assignment

- Assign user/role to branch or office scope.
- Option to include child branches only when policy allows.
- Effective from/to dates.
- Approval status and audit history.

## Screen D - Employee Branch Assignment

- Current and historical branch assignment.
- Primary branch indicator.
- Effective-dated changes with reason and approval where required.
- Impact warning for payroll, attendance, reporting, and workflow.

## Screen E - Branch Access Denied State

- Clear permission message without revealing restricted branch data.
- Correlation id for support.
- No branch names from unauthorized scope are exposed.

---

# 3. Cross-Module UI Rules

- Employee directory, attendance, leave, payroll, reports, and audit screens must apply
  server-side branch scope.
- Branch filter controls can narrow visible data but cannot expand authorization.
- Export buttons must be disabled or approval-gated where branch-sensitive data is present.
- Audit links must show scope decision evidence where permitted.

---

# 4. Accessibility and States

The screens must comply with `UI-PHASE-7A-STD-001-accessibility-states.md`.

Required states:

- Loading branch hierarchy.
- Empty branch list.
- Permission denied.
- Branch suspended.
- Branch hierarchy conflict.
- Pending approval.
- Export approval required.

---

# 5. Acceptance Criteria

| ID | Acceptance Criteria |
| --- | --- |
| UI-BRANCH-AC-001 | Tenant admin can navigate full branch tree. |
| UI-BRANCH-AC-002 | Branch admin sees only assigned branch scope. |
| UI-BRANCH-AC-003 | Employee branch assignment supports effective-date view. |
| UI-BRANCH-AC-004 | Unauthorized branch data is not displayed in filters, counts, tables, exports, or audit preview. |
| UI-BRANCH-AC-005 | Screens meet accessibility, responsiveness, localization, and white-label requirements. |

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
UX/UI Architect: Approved 2026-06-29  
Security Architect: Approved 2026-06-29  
QA Architect: Approved 2026-06-29

(Status: Approved - owner approved 2026-06-29)
