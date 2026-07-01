# Database Design - Branch / Office Hierarchy and Scoped Administration

Module: Platform Foundation / Core HR / Identity
Schema: `org`, `security`
Phase: Phase 7A / Sprint S1-S4
Owner: Database Architect
Created Date: 2026-06-29
Version: 1.0
Status: Approved

> Doc 3 of 5 for Branch / Office Hierarchy and Scoped Administration.

---

# 1. Tables

```text
org.BranchOffice
  BranchOfficeId, TenantId, ParentBranchOfficeId, Code, Name,
  BranchType, LegalEntityId, LocationId, TimeZone, Status,
  EffectiveFrom, EffectiveTo, audit columns

org.BranchOfficeHierarchyClosure
  BranchOfficeHierarchyClosureId, TenantId, AncestorBranchOfficeId,
  DescendantBranchOfficeId, Depth, EffectiveFrom, EffectiveTo, audit columns

org.EmployeeBranchAssignment
  EmployeeBranchAssignmentId, TenantId, EmployeeId, BranchOfficeId,
  AssignmentType, IsPrimary, EffectiveFrom, EffectiveTo,
  ApprovalReferenceId, audit columns

security.BranchScopeAssignment
  BranchScopeAssignmentId, TenantId, UserAccountId, RoleId,
  BranchOfficeId, IncludeChildBranches, ScopePurpose,
  EffectiveFrom, EffectiveTo, Status, ApprovalReferenceId, audit columns

security.BranchScopeDecisionLog
  BranchScopeDecisionLogId, TenantId, CorrelationId, UserAccountId,
  PermissionKey, RequestedBranchOfficeId, Decision, ReasonCode,
  PolicyVersion, EvaluatedAt, audit columns
```

---

# 2. Indexes

- `BranchOffice`: unique `(TenantId, Code)`.
- `BranchOffice`: `(TenantId, ParentBranchOfficeId, Status)`.
- `BranchOfficeHierarchyClosure`: unique `(TenantId, AncestorBranchOfficeId,
  DescendantBranchOfficeId, EffectiveFrom)`.
- `EmployeeBranchAssignment`: `(TenantId, EmployeeId, EffectiveFrom, EffectiveTo)`.
- `EmployeeBranchAssignment`: `(TenantId, BranchOfficeId, EffectiveFrom, EffectiveTo)`.
- `BranchScopeAssignment`: `(TenantId, UserAccountId, RoleId, BranchOfficeId, Status)`.
- `BranchScopeDecisionLog`: `(TenantId, CorrelationId)` and `(TenantId, UserAccountId,
  EvaluatedAt desc)`.

---

# 3. Integrity Rules

- Branch hierarchy cannot cross TenantId.
- A branch cannot be its own parent.
- Cycles are prohibited.
- Only one primary active branch assignment is allowed per employee unless a tenant policy
  explicitly allows multiple primary contexts.
- Branch scope assignments are effective-dated and approval-controlled where tenant policy
  requires.
- Branch closure rows are rebuilt or versioned when hierarchy changes.
- Soft delete preserves audit and historical scope decisions.

---

# 4. RLS and Security

All branch tables are tenant-scoped and protected by TenantId/RLS. Branch scope does not
replace tenant isolation. It is an additional ABAC boundary evaluated by application
services, authorization policies, reports, jobs, exports, workflows, and AI retrieval.

Sensitive decision logs must not store raw employee personal data. They store identifiers,
policy version, decision, reason, and correlation id.

---

# 5. Effective Dating

Branch hierarchy, employee branch assignment, and branch scope assignment are
effective-dated. Historical reports and payroll calculations must use the correct branch
assignment as of the relevant business date.

---

# 6. Acceptance Criteria

1. Branch hierarchy supports parent-child relationships within a tenant.
2. Branch scope assignments support include/exclude child branch behavior.
3. Employee branch assignment supports as-of queries.
4. RLS blocks cross-tenant branch records.
5. Branch decision logs are searchable by correlation id.
6. Migration scripts include rollback and hierarchy-cycle verification.

---

# 7. References

- DB-DESIGN-TENANT-001.
- DB-DESIGN-CORE-HR-001.
- DB-DESIGN-IDENTITY-001.
- SQL Server Row-Level Security:
  https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
- SQL Server temporal tables:
  https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables

References last validated: 2026-06-29.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-29  
Database Architect: Approved 2026-06-29  
Security Architect: Approved 2026-06-29  
Solution Architect: Approved 2026-06-29  
QA Architect: Approved 2026-06-29

(Status: Approved - owner approved 2026-06-29)
