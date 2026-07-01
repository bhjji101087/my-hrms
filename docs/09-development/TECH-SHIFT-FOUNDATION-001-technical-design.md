# Technical Design - Shift Foundation

Module: Attendance / Payroll / Core HR
Phase: Phase 7A / Sprint S6-S8
Owner: Solution Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 2 of 5 for Shift Foundation.

---

# 1. Architecture

Shift Foundation is owned by Attendance but consumed by Payroll, Core HR, Reports, Rules,
Workflow, and Configuration.

```text
Admin UI/API -> Shift Service -> Effective Dating -> SQL Server
                         +-> Rule Engine
                         +-> Audit/Event Bus

Punches -> Attendance Engine -> Shift Resolver -> Attendance Summary -> Payroll Impact
```

Full roster planning will be implemented later. Phase 7A provides stable shift definitions,
effective-dated employee shift assignment, and shift-aware attendance/payroll calculations.

---

# 2. Components

- Shift Definition Service: creates, validates, versions, publishes, and retires shift
  definitions.
- Shift Assignment Service: assigns effective-dated shifts to employees.
- Shift Override Service: records approved one-day or date-range overrides.
- Shift Resolver: returns the effective shift for employee/date/branch/time zone.
- Attendance Calculation Adapter: uses shift timing for late, early, absence, overtime,
  night shift, break, weekly-off, and holiday-work calculations where rules enable them.
- Payroll Impact Adapter: exposes shift-derived attendance impacts to payroll snapshots.

---

# 3. Runtime Rules

- Shift resolution uses tenant id, employee id, attendance date, branch/office, location,
  and effective dates.
- Shift time is interpreted in branch/location time zone.
- Overnight shift end date may be next calendar day.
- Shift assignment changes after payroll lock require correction workflow.
- Published shift definitions referenced by approved attendance summaries remain
  historically explainable.
- Client filters cannot expand branch or employee scope.

---

# 4. API Requirements

OpenAPI must document endpoints under `/api/v1/attendance/shifts`.

Example endpoints:

- `GET /api/v1/attendance/shifts`
- `POST /api/v1/attendance/shifts`
- `POST /api/v1/attendance/shifts/{id}/publish`
- `POST /api/v1/attendance/shift-assignments`
- `POST /api/v1/attendance/shift-overrides`
- `GET /api/v1/attendance/employees/{employeeId}/shift?date=YYYY-MM-DD`
- `POST /api/v1/attendance/shifts/impact-preview`

---

# 5. Events

- `ShiftDefinitionPublished`
- `ShiftDefinitionRetired`
- `EmployeeShiftAssigned`
- `EmployeeShiftAssignmentChanged`
- `ShiftOverrideApproved`
- `ShiftPayrollImpactChanged`

Events must include tenant id, employee id where applicable, branch/office id, effective
date, shift version id, correlation id, and classification.

---

# 6. Integration Rules

- Attendance owns Shift Foundation data.
- Core HR provides employee, branch, location, and assignment context.
- Rule Engine evaluates late, early, overtime, night, weekly-off, and absence rules.
- Workflow approves shift override and payroll-impacting corrections where configured.
- Payroll consumes shift-aware attendance summaries, not raw shift data alone.
- Reporting exposes shift filters and projections where authorized.

---

# 7. Degraded Modes

| Condition | Behavior |
| --- | --- |
| No shift assigned | Use tenant default shift only if configured; otherwise mark summary exception. |
| Shift resolver unavailable | Attendance calculation fails safely and records exception. |
| Time zone missing | Reject shift publish or assignment until fixed. |
| Payroll already locked | Require correction workflow for shift-affecting change. |

---

# 8. Acceptance Criteria

1. Shift Resolver returns the correct effective shift for employee/date.
2. Attendance summary uses shift timing for late/early/absence calculations.
3. Overnight shifts are calculated correctly across date boundary.
4. Shift override creates audit/event records and preserves base assignment history.
5. Payroll receives shift-aware attendance impact through approved snapshot flow.
6. OpenAPI documents shift endpoints and error responses.

---

# 9. References

- TECH-ATTENDANCE-001.
- TECH-PAYROLL-001.
- TECH-EFFECTIVE-DATING-001.
- Keka Attendance Management System:
  https://www.keka.com/attendance-management-system

References last validated: 2026-06-29.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
Solution Architect: Approved 2026-06-29  
.NET Architect: Approved 2026-06-29  
Attendance Domain Expert: Approved 2026-06-29  
Payroll Domain Expert: Approved 2026-06-29  
QA Architect: Approved 2026-06-29

(Status: Approved - owner approved 2026-06-29)
