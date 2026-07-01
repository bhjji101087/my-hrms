# Feature Specification - Shift Foundation

Feature Name: Shift Foundation
Module: Attendance / Payroll / Core HR
Priority: Must
Phase: Phase 7A / Sprint S6-S8
Owner: Product Owner
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 1 of 5 required before implementation. Companion docs:
> TECH-SHIFT-FOUNDATION-001, DB-DESIGN-SHIFT-FOUNDATION-001,
> UI-SHIFT-FOUNDATION-001, TEST-SHIFT-FOUNDATION-001.
> Owner approved inclusion in Phase 7A on 2026-06-29.

---

# 1. Problem Statement

Attendance and payroll calculations cannot be reliable unless the system knows an
employee's expected working time. Phase 7A already includes Attendance and Payroll, so a
basic shift foundation is required now.

Full workforce rostering remains a later phase. Phase 7A delivers only the minimum
enterprise-grade shift capability needed for correct attendance and payroll outcomes.

---

# 2. User Stories

- As an HR/Admin user, I want to define shifts such as General, Morning, Evening, Night,
  and custom shifts, so attendance can be calculated correctly.
- As an Attendance Admin, I want to assign a shift to an employee with an effective date,
  so employee schedules are traceable over time.
- As a Branch Admin, I want to manage shifts available to my branch/office, so local work
  timings are respected.
- As a Payroll Admin, I want payroll to know the assigned shift, so late, early, overtime,
  night, weekly-off, and absence calculations can be correct where configured.
- As an Employee, I want to see my assigned shift and any approved shift override, so I
  understand expected work timing.

---

# 3. Scope

In scope for Phase 7A:

- Shift definition: code, name, branch/location availability, start time, end time, break
  minutes, grace minutes, shift type, weekly-off policy reference, and status.
- Custom shifts per tenant and branch/location.
- Effective-dated employee shift assignment.
- One-day or date-range shift override with approval where configured.
- Shift-aware attendance calculation.
- Shift-aware payroll impact for absence, late, early, overtime, night shift, and weekly
  off where tenant rules enable those outcomes.
- Shift history and audit.
- Shift filters in attendance views and reports.

Out of scope for Phase 7A:

- Full roster planning.
- Auto scheduling and demand planning.
- Shift bidding.
- Employee shift swap marketplace.
- Multi-week roster optimization.
- Capacity planning.
- Workforce forecasting.

---

# 4. Business Rules

1. A shift belongs to one tenant and may be available to all branches or selected
   branches/locations.
2. Shift start/end times are interpreted in the branch/location time zone unless an
   approved tenant policy states otherwise.
3. Overnight shifts are allowed.
4. Employee shift assignment is effective-dated.
5. Shift override cannot silently overwrite base assignment; it must be separately
   recorded and audited.
6. Attendance calculation must use the effective shift for the attendance date.
7. Payroll impact must use the same shift-derived attendance summary that was approved or
   locked for payroll.
8. Shift rules must be configurable through Rule Engine and Configuration-as-Data where
   policy variation exists.
9. Published shift definitions used by payroll-impacting attendance records must not be
   modified destructively.
10. Shift Foundation must remain compatible with future full roster management.

---

# 5. Approved Delivery

- Shift definition and shift versioning.
- Employee shift assignment.
- Shift override.
- Shift-aware attendance summary.
- Shift-aware payroll impact.
- Shift UI in Attendance Admin and employee self-service view.
- Shift audit, events, and tests.

---

# 6. Acceptance Criteria

| ID | Acceptance Criteria |
| --- | --- |
| SHIFT-AC-001 | Admin can create active/inactive shift definitions with timing, break, grace, and type. |
| SHIFT-AC-002 | Admin can assign shift to an employee using effective dates. |
| SHIFT-AC-003 | Attendance summary uses the employee's effective shift for the attendance date. |
| SHIFT-AC-004 | Overnight shift calculation works correctly across date boundary. |
| SHIFT-AC-005 | Shift override is audited and does not destroy assignment history. |
| SHIFT-AC-006 | Payroll receives shift-aware attendance impact where configured. |
| SHIFT-AC-007 | Branch/office scope restricts which shifts an admin can manage. |
| SHIFT-AC-008 | Full roster planning remains excluded from Phase 7A. |

---

# 7. References

- Existing approved docs: FEAT-ATTENDANCE-001, FEAT-PAYROLL-001,
  FEAT-RULE-ENGINE-001, FEAT-EFFECTIVE-DATING-001.
- Keka Attendance Management System:
  https://www.keka.com/attendance-management-system
- SQL Server temporal tables:
  https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables

References last validated: 2026-06-29.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
Solution Architect: Approved as Phase 7A amendment 2026-06-29  
Attendance Domain Expert: Approved as Phase 7A amendment 2026-06-29  
Payroll Domain Expert: Approved as Phase 7A amendment 2026-06-29  
QA Architect: Approved as Phase 7A amendment 2026-06-29

(Status: Approved - owner approved 2026-06-29)
