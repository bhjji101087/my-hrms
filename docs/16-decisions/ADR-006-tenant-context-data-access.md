# ADR-006 — Tenant Context & Data-Access Pattern

Architecture Decision Record

Date: 2026-06-14
Status: Approved (Bhajan Lal, 2026-06-18)

---

# Context

ADR-005 chose a hybrid pooled multi-tenant model with RLS and a tenant catalog. We must
define **how every request establishes tenant context and how code accesses data** so that
isolation is enforced uniformly and a developer cannot accidentally bypass it. See
`ARCH-REVIEW-001` §4 and `SEC-DESIGN-001` §4.

# Decision

A single, mandatory **tenant-context pipeline**:

1. **Resolve tenant** early in the request pipeline from the validated JWT (and/or host
   for white-label domains) → an `ITenantContext` (TenantId, region, shard, entitlements).
   The client never supplies a trusted TenantId.
2. **Resolve the shard/connection** from the catalog map (ADR-005); open the connection
   and set **`SESSION_CONTEXT('TenantId')`** so SQL Server **RLS** filters at the DB.
3. **EF Core global query filter** on `TenantId` for all tenant-scoped entities (app-layer
   belt to the DB-layer suspenders).
4. **Repository / Unit-of-Work** layer is the only data path; it injects `TenantId` on
   writes and forbids raw cross-tenant queries. Effective-dated entities default to
   "as-of today" (ADR-007).
5. **Fail closed:** no tenant context ⇒ request rejected; background/system jobs run under
   an explicit, audited system context per tenant.

# Alternatives Considered

- **App-layer filter only (no RLS)** — one missing `.Where(TenantId)` leaks data. Rejected.
- **RLS only (no app filter)** — works but loses early failure + clear app semantics.
- **Manual TenantId on each query** — error-prone, unenforceable. Rejected.

# Consequences

Positive: uniform, enforceable isolation; developers can't easily bypass; residency/shard
move is configuration. Negative: pipeline + session-context plumbing; RLS overhead. Risks:
forgetting to set session context on a raw connection (mitigated: centralized connection
factory + tests).

# Impact

Architecture: middleware + connection factory + repository base. Database: RLS predicates
using SESSION_CONTEXT. Security: defense-in-depth isolation. Development: all access via
repositories; cross-tenant operations require an explicit, audited admin path.

# Approval

Solution Architect: Approved · Security Architect: Approved · Database Architect: Approved ·
Product Owner: Approved (Bhajan Lal, 2026-06-18)
