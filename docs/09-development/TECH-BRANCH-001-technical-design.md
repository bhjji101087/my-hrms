# Technical Design - Branch / Office Hierarchy and Scoped Administration

Module: Platform Foundation / Core HR / Identity
Phase: Phase 7A / Sprint S1-S4
Owner: Solution Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 2 of 5 for Branch / Office Hierarchy and Scoped Administration.

---

# 1. Architecture

Branch / Office Hierarchy is a tenant-scoped organizational boundary layered under Tenant
Catalog and consumed by Identity, Core HR, Leave, Attendance, Payroll, Reports, Audit, and
Configuration.

```text
Request -> Tenant Context -> Identity PEP/PDP -> Branch Scope Resolver
        -> Module Service -> Repository / Report / Workflow / Job
```

The feature does not create child tenants. Branches/offices remain inside one tenant and
are protected by TenantId plus branch/office ABAC scope.

---

# 2. Components

- Branch Hierarchy Service: manages branch/office nodes, parent-child relationships,
  lifecycle status, and effective dates.
- Branch Scope Resolver: calculates allowed branches for user, role, delegation, and
  policy context.
- Branch Assignment Adapter: integrates Core HR employee assignments with branch/office
  scope.
- Authorization Policy Adapter: exposes branch attributes to the Identity PDP and Rule
  Engine.
- Cache Invalidation Publisher: emits branch hierarchy and scope change events.
- Audit Adapter: records branch setup, branch assignment, scope grants, denied attempts,
  and export decisions.

---

# 3. Authorization Rules

- Tenant admin scope: all branches/offices under the tenant.
- Branch admin scope: assigned branch/office only, plus child branches only if policy
  explicitly allows inheritance.
- Employee scope: self data, permitted directory information, and approved branch-level
  operational views.
- Manager scope: manager chain plus branch/location policy where configured.
- Payroll scope: legal entity, payroll group, branch, and data sensitivity.
- Auditor scope: approved branch/office and purpose-limited audit evidence.

Every authorization decision must capture tenant id, user id, permission, branch scope,
ABAC policy version, decision, reason, and correlation id.

---

# 4. API Requirements

OpenAPI must document endpoints under `/api/v1/branches` and branch-scope fields in
affected module APIs.

Example endpoints:

- `GET /api/v1/branches`
- `POST /api/v1/branches`
- `GET /api/v1/branches/{id}/tree`
- `POST /api/v1/branches/{id}/scope-assignments`
- `GET /api/v1/branches/{id}/employees`
- `GET /api/v1/security/branch-scopes`

Module APIs that return employee or operational data must support server-side branch scope
filtering. Client-provided branch filters may reduce result sets but cannot expand the
caller's allowed scope.

---

# 5. Events

- `BranchCreated`
- `BranchUpdated`
- `BranchHierarchyChanged`
- `BranchScopeAssigned`
- `BranchScopeRevoked`
- `EmployeeBranchAssignmentChanged`
- `BranchScopePolicyChanged`

Events must include tenant id, branch id, hierarchy version, correlation id, actor, and
classification. Sensitive data must be minimized.

---

# 6. Integration Rules

- Core HR owns employee branch assignment through effective-dated employee assignment.
- Identity owns role, permission, and ABAC decisioning.
- Reports use branch scope as a mandatory security filter where employee data is present.
- Payroll applies branch scope together with legal entity and payroll group.
- Attendance applies branch scope together with location, device, and employee scope.
- Leave applies branch scope for manager, HR, and admin views.
- AI retrieval must not expose branch data outside authorized scope.

---

# 7. Degraded Modes

| Condition | Behavior |
| --- | --- |
| Branch scope cache unavailable | Read from SQL and fail closed for high-risk APIs. |
| Branch hierarchy conflict | Reject publish and create audit/security event. |
| User has no branch scope | Permit only self-service where policy allows. |
| Branch suspended | Block branch-scoped operations except approved audit/export tasks. |

---

# 8. Acceptance Criteria

1. Branch scope is resolved after tenant context and before module service access.
2. Tenant admin can access all branch/office data within the tenant.
3. Branch admin cannot access another branch's data.
4. Branch scope works for API, UI, reports, jobs, exports, workflows, and AI retrieval.
5. Branch hierarchy changes emit audit records and invalidation events.
6. OpenAPI includes branch endpoints and scope-filter behavior.

---

# 9. References

- ADR-006 Tenant Context and Data Access.
- ADR-008 Identity and Access.
- DB-DESIGN-BRANCH-001.
- Microsoft SQL Server Row-Level Security:
  https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security

References last validated: 2026-06-29.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
Solution Architect: Approved 2026-06-29  
.NET Architect: Approved 2026-06-29  
Security Architect: Approved 2026-06-29  
Database Architect: Approved 2026-06-29

(Status: Approved - owner approved 2026-06-29)
