# Test Plan - Tenant Catalog and Row-Level Security

Feature Name: Tenant Catalog and Isolation
Requirement ID: FR-015
Module: Platform / Core
Owner: QA Architect
Created Date: 2026-06-14
Last Updated: 2026-06-27
Version: 1.1
Status: Approved

> Doc 5 of 5 required before implementation. Companion docs:
> FEAT-TENANT-001, TECH-TENANT-001, DB-DESIGN-TENANT-001, UI-TENANT-001.
> No Tenant Catalog or RLS implementation may start until all five documents are Approved.

---

# 1. Purpose

This test plan proves that Tenant Catalog and RLS enforcement are safe enough to become the
first implementation foundation for the HRMS platform. Tenant isolation is non-negotiable:
any confirmed cross-tenant read, write, cache, search, event, background-job, or UI leak is
a release blocker.

---

# 2. Scope

In scope:

- Tenant resolution.
- Tenant catalog lifecycle.
- Tenant placement and shard routing.
- SQL Server RLS filter predicates.
- SQL Server RLS block predicates.
- EF Core global query filters.
- Tenant-aware write stamping.
- Tenant entitlements and feature flags.
- Tenant suspension, activation, offboarding, and placement change.
- Tenant-aware cache, search, storage, event, telemetry, and provider namespaces.
- Tenant-aware background jobs.
- Tenant administration UI.
- OpenAPI/API contract behavior.
- Audit, security, performance, and degraded-mode behavior.

Out of scope:

- Billing.
- Public self-service signup.
- Business-module-specific rules.
- Full data migration automation for dedicated tenant movement.

---

# 3. Quality Gates

| Gate | Requirement |
|---|---|
| Cross-tenant leakage | Zero tolerated. Any confirmed leak blocks release. |
| Tenant security tests | 100 percent pass required. |
| Unit coverage | At least 85 percent line and branch coverage. |
| Critical isolation coverage | 95 percent coverage for resolver, connection factory, filters, RLS setup, and entitlement enforcement. |
| OpenAPI contract | All tenant APIs match approved OpenAPI before implementation acceptance. |
| RLS coverage | Every tenant-scoped table has active filter and block predicates. |
| Performance | Tenant resolution and RLS overhead meet approved budget. |
| Accessibility | Tenant UI meets WCAG 2.2 AA target. |

---

# 4. Test Environments

Required:

- Local developer environment with deterministic tenant fixtures.
- Integration environment with SQL Server RLS enabled.
- Redis/cache test environment.
- Search/index namespace test double or integration environment.
- Background job test host.
- API contract test environment.
- UI test environment.
- Security/adversarial test environment with Tenant A, Tenant B, and platform-owner users.

RLS tests must run against real SQL Server behavior, not only mocks.

---

# 5. Test Data

Minimum test tenants:

- Tenant A: active pooled tenant.
- Tenant B: active pooled tenant on same shard.
- Tenant C: active dedicated placement tenant.
- Tenant D: suspended tenant.
- Tenant E: offboarding tenant.

Minimum users:

- Platform Owner.
- Platform Operator.
- Security Reviewer.
- Tenant A Admin.
- Tenant B Admin.
- Tenant A Employee.
- Tenant B Employee.
- Multi-tenant user with membership in two tenants.
- Unauthorized user.

Minimum data:

- Same logical entity IDs across tenants where possible.
- Distinct tenant feature flags.
- Distinct branding/domain mappings.
- Distinct cache/search/storage namespaces.
- Background jobs queued for multiple tenants.

---

# 6. Unit Test Scenarios

Tenant resolver:

- `ResolveTenant_ValidTokenTenant_ReturnsTenantContext`
- `ResolveTenant_CustomDomainWithoutMembership_FailsClosed`
- `ResolveTenant_ClientBodyTenantId_Ignored`
- `ResolveTenant_MultipleMembershipWithoutSelection_ReturnsAmbiguous`
- `ResolveTenant_SuspendedTenant_ReturnsAccessDenied`
- `ResolveTenant_UnknownTenant_ReturnsNotFoundOrForbidden`

Entitlements:

- `Entitlement_DisabledModule_BlocksApiAndNavigation`
- `Entitlement_BetaModule_VisibleOnlyWhenEnabled`
- `Entitlement_UserPermissionMissing_RemainsForbidden`

Connection and context:

- `ConnectionFactory_OpenTenantConnection_SetsSessionContext`
- `ConnectionFactory_PooledConnection_ReappliesTenantContext`
- `ConnectionFactory_MissingTenantContext_FailsClosed`
- `SaveChanges_MismatchedTenantId_BlockedBeforeDatabase`
- `SaveChanges_NewTenantEntity_StampsTenantId`

---

# 7. Integration Test Scenarios

RLS read isolation:

- `Query_WithoutTenantFilter_RlsReturnsOnlyCurrentTenantRows`
- `Query_RawSqlWithoutWhereClause_RlsReturnsOnlyCurrentTenantRows`
- `Query_JoinAcrossTenantScopedTables_RlsBlocksOtherTenantRows`
- `Query_TenantHistoryTable_RlsAppliesToHistoryRows`

RLS write isolation:

- `Insert_MismatchedTenantId_BlockPredicateRejects`
- `Update_RowToDifferentTenant_BlockPredicateRejects`
- `Delete_OtherTenantRow_FilterPredicatePreventsAccess`
- `BulkInsert_MismatchedTenantId_RejectedOrQuarantined`

EF filters:

- `EfQuery_DefaultQuery_AppliesTenantAndSoftDeleteFilters`
- `EfQuery_RequiredNavigation_DoesNotBypassTenantIsolation`
- `EfQuery_IgnoreQueryFilters_NotAllowedInProductRepository`

Catalog:

- `ProvisionTenant_CreatesCatalogPlacementEntitlementsAndAudit`
- `ActivateTenant_RequiresDependencyChecks`
- `SuspendTenant_BlocksTenantUserAccess`
- `OffboardTenant_RequiresExportRetentionLegalHoldChecks`
- `ChangePlacement_UpdatesCatalogRoutingWithoutCodeChange`

---

# 8. Security and Adversarial Tests

Required tests:

- Manipulate tenant ID in request body.
- Manipulate tenant ID in query string.
- Manipulate custom tenant header.
- Use valid Tenant A token against Tenant B URL/domain.
- Use valid platform API endpoint with unauthorized user.
- Attempt object-level access by changing resource IDs.
- Attempt platform-owner lifecycle action as tenant admin.
- Attempt cache key collision.
- Attempt search namespace collision.
- Attempt blob/object storage path traversal into another tenant namespace.
- Attempt background job execution without tenant context.
- Attempt SQL query before session context is set.
- Attempt RLS policy disablement in migration or runtime.

All high and critical security findings block release.

---

# 9. API Contract Tests

Required:

- Tenant registry response envelope.
- Tenant detail authorization.
- Provision tenant request validation.
- Suspend/activate/offboard idempotency.
- Entitlement update validation.
- Placement change validation.
- Error response codes:
  - 401 missing authentication.
  - 403 unauthorized tenant or role.
  - 404 unknown tenant where policy hides existence.
  - 409 ambiguous tenant or lifecycle conflict.
  - 422 validation failure.
- Audit/correlation headers where approved.
- OpenAPI conformance.

---

# 10. UI and Accessibility Tests

Required Playwright or equivalent tests:

- Platform Tenant Registry list, filter, and search.
- Provisioning wizard happy path and validation errors.
- Tenant detail platform-owner view.
- Tenant detail tenant-admin restricted view.
- Entitlement toggle impact preview.
- Placement change disabled until evidence exists.
- Suspension workflow with reason and confirmation.
- Offboarding workflow with legal-hold and retention messaging.
- Isolation Evidence screen read-only behavior.
- Suspended tenant user blocked-access state.
- Keyboard-only operation.
- Screen-reader labels for statuses and dangerous actions.
- Responsive layout checks.
- Text overflow checks.

---

# 11. Background Job Tests

Required:

- `BackgroundJob_PerTenantExecution_SetsTenantContext`
- `BackgroundJob_MultipleTenants_SeparatesAuditAndCorrelation`
- `BackgroundJob_SuspendedTenant_SkippedUnlessMaintenanceAllowed`
- `BackgroundJob_TenantFailure_DoesNotLeakOrStopUnrelatedTenant`
- `BackgroundJob_CacheNamespace_IncludesTenant`
- `BackgroundJob_EventEmission_IncludesTenantContext`

---

# 12. Performance Tests

Required:

- Tenant resolution warm-cache latency.
- Tenant resolution cold-cache latency.
- Catalog lookup under thousands of tenants.
- RLS overhead benchmark versus non-RLS baseline.
- Query performance with `TenantId` leading indexes.
- Connection open plus `sp_set_session_context` overhead.
- Entitlement evaluation latency.
- Tenant registry search/filter performance.
- Suspended tenant denial under load.

Performance must be measured before accepting implementation. Security is not traded away
to improve speed; performance fixes must preserve isolation.

---

# 13. Degraded-Mode Tests

Required:

- Catalog DB unavailable with no cache: fail closed.
- Catalog DB unavailable with safe active cache: allowed read-only behavior if policy
  permits.
- Redis unavailable: catalog DB fallback works.
- Session context setup failure: data access blocked.
- RLS policy missing: deployment health fails.
- Tenant placement unavailable: only affected tenant fails where placement isolation
  allows it.
- Suspended status cache invalidation delayed: system does not allow unsafe access.

---

# 14. Migration and Schema Tests

Required:

- Every tenant-scoped table has `TenantId`.
- Every tenant-scoped table has RLS filter predicate.
- Every tenant-scoped table has RLS block predicate.
- Every tenant-scoped table has tenant index.
- RLS applies to temporal/history tables where used.
- Migrations cannot introduce tenant-scoped tables without RLS.
- RLS predicate function avoids implicit conversions and excessive joins.
- Catalog tables do not store raw secrets.

---

# 15. Test Automation

Automation layers:

- Unit tests: resolver, entitlement, connection factory, write stamping.
- Integration tests: SQL Server RLS, EF filters, catalog lifecycle.
- API tests: OpenAPI contract, authz, validation, idempotency.
- UI tests: Playwright for tenant administration.
- Security tests: tenant tampering and BOLA scenarios.
- Performance tests: RLS, resolver, catalog, and connection overhead.
- Migration tests: schema/RLS policy coverage.

CI must fail if tenant isolation tests fail.

---

# 16. Exit Criteria

Tenant Catalog + RLS implementation cannot be accepted until:

- All FEAT, TECH, DB, UI, and TEST acceptance criteria pass.
- Zero cross-tenant leakage is proven in automated tests.
- RLS filter and block predicates cover every tenant-scoped table.
- API contract tests pass.
- Security tests pass with zero critical/high unresolved findings.
- Performance benchmarks are recorded and approved.
- Accessibility checks pass for tenant UI.
- Product Owner, Security, Database, Solution Architecture, and QA sign-off is complete.

## Phase 7A Branch / Office Addendum

Tenant testing must include `docs/10-testing/TEST-BRANCH-001-test-plan.md`. Complete
tenant admin access and branch admin restricted access are release-blocking security
tests.

---

# 17. Official and Primary References

- Microsoft SQL Server Row-Level Security:
  `https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security`
- Microsoft SQL Server `SESSION_CONTEXT`:
  `https://learn.microsoft.com/en-us/sql/t-sql/functions/session-context-transact-sql`
- Microsoft SQL Server `sp_set_session_context`:
  `https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-set-session-context-transact-sql`
- Microsoft EF Core Global Query Filters:
  `https://learn.microsoft.com/en-us/ef/core/querying/filters`
- Microsoft Azure Architecture Center - tenant request mapping:
  `https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/map-requests`
- OWASP API1:2023 Broken Object Level Authorization:
  `https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/`
- NIST SP 800-207 Zero Trust Architecture:
  `https://csrc.nist.gov/pubs/sp/800/207/final`
- WCAG 2.2:
  `https://www.w3.org/TR/WCAG22/`

References last validated: 2026-06-27.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-27  
QA Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Security Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Solution Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Database Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Platform/Operations Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27

(Status: Approved - owner approved 2026-06-27)
