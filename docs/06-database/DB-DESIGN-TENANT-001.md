# Database Design — Tenant Catalog + RLS (FR-015)

Module: Platform / `catalog` schema + RLS
Author: Database Architect (Agent 7)
Created Date: 2026-06-14
Version: 1.1
Status: Approved (Bhajan Lal, 2026-06-18)

> Doc 3 of 5 (Rule 1). Refines DB-DESIGN-001 §1 for the S1 build. Follows
> `DATABASE_STANDARDS.md`; ratifies ADR-005/006.

---

# Purpose

Define the **control-plane catalog** (tenant definitions/placement/entitlements) and the
**RLS enforcement** applied to every tenant-scoped table.

# Catalog schema (control DB — NOT tenant-scoped; it *defines* tenants)

```
catalog.Tenant
  TenantId(PK, uniqueidentifier), Code(unique), Name,
  Status(Active/Suspended/Offboarding), Region, ShardId(FK), PlacementType(Pooled/Dedicated),
  Plan, CreatedDate, ...
catalog.TenantShard
  ShardId(PK), Region, ConnectionRef(KeyVault secret name — NOT raw), Capacity, TenantCount
catalog.TenantBranding
  TenantId(FK), LogoUrl, ThemeJson, CustomDomain, EmailFromDomain, DkimVerified
catalog.TenantFeatureFlag
  TenantId(FK), FeatureKey, Enabled(bit), EntitlementJson      -- module/feature gating
catalog.TenantConfigVersion
  TenantId(FK), Environment(Sandbox/Prod), Version, SnapshotRef, PromotedBy, PromotedDate
catalog.ProviderType
  ProviderTypeId(PK), [Key](Storage/Cache/Messaging/Email/SMS/Push/Identity/Search/Reporting/LLM), Description
catalog.Provider
  ProviderId(PK), ProviderTypeId(FK), [Key], DisplayName, CapabilitiesJson, Status
catalog.TenantProviderConfig
  TenantProviderConfigId(PK), TenantId(FK), ProviderTypeId(FK), ProviderId(FK),
  ConfigJson, SecretRef(KeyVault), IsPrimary(bit), FallbackProviderId(NULL),
  Enabled(bit), EffectiveFrom, + audit
catalog.ProviderHealth
  ProviderHealthId(PK), TenantId(FK), ProviderTypeId(FK), ProviderId(FK),
  Status(Healthy/Degraded/Down), LatencyMs, LastCheckedAt, LastError
```

# RLS enforcement (applied to ALL tenant-scoped schemas)

```sql
-- predicate function
CREATE FUNCTION security.fn_tenant_predicate(@TenantId uniqueidentifier)
RETURNS TABLE WITH SCHEMABINDING AS
RETURN SELECT 1 AS ok
WHERE @TenantId = CAST(SESSION_CONTEXT(N'TenantId') AS uniqueidentifier);

-- applied per table
CREATE SECURITY POLICY security.TenantIsolation
  ADD FILTER PREDICATE security.fn_tenant_predicate(TenantId) ON <schema>.<table>,
  ADD BLOCK PREDICATE  security.fn_tenant_predicate(TenantId) ON <schema>.<table>
  WITH (STATE = ON);
```
- **FILTER** hides other tenants' rows on read; **BLOCK** prevents writing rows for the wrong tenant.
- `SESSION_CONTEXT('TenantId')` is set by the connection factory (TECH-TENANT-001 §1).

# Relationships & Indexes

- Tenant 1—* TenantFeatureFlag / TenantBranding / TenantConfigVersion /
  TenantProviderConfig / ProviderHealth; Shard 1—* Tenant.
- Catalog indexed on `Code`, `Status`, `ShardId`, `(TenantId, ProviderTypeId)`.
  Every tenant-scoped table indexed on `TenantId` (mandatory).

Branch / Office Hierarchy is defined in `DB-DESIGN-BRANCH-001`. It extends tenant setup
without creating child tenants and must remain protected by TenantId/RLS.

# Integrity & Security

- Catalog mutations restricted to platform-owner role; audited.
- Provider config is admin-only, test-connection validated before activation, and secrets
  are stored only as Key Vault references.
- Connection strings only as Key Vault references; never stored raw.
- Soft delete on catalog rows; offboarding triggers export + purge (ADR-022).

# Performance

RLS adds a predicate to every query — keep `TenantId` first in composite indexes; benchmark
in S1. Catalog reads cached (Redis) with invalidation.

---

## Approval

Database Architect: Approved · Solution Architect: Approved · Security Architect: Approved ·
Product Owner: Approved (Bhajan Lal, 2026-06-18)

## Phase 7A Branch / Office Amendment

Approved 2026-06-29: Tenant Catalog + RLS includes explicit Branch / Office Hierarchy and
Scoped Administration through the approved `BRANCH-001` five-document pack.
