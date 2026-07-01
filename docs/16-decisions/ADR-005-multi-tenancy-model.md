# ADR-005 — Multi-Tenancy Model

Architecture Decision Record

Date: 2026-06-14
Status: Approved (Bhajan Lal, 2026-06-14)

---

# Context

The platform targets 50–2,000-employee Indian companies, scaling toward thousands of
tenants and future multi-country (UAE/USA/UK) with **data residency** needs. We must
choose a tenant data-isolation model that is secure, cost-efficient at density, supports
per-tenant restore and residency, and does not require a rewrite as we grow from 100 →
10,000 tenants. See `ARCH-REVIEW-001` §4.

# Decision

Adopt a **hybrid pooled model with a tenant catalog**:

1. **Default:** shared database, shared schema, `TenantId` on every table, enforced by an
   **EF Core global query filter** *and* **SQL Server Row-Level Security (RLS)** as
   defense-in-depth (a missing code filter must still be blocked at the DB).
2. **Sharding by pools:** many tenants per DB, multiple DBs (shards). A **catalog DB** maps
   `Tenant → shard / region / entitlements`; the connection is resolved per request.
3. **Tiered placement:** premium / regulated / residency-bound tenants are placed in a
   **dedicated database** (or region) — a *configuration* change in the catalog, not a
   code change.

All data access flows through a single **tenant-context resolver**; the client never
supplies a trusted `TenantId`.

# Alternatives Considered

- **Shared schema only (TenantId)** — cheapest, best density, but logical isolation only,
  noisy-neighbour risk, hard per-tenant restore/residency. Rejected as the *sole* model.
- **Schema-per-tenant** — medium isolation, schema-migration pain at thousands of tenants.
- **Database-per-tenant for everyone** — strongest isolation but poor density/cost and
  high ops overhead at 10,000 tenants. Reserved for the premium/residency tier only.

# Consequences

Positive: cost-efficient at scale, strong isolation via RLS, residency-ready, per-tenant
restore for dedicated tier, single code path. Negative: catalog + shard-routing complexity
up front; RLS adds query overhead. Risks: tenant-context leakage (mitigated: fail-closed
resolver + RLS + tests); shard rebalancing (mitigated: catalog indirection from day one).

# Impact

Architecture: tenant resolver + catalog + shard map are core infrastructure. Database:
`TenantId` + RLS on every table; catalog DB. Security: belt-and-suspenders isolation.
Performance: per-tenant quotas, namespaced caches, per-tenant search indices. Development:
all repositories go through the tenant context; no raw cross-tenant queries.

# Approval

Solution Architect: ____ · Security Architect: ____ · Database Architect: ____
