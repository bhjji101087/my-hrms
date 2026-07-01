# Test Plan - Branch / Office Hierarchy and Scoped Administration

Module: Platform Foundation / Core HR / Identity
Feature: Branch / Office Hierarchy and Scoped Administration
Phase: Phase 7A / Sprint S1-S4
Owner: QA Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 5 of 5 for Branch / Office Hierarchy and Scoped Administration.

---

# 1. Scope

In scope:

- Branch hierarchy creation and update.
- Branch admin scope assignment.
- Employee branch assignment.
- Complete tenant admin full visibility.
- Branch admin restricted visibility.
- Cross-module branch filtering.
- Branch-scope audit and authorization decision logs.

Out of scope:

- Franchise billing.
- Separate child-tenant contracts.
- Advanced matrix org design.

---

# 2. Test Scenarios

## Positive

- Tenant admin creates branch hierarchy.
- Tenant admin sees all branch employees.
- Branch admin sees employees in assigned branch.
- Branch admin with child-scope flag sees child branches.
- Employee branch assignment can be scheduled for a future date.
- Branch filter reduces report data within allowed scope.

## Negative

- Branch admin attempts to view another branch employee and receives 403.
- Branch admin attempts export outside scope and receives denial.
- User without branch scope cannot access branch admin pages.
- Attempt to create branch parent cycle is rejected.
- Attempt to assign branch from another tenant is rejected.

## Edge Cases

- Employee transfers branch mid-pay-period.
- Branch suspended while workflow tasks are open.
- Branch hierarchy changes while report export is running.
- Tenant admin delegates branch scope temporarily.
- Cache unavailable during branch scope decision.

---

# 3. Automation

- Unit tests for scope resolver and hierarchy validation.
- Integration tests for API, RLS, ABAC, reports, exports, and workflows.
- E2E tests for tenant admin and branch admin user journeys.
- Security abuse tests for cross-branch IDOR and filter manipulation.

---

# 4. Security Testing

- Tenant isolation remains enforced before branch scope.
- Branch admin cannot enumerate restricted branch ids.
- Branch filters cannot expand allowed scope.
- Audit records are created for denied access and exports.
- AI retrieval and reports apply branch scope.

---

# 5. Performance Testing

- Branch tree load under expected tenant hierarchy size.
- Branch scope decision latency under cached and uncached modes.
- Employee directory and report filters with branch scope.
- Hierarchy closure rebuild performance.

---

# 6. Exit Criteria

- 100 percent pass for tenant and branch isolation tests.
- No unresolved P1/P2 security defects.
- Unit coverage at least 85 percent for branch services.
- E2E tests pass for tenant admin and branch admin workflows.
- OpenAPI and audit evidence verified.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
QA Architect: Approved 2026-06-29  
Security Architect: Approved 2026-06-29  
Solution Architect: Approved 2026-06-29

(Status: Approved - owner approved 2026-06-29)
