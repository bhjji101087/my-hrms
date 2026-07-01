# Database Design - Shift Foundation

Module: Attendance / Payroll / Core HR
Schema: `attendance`
Phase: Phase 7A / Sprint S6-S8
Owner: Database Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 3 of 5 for Shift Foundation.

---

# 1. Tables

```text
attendance.ShiftDefinition
  ShiftDefinitionId, TenantId, Code, Name, ShiftType,
  AvailableToAllBranches, Status, CurrentPublishedVersionId,
  audit columns

attendance.ShiftDefinitionVersion
  ShiftDefinitionVersionId, TenantId, ShiftDefinitionId, VersionNumberText,
  EffectiveFrom, EffectiveTo, StartTimeLocal, EndTimeLocal,
  BreakMinutes, GraceInMinutes, GraceOutMinutes,
  IsOvernight, WeeklyOffRuleSetId, OvertimeRuleSetId, NightShiftRuleSetId,
  BranchAvailabilityJson, Status, ApprovalWorkflowInstanceId,
  PublishedBy, PublishedAt, audit columns

attendance.EmployeeShiftAssignment
  EmployeeShiftAssignmentId, TenantId, EmployeeId, ShiftDefinitionVersionId,
  BranchOfficeId, LocationId, AssignmentType,
  EffectiveFrom, EffectiveTo, ApprovalReferenceId, audit columns

attendance.EmployeeShiftOverride
  ShiftOverrideId, TenantId, EmployeeId, ShiftDefinitionVersionId,
  BranchOfficeId, OverrideDateFrom, OverrideDateTo,
  Reason, Status, WorkflowInstanceId, audit columns

attendance.ShiftResolutionLog
  ShiftResolutionLogId, TenantId, EmployeeId, AttendanceDate,
  BranchOfficeId, ShiftDefinitionVersionId, ResolutionSource,
  CorrelationId, ResolvedAt, audit columns
```

---

# 2. Indexes

- `ShiftDefinition`: unique `(TenantId, Code)`.
- `ShiftDefinitionVersion`: `(TenantId, ShiftDefinitionId, Status, EffectiveFrom)`.
- `EmployeeShiftAssignment`: `(TenantId, EmployeeId, EffectiveFrom, EffectiveTo)`.
- `EmployeeShiftAssignment`: `(TenantId, BranchOfficeId, EffectiveFrom, EffectiveTo)`.
- `EmployeeShiftOverride`: `(TenantId, EmployeeId, OverrideDateFrom, OverrideDateTo)`.
- `ShiftResolutionLog`: `(TenantId, EmployeeId, AttendanceDate)`.

---

# 3. Integrity Rules

- Shift definitions are tenant-scoped.
- Published shift definition versions are immutable.
- Employee shift assignments are effective-dated.
- Only one active base shift assignment should exist per employee/date unless an approved
  tenant policy allows multiple shift contexts.
- Shift overrides do not delete or overwrite base assignments.
- Overnight shifts must explicitly set `IsOvernight`.
- Branch availability must reference branches/offices within the same tenant.

---

# 4. RLS and Security

All shift tables include TenantId and RLS. Branch/office scope applies to admin screens,
API queries, reports, exports, jobs, and assignment changes. Payroll-impacting shift
changes require elevated permission and may require workflow approval.

---

# 5. Retention

Shift definitions, assignments, overrides, and resolution logs used by payroll or audit
must be retained for the same retention class as related attendance and payroll records.

---

# 6. Acceptance Criteria

1. Shift assignment supports as-of query by employee and date.
2. Published shift versions are immutable.
3. Shift override preserves base assignment history.
4. RLS blocks cross-tenant shift data.
5. Branch scope blocks unauthorized shift management.
6. Payroll-impacting shift records are retained and auditable.

---

# 7. References

- DB-DESIGN-ATTENDANCE-001.
- DB-DESIGN-PAYROLL-001.
- DB-DESIGN-BRANCH-001.
- SQL Server temporal tables:
  https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables

References last validated: 2026-06-29.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
Database Architect: Approved 2026-06-29  
Attendance Domain Expert: Approved 2026-06-29  
Payroll Domain Expert: Approved 2026-06-29  
Security Architect: Approved 2026-06-29  
QA Architect: Approved 2026-06-29

(Status: Approved - owner approved 2026-06-29)
