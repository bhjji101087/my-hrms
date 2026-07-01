# UI Design - Shift Foundation

Module: Attendance / Payroll / Core HR
Phase: Phase 7A / Sprint S6-S8
Owner: UX/UI Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 4 of 5 for Shift Foundation.

---

# 1. UX Goal

Make shift setup simple for administrators and clear for employees, while avoiding the
complexity of full roster planning in Phase 7A.

---

# 2. Screens

## Screen A - Shift Library

- List of shifts with code, name, shift type, start/end time, break, grace, status, and
  branch/location availability.
- Filters by branch/office, location, active/inactive, shift type.
- Create, duplicate, retire, and view history actions based on permission.

## Screen B - Shift Definition Detail

- Timing setup: start time, end time, overnight flag, break, grace-in, grace-out.
- Rule references: overtime, night shift, weekly-off.
- Branch/location availability.
- Publish workflow and impact preview.

## Screen C - Employee Shift Assignment

- Assign shift to one employee or a filtered employee set.
- Effective from/to.
- Branch/office and location context.
- Conflict warning when an assignment overlaps existing active assignment.

## Screen D - Shift Override

- One-day or date-range override.
- Reason and approval workflow where configured.
- Payroll impact warning if period is locked or already calculated.

## Screen E - Employee Shift View

- Employee can see current shift, upcoming scheduled change, and approved override.
- Read-only for employee unless tenant policy later enables request flow.

---

# 3. Cross-Module UI Rules

- Attendance screens show expected shift timing with actual punch comparison.
- Payroll exception screens identify shift-related attendance impact.
- Reports can filter by shift where user scope permits.
- Branch admins can manage only shifts available to their branch/office scope.

---

# 4. Accessibility and States

The screens must comply with `UI-PHASE-7A-STD-001-accessibility-states.md`.

Required states:

- No shift assigned.
- Shift publish pending approval.
- Shift conflict detected.
- Overnight shift warning.
- Payroll locked warning.
- Permission denied.
- Branch scope restricted.

---

# 5. Acceptance Criteria

| ID | Acceptance Criteria |
| --- | --- |
| UI-SHIFT-AC-001 | Admin can create and publish a shift definition. |
| UI-SHIFT-AC-002 | Admin can assign an effective-dated shift to an employee. |
| UI-SHIFT-AC-003 | Employee can view current and upcoming shift assignment. |
| UI-SHIFT-AC-004 | Attendance screen shows shift timing versus actual punches. |
| UI-SHIFT-AC-005 | Payroll-impact warnings appear for locked or calculated periods. |
| UI-SHIFT-AC-006 | Branch scope prevents unauthorized shift visibility and edits. |

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
UX/UI Architect: Approved 2026-06-29  
Attendance Domain Expert: Approved 2026-06-29  
Payroll Domain Expert: Approved 2026-06-29  
QA Architect: Approved 2026-06-29

(Status: Approved - owner approved 2026-06-29)
