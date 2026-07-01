# Test Plan - Shift Foundation

Module: Attendance / Payroll / Core HR
Feature: Shift Foundation
Phase: Phase 7A / Sprint S6-S8
Owner: QA Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 5 of 5 for Shift Foundation.

---

# 1. Scope

In scope:

- Shift definition.
- Shift publishing.
- Employee shift assignment.
- Shift override.
- Shift-aware attendance summary.
- Shift-aware payroll impact.
- Branch/office scope for shifts.

Out of scope:

- Full roster planning.
- Auto scheduling.
- Shift swap marketplace.
- Workforce forecasting.

---

# 2. Test Scenarios

## Positive

- Create General shift and publish.
- Create overnight shift and publish.
- Assign shift to employee effective next month.
- Apply one-day shift override with approval.
- Attendance summary uses assigned shift.
- Payroll impact reflects approved shift-aware attendance summary.

## Negative

- Publish shift without valid start/end time is rejected.
- Unauthorized branch admin cannot edit another branch's shift.
- Overlapping active employee shift assignment is rejected unless policy allows it.
- Shift assignment after payroll lock requires correction workflow.
- Employee cannot edit their own assigned shift in Phase 7A.

## Edge Cases

- Overnight shift crosses date boundary.
- Employee transfers branch and shift in same pay period.
- Holiday work on assigned shift.
- Weekly-off attendance with overtime rule enabled.
- Grace period exactly at boundary.
- Shift time zone differs from user's browser time zone.

---

# 3. Automation

- Unit tests for Shift Resolver and time boundary rules.
- Integration tests for attendance summary and payroll impact.
- E2E tests for admin shift setup and employee shift view.
- Security tests for branch scope and unauthorized shift assignment.

---

# 4. Security Testing

- Tenant RLS blocks cross-tenant shift data.
- Branch scope blocks unauthorized shift management.
- Payroll-impacting shift changes require elevated permission.
- Audit records are created for shift publish, assignment, override, and denied attempts.

---

# 5. Performance Testing

- Shift resolution under attendance import volume.
- Bulk shift assignment for filtered employee set.
- Attendance summary recalculation after shift override.
- Payroll snapshot with shift-aware attendance inputs.

---

# 6. Exit Criteria

- Shift Resolver unit tests pass for regular and overnight shifts.
- Attendance and payroll integration tests pass.
- No P1/P2 security defects remain.
- OpenAPI and audit evidence verified.
- Unit coverage at least 85 percent for Shift Foundation services.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
QA Architect: Approved 2026-06-29  
Attendance Domain Expert: Approved 2026-06-29  
Payroll Domain Expert: Approved 2026-06-29  
Security Architect: Approved 2026-06-29

(Status: Approved - owner approved 2026-06-29)
