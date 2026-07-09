# Feature Specification - Tenant Catalog and Row-Level Security

Feature Name: Tenant Catalog and Isolation
Requirement ID: FR-015
Module: Platform / Core
Priority: Must
Phase: Phase 7A / Sprint S1 - first foundation to build
Owner: Product Owner
Created Date: 2026-06-14
Last Updated: 2026-06-27
Version: 1.1
Status: Approved

> Doc 1 of 5 required before implementation. Companion docs:
> TECH-TENANT-001, DB-DESIGN-TENANT-001, UI-TENANT-001, TEST-TENANT-001.
> No Tenant Catalog or RLS implementation may start until all five documents are Approved.

---

# 1. Problem Statement

Every HRMS capability depends on tenant isolation. The platform must know which customer
tenant a request belongs to, where that tenant's data lives, what capabilities the tenant
is entitled to use, and which visual/domain configuration applies. More importantly, the
platform must make cross-tenant access impossible even when an application developer forgets
to add a tenant filter.

The Tenant Catalog and Row-Level Security foundation must provide:

- A trusted control-plane catalog of tenants, placement, region, shard, status,
  entitlements, provider configuration, and branding references.
- A server-side tenant-context pipeline that never trusts tenant IDs from request bodies.
- SQL Server Row-Level Security (RLS) on every tenant-scoped table.
- A repository-injected tenant predicate as application-layer defense in depth (ADR-037).
- Tenant lifecycle controls for provisioning, activation, suspension, offboarding, export,
  purge, and placement change.
- Audit, RBAC, ABAC, OpenAPI, and automated isolation proof for every tenant operation.

This feature is the first build item because all later modules - Identity, Effective Dating,
Rule Engine, Workflow, Leave, Attendance, Payroll, AI, Reporting, and integrations - depend
on trustworthy tenant context and tenant-scoped data access.

---

# 2. Business Goals

1. Prevent cross-tenant data disclosure, modification, deletion, and cache/search leakage.
2. Support shared, pooled, sharded, and dedicated tenant placement without code changes.
3. Allow platform operations to provision, suspend, migrate, and offboard tenants safely.
4. Allow tenant administrators to manage company setup and permitted configuration.
5. Provide evidence that isolation is enforced and tested before any business module is
   implemented.
6. Keep future modules open for extension by relying on common tenant context,
   entitlements, provider configuration, and audit controls.
7. Support explicit branch/office hierarchy inside a tenant so complete tenant admins can
   administer all offices while branch/office admins operate only within assigned scope.

---

# 3. User Stories

- As a Platform Owner, I want to provision a tenant with region, placement, plan,
  entitlements, provider defaults, and branding references, so that a customer can be
  onboarded consistently.
- As a Platform Owner, I want to suspend or offboard a tenant with audit evidence, so that
  contractual, payment, abuse, or compliance actions can be enforced safely.
- As a Platform Owner, I want to move a tenant from pooled placement to a dedicated database
  or another shard through catalog configuration, so that growth and compliance needs do not
  require application code changes.
- As a Tenant Administrator, I want to manage company profile, locations, localization,
  working calendar, and allowed modules, so that the platform reflects my organization.
- As a Tenant Administrator, I want to manage branch/office hierarchy, so my tenant can
  represent head office, regional offices, branches, and sites.
- As a Branch Administrator, I want to manage only my assigned branch/office scope, so I
  cannot view or change another branch's employees or operational data.
- As a Security Reviewer, I want proof that unfiltered queries cannot return another
  tenant's data, so that tenant isolation is independently verified.
- As the System, I need every request, background job, API, cache key, search index, event,
  and audit record to carry trusted tenant context.

---

# 4. Scope

In scope:

- Tenant catalog and tenant status lifecycle.
- Tenant-to-region, tenant-to-shard, and tenant-to-placement mapping.
- Pooled and dedicated database placement metadata.
- Tenant context resolution from validated token and approved host/domain mapping.
- Tenant entitlements and feature flags.
- Tenant branding and white-label domain references.
- Tenant provider configuration references.
- Branch/office hierarchy and branch/office scoped administration.
- Repository-injected tenant predicate (ADR-037).
- SQL Server RLS filter and block predicates.
- Tenant-aware connection factory and session-context setup.
- Tenant-aware background job execution.
- Suspension, activation, offboarding, export, purge initiation, and placement-change
  workflow.
- Audit, security, telemetry, and test evidence.

Out of scope:

- Self-service public signup.
- Billing and payment collection.
- Fully automated physical tenant database migration tooling.
- Customer-specific code forks.
- Cross-tenant analytics data marts.
- Identity provider SCIM implementation details, except tenant mapping references.
- Business module data models beyond enforcing tenant requirements.

---

# 5. Business Rules

1. Every tenant-scoped table must include `TenantId` and be protected by SQL Server RLS.
2. Every tenant-scoped query must use the resolved server-side tenant context.
3. `TenantId` from request body, query string, or untrusted headers is never authoritative.
4. Tenant context is resolved from validated identity claims and approved host/domain
   mapping. Host/domain mapping is a routing hint, not authorization proof.
5. If tenant context is missing, ambiguous, suspended, offboarding-blocked, or unauthorized,
   the request fails closed.
6. Platform-owner tenant lifecycle actions require elevated platform role, reason code,
   audit trail, and where configured, approval workflow.
7. Tenant placement is catalog configuration, not application code.
8. Pooled and dedicated tenants must use the same application code path.
9. Entitlements and feature flags control module availability in API, UI navigation, jobs,
   events, reports, and integrations.
10. Feature disablement must not delete data; it only blocks access and execution.
11. Tenant suspension blocks tenant user access while preserving platform-owner recovery,
    export, and audit access.
12. Tenant offboarding follows ADR-022 retention, legal hold, export, purge, and evidence
    requirements.
13. Tenant-provider configuration stores only references to secrets, never raw secrets.
14. Cache keys, search indexes, object storage paths, events, telemetry, and audit records
    must be tenant-namespaced.
15. Cross-tenant operations require explicit platform-owner workflow and cannot be available
    through normal tenant-user APIs.

---

# 6. Workflows

## 6.1 Tenant Provisioning

1. Platform Owner starts tenant provisioning.
2. System validates tenant code, legal name, primary country, region, plan, placement,
   default locale, default currency, and admin contact.
3. System creates catalog record in Draft or Provisioning state.
4. System allocates shard/placement and stores secret references.
5. System applies default entitlements and feature flags.
6. System creates tenant configuration version.
7. System emits provisioning event and audit record.
8. Tenant becomes Active only after database, identity, and initial admin setup checks pass.

## 6.2 Tenant Context Resolution

1. Request arrives through approved ingress.
2. Authentication validates issuer, audience, signature, expiry, and claims.
3. Tenant resolver maps token and/or approved host/domain to tenant.
4. Resolver verifies user membership and tenant status.
5. Catalog resolver loads region, shard, entitlements, provider config, and branding
   references.
6. Connection factory opens the resolved database and sets SQL session context.
7. EF query filters and SQL RLS enforce tenant isolation for data access.

## 6.3 Suspension and Activation

1. Platform Owner selects tenant and action.
2. System requires reason, effective time, and approval where configured.
3. Suspension blocks tenant-user access, scheduled jobs, integrations, and tenant-scoped
   background processing.
4. Platform-owner maintenance access remains audited and limited.
5. Activation requires validation that tenant status, identity, placement, and required
   dependencies are healthy.

## 6.4 Placement Change

1. Platform Owner requests placement change, such as pooled to dedicated database.
2. System validates risk, region, data residency, capacity, maintenance window, and rollback.
3. Catalog is updated only after migration evidence is complete.
4. Requests route to the new placement through catalog resolution.
5. No application code change is allowed for placement change.

## 6.5 Offboarding

1. Platform Owner starts offboarding workflow.
2. System verifies contractual authorization, legal hold, export request, and retention rules.
3. Tenant access is blocked according to policy.
4. Export is produced where permitted.
5. Purge is scheduled according to ADR-022.
6. Audit evidence remains according to retention policy.

---

# 7. UI Requirements

Required UI surfaces are defined in `UI-TENANT-001-screens.md`:

- Platform Tenant Registry.
- Tenant Provisioning Wizard.
- Tenant Detail and Administration.
- Entitlements and Feature Flags.
- Placement, Region, and Shard view.
- Suspension, Activation, and Offboarding workflows.
- Tenant Isolation Evidence panel.

UI must be permission-gated. Dangerous actions require confirmation, reason, audit, and
where configured, approval workflow.

---

# 8. API Requirements

APIs must follow approved API standards and be documented in OpenAPI before implementation.

Required API groups:

- Tenant registry and detail.
- Tenant provisioning.
- Tenant lifecycle: activate, suspend, offboard.
- Tenant entitlements and feature flags.
- Tenant branding/domain references.
- Tenant placement and shard metadata.
- Tenant isolation evidence.

Rules:

- Tenant management APIs are platform-owner-only unless explicitly tenant-admin scoped.
- Tenant user APIs may read only their own resolved tenant metadata.
- Normal tenant users cannot select arbitrary tenant IDs.
- Every endpoint must enforce RBAC, ABAC, audit, idempotency where mutating, and
  tenant-aware rate limiting.

---

# 9. Database Requirements

The approved database design is `DB-DESIGN-TENANT-001.md`.

Implementation must provide:

- `catalog` schema for tenant control-plane metadata.
- RLS security schema and predicate function.
- RLS filter predicates for reads.
- RLS block predicates for writes.
- Tenant indexes on every tenant-scoped table.
- Tenant-aware migration conventions.
- Audit logging for catalog and lifecycle changes.
- No raw connection strings or secrets in catalog tables.

Every future module database design must explicitly state how it inherits Tenant Catalog
and RLS controls.

---

# 10. Security Requirements

- Apply zero-trust assumptions: every request must be authenticated and authorized for the
  tenant, even when the host/domain appears tenant-specific.
- Prevent broken object-level authorization by checking object ownership and tenant
  membership for every resource ID.
- Use the repository-injected tenant predicate and SQL Server RLS together (ADR-037).
- Use both RLS filter and block predicates.
- Set SQL session context before the first query on every tenant-scoped connection.
- Disable or tightly review APIs that bypass the repository predicate.
- Protect catalog mutation endpoints with elevated platform permissions.
- Audit tenant lifecycle, placement, entitlement, provider, branding, and domain changes.
- Monitor suspicious RLS policy changes and tenant mapping anomalies.

---

# 11. Non-Functional Requirements

| Area | Requirement |
|---|---|
| Isolation | Zero tolerated cross-tenant leakage in tests and production monitoring. |
| Tenant resolution | Warm-cache tenant resolution target: under 5 ms at application layer. |
| RLS overhead | Measured in S1; indexes must keep overhead within approved budget. |
| Scale | Supports thousands of pooled tenants and dedicated tenants for premium/regulatory use. |
| Availability | Catalog cache must degrade safely; stale unsafe tenant state must fail closed. |
| Audit | Tenant lifecycle and catalog changes are immutable and queryable. |
| Extensibility | Future modules consume tenant context and entitlements without custom code forks. |
| Operability | Placement, suspension, and entitlement changes require no deployment. |

---

# 12. Dependencies

- Approved: ADR-005 Multi-Tenancy Model.
- Approved: ADR-006 Tenant Context and Data Access.
- Approved: DB-DESIGN-TENANT-001.
- Approved: SEC-DESIGN-001 Threat Model.
- Approved: API-SPEC-001 foundational API package.
- Required companion docs before implementation:
  - TECH-TENANT-001
  - UI-TENANT-001
  - TEST-TENANT-001

---

# 13. Acceptance Criteria

| ID | Criterion |
|---|---|
| FEAT-TENANT-AC-001 | Every tenant-scoped table has `TenantId`, tenant index, audit columns, and active RLS policy. |
| FEAT-TENANT-AC-002 | Query code that omits tenant filtering still cannot return another tenant's rows because RLS blocks it. |
| FEAT-TENANT-AC-003 | Write attempts with mismatched `TenantId` are blocked by RLS block predicates. |
| FEAT-TENANT-AC-004 | Client-supplied tenant ID is ignored unless it matches a validated, authorized tenant context. |
| FEAT-TENANT-AC-005 | Suspended tenants cannot access tenant-user APIs, jobs, reports, integrations, or AI paths. |
| FEAT-TENANT-AC-006 | Tenant placement can be changed through catalog configuration without application code change. |
| FEAT-TENANT-AC-007 | Feature flags hide UI navigation and block API execution for disabled modules. |
| FEAT-TENANT-AC-008 | Tenant lifecycle actions require elevated role, reason code, and audit trail. |
| FEAT-TENANT-AC-009 | Tenant-provider configuration stores secret references only. |
| FEAT-TENANT-AC-010 | Cache, search, storage, events, telemetry, and audit are tenant-namespaced. |
| FEAT-TENANT-AC-011 | Background jobs run only under explicit audited tenant context. |
| FEAT-TENANT-AC-012 | Offboarding follows export, legal hold, retention, purge, and evidence rules. |
| FEAT-TENANT-AC-013 | Tenant resolution fails closed when token, host mapping, user membership, or tenant status is invalid. |
| FEAT-TENANT-AC-014 | OpenAPI documentation exists for all tenant management APIs before coding. |
| FEAT-TENANT-AC-015 | Automated tests prove zero cross-tenant leakage before any later business module starts implementation. |

---

# 14. Official and Primary References

- Microsoft SQL Server Row-Level Security:
  `https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security`
- Microsoft SQL Server `SESSION_CONTEXT`:
  `https://learn.microsoft.com/en-us/sql/t-sql/functions/session-context-transact-sql`
- Microsoft SQL Server `sp_set_session_context`:
  `https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-set-session-context-transact-sql`
- Microsoft EF Core Global Query Filters:
  `https://learn.microsoft.com/en-us/ef/core/querying/filters`
- Microsoft Azure Architecture Center - tenancy models:
  `https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models`
- Microsoft Azure Architecture Center - map requests to tenants:
  `https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/map-requests`
- OWASP API1:2023 Broken Object Level Authorization:
  `https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/`
- NIST SP 800-207 Zero Trust Architecture:
  `https://csrc.nist.gov/pubs/sp/800/207/final`

References last validated: 2026-06-27.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-27  
Solution Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Security Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Database Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Platform/Operations Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
QA Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27

(Status: Approved - owner approved 2026-06-27)
