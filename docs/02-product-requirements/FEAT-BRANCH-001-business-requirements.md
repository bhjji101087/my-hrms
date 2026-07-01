# Feature Specification - Branch / Office Hierarchy and Scoped Administration

Feature Name: Branch / Office Hierarchy and Scoped Administration
Module: Platform Foundation / Core HR / Identity
Priority: Must
Phase: Phase 7A / Sprint S1-S4
Owner: Product Owner
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 1 of 5 required before implementation. Companion docs:
> TECH-BRANCH-001, DB-DESIGN-BRANCH-001, UI-BRANCH-001, TEST-BRANCH-001.
> Owner approved inclusion in Phase 7A on 2026-06-29.

---

# 1. Problem Statement

Enterprise customers commonly operate through multiple branches, offices, locations,
legal entities, departments, or business units under one tenant. A complete tenant
administrator needs visibility across the whole tenant, while branch or office
administrators must operate only within their assigned scope.

The platform already supports tenant isolation, locations, legal entities, departments,
and ABAC. This feature makes the branch/office model explicit so data boundaries are not
left to interpretation during implementation.

---

# 2. User Stories

- As a complete Tenant Administrator, I want to view and administer all branches/offices
  under my tenant, so I can manage the full organization.
- As a Branch Administrator, I want to manage only my assigned branch/office, so branch
  operations remain separate and secure.
- As an Office HR Admin, I want to manage employees, attendance, leave, and local setup
  only for my office scope, so I do not access another office's information.
- As an Employee, I want to see only my own data and allowed branch-level information, so
  other branch data remains private.
- As an Auditor, I want every scoped access decision to be traceable, so branch-level data
  access can be investigated.

---

# 3. Scope

In scope for Phase 7A:

- Tenant-owned branch/office hierarchy.
- Branch/office as an explicit organizational scope under a tenant.
- Parent-child hierarchy for branch, office, region, area, and site structures.
- Branch/office assignment to employees through Core HR.
- Branch/office-scoped administration using RBAC plus ABAC.
- Complete tenant admin visibility across all branches/offices.
- Branch admin visibility restricted to assigned branch/office scope.
- Branch-aware filtering in Core HR, Leave, Attendance, Payroll, Reports, Audit, and
  Configuration where the module exposes employee or operational data.
- Effective dating for branch assignment and branch hierarchy changes.
- Audit of branch setup, assignment, scope grants, and cross-scope denied attempts.

Out of scope for Phase 7A:

- Franchise accounting.
- Branch-level billing.
- Independent child-tenant commercial contracts.
- Separate tenant databases per branch unless approved as a later placement strategy.
- Complex matrix organizations beyond explicit hierarchy and ABAC scope.

---

# 4. Business Rules

1. A branch/office belongs to exactly one tenant.
2. A branch/office may have a parent branch/office under the same tenant.
3. Complete tenant administrators can access all branch/office data within the tenant.
4. Branch administrators can access only assigned branch/office scope and optionally
   approved child branches where policy allows.
5. Employees cannot view other branch employee data unless a role and ABAC policy grants
   that access.
6. Branch scope never bypasses tenant isolation; TenantId remains mandatory on all tables.
7. Branch/office assignment is effective-dated for employees and configuration.
8. Branch hierarchy changes require audit and may require Workflow approval by tenant
   policy.
9. Branch scope must be applied consistently in APIs, UI, jobs, reports, exports,
   workflows, integrations, and AI retrieval.
10. Branch names, codes, and hierarchy must be configurable per tenant without code change.

---

# 5. Approved Delivery

- Branch/office hierarchy management.
- Branch/office admin role and scope assignment.
- Branch/office-aware ABAC attributes.
- Branch assignment in employee profile and employee assignment history.
- Branch filters and permission checks in employee directory, attendance, leave, payroll,
  reports, audit views, and exports.
- Branch-level working calendar and location linkage where configured.
- Branch hierarchy and scope audit evidence.

---

# 6. Acceptance Criteria

| ID | Acceptance Criteria |
| --- | --- |
| BRANCH-AC-001 | Tenant admin can view and administer all branches/offices under the tenant. |
| BRANCH-AC-002 | Branch admin can view and administer only assigned branch/office scope. |
| BRANCH-AC-003 | Branch admin cannot access another branch's employees, attendance, leave, payroll, reports, or audit data unless explicitly granted. |
| BRANCH-AC-004 | Branch hierarchy supports parent-child relationships within the same tenant. |
| BRANCH-AC-005 | Employee branch assignment is effective-dated and auditable. |
| BRANCH-AC-006 | APIs, UI, reports, exports, background jobs, and workflows enforce branch scope. |
| BRANCH-AC-007 | Branch setup and scope changes create audit records and invalidation events. |
| BRANCH-AC-008 | OpenAPI documents branch hierarchy and branch-scope administration endpoints. |

---

# 7. References

- Existing approved docs: FEAT-TENANT-001, FEAT-IDENTITY-001, FEAT-CORE-HR-001,
  DB-DESIGN-TENANT-001, DB-DESIGN-CORE-HR-001, DB-DESIGN-IDENTITY-001.
- Microsoft SQL Server Row-Level Security:
  https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
- Microsoft Azure Architecture Center - multitenant request mapping:
  https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/map-requests

References last validated: 2026-06-29.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
Solution Architect: Approved as Phase 7A amendment 2026-06-29  
Security Architect: Approved as Phase 7A amendment 2026-06-29  
Database Architect: Approved as Phase 7A amendment 2026-06-29  
QA Architect: Approved as Phase 7A amendment 2026-06-29

(Status: Approved - owner approved 2026-06-29)
