# ADR-037 — Data Access with Dapper + DbUp (supersedes the EF Core mechanism)

Architecture Decision Record

Date: 2026-07-09

Status: Proposed

Supersedes: the **EF-Core-specific mechanism** in ADR-006 §3 and ADR-005 §1 (tenant query
filter), and the "EF Core Migrations Only" clause in ADR-003, ADR-002, and DATABASE_STANDARDS.
Retains: every ADR-006 / ADR-005 / SEC-DESIGN-001 **outcome** (tenant isolation, RLS,
session context, repository/UoW, soft delete, audit, effective dating, fail-closed).

---

# Context

Earlier ADRs named **EF Core** for two specific jobs: the tenant global **query filter**
(ADR-006 §3, ADR-005 §1) and schema **migrations** ("EF Core Migrations Only" — ADR-003,
ADR-002, DATABASE_STANDARDS). The runtime data-access *pattern* they mandate, however, is
ORM-agnostic: a **Repository / Unit-of-Work** seam (ADR-006 §4) plus **SQL Server Row-Level
Security via `SESSION_CONTEXT`** as the database-level enforcement (ADR-006 §2, TECH-TENANT-001
§8, SEC-DESIGN-001 §4).

The owner has decided to standardize the platform on **Dapper** (a micro-ORM) rather than EF
Core, implemented once as a shared **data-access kernel** every module uses. The motivations:
explicit, predictable SQL and performance on read paths; a small, auditable data layer; and
avoiding EF's change-tracking/model-building machinery. No business modules, repositories, or
queries exist yet, and EF Core currently touches only a single scaffold file (the US #7
`ModuleDbContext`, never merged), so the switch is low-cost now and expensive later.

The hard requirement carried over from ADR-006: it **explicitly rejected** "manual `TenantId`
on each query" as *"error-prone, unenforceable."* SEC-DESIGN-001 §4.6 requires a test proving
*"a deliberately-unfiltered query must return zero rows."* Any Dapper design must therefore
enforce the tenant predicate **without per-query developer discretion**, and keep RLS as the
real backstop.

---

# Decision

Adopt **Dapper** as the platform's data-access technology and **DbUp** for schema migrations,
implemented as a one-time **data-access kernel** in a new foundation project
`HRMS.Platform.Data`. Specifically:

1. **Central predicate injection, not manual filtering.** A `RepositoryBase<TEntity,TId>` +
   `ISqlBuilder` are the **only** sanctioned way to build tenant-scoped SQL. The base always
   emits the mandatory predicates — `TenantId = @__tenantId` (bound from `ITenantContext`,
   never a caller parameter), `IsDeleted = 0`, and (for `IEffectiveDated`) the as-of predicate.
   A developer cannot obtain a tenant-scoped query without them. This is the enforceable
   replacement for the EF global query filter, and it directly answers ADR-006's rejected
   "manual TenantId" alternative.

2. **SQL Server RLS via `SESSION_CONTEXT('TenantId')` is retained unchanged** as the
   database-level hard stop (ADR-006 §2, TECH-TENANT-001 §8). The connection factory sets the
   session context on **every** opened connection before the first query (pooling reuses
   physical connections). Even a bug that bypassed the app filter returns zero cross-tenant
   rows. RLS is the load-bearing control; the app-level predicate provides early failure and
   clear semantics (exactly why ADR-006 rejected "RLS only").

3. **Fail closed.** No resolved `ITenantContext` ⇒ tenant-scoped data access is rejected at the
   connection factory. Background/system jobs run under an explicit, audited system-tenant scope.

4. **Repository / Unit of Work** (ADR-006 §4) is realized by `IDbSession` (one connection +
   ambient transaction per request scope; the single Dapper entry point) and repository bases.

5. **Migrations use DbUp** — plain, versioned, forward-only SQL scripts run by a migration
   runner (replaces EF Core Migrations). The RLS predicate function and security policy, audit
   schema, and per-module schemas/tables are all created by these scripts.

6. **Explicit, parameterized, schema-qualified SQL** — the builder emits explicit columns
   (never `SELECT *`), schema-qualified table names (schema-per-module, ADR-004), and only
   `@parameters` for values (no dynamic SQL; satisfies parameterized-queries-only and CA2100).

7. **Audit and effective dating** are generic kernel services: an audit interceptor captures
   old→new per write (append-only, hash-chained, atomic with the business transaction), and an
   `EffectiveDatedRepositoryBase` provides as-of/history/supersede with valid-time columns and
   SQL Server temporal tables for system-time history.

8. **Boundary enforcement.** Only `HRMS.Platform.Data` may reference Dapper /
   `Microsoft.Data.SqlClient`; a NetArchTest fails the build if any other project does, and if
   any project references EF Core. This makes "the repository base is the only way to build SQL"
   structurally true.

---

# Alternatives Considered

- **Keep EF Core (default) + Dapper for hot paths** — least doc churn; EF's global filter,
  change tracking, migrations, and audit interceptors are mature. Rejected by owner preference
  for an explicit, uniform Dapper layer; retained here only as the fallback if the kernel proves
  costlier than expected.
- **Naive Dapper (developers hand-write `WHERE TenantId`)** — rejected: this is exactly the
  "manual TenantId per query" alternative ADR-006 already rejected as unenforceable.
- **App-level filter only, drop RLS** — rejected: one kernel bug or raw-query bypass leaks data;
  contradicts SEC-DESIGN-001 defense-in-depth.
- **Keep EF Core solely for migrations** — viable, but keeping an EF dependency and DbContext
  model just for migrations adds tooling overlap; DbUp is simpler for a Dapper stack.

---

# Consequences

Positive: explicit predictable SQL; small auditable data layer; central, non-bypassable tenant
/ soft-delete / effective-date enforcement; RLS retained; performance headroom on reads.

Negative: the platform hand-builds SQL generation, mapping, migrations, and audit that EF
provides out of the box — more foundation code to write and test. Loses EF conveniences
(navigation loading, automatic change tracking, LINQ). Mitigated by concentrating all of it in
one well-tested kernel.

Risks: (a) the "unenforceable manual filter" failure mode — mitigated by central injection +
no bypass API + RLS + tests; (b) missed session context on a pooled connection — mitigated by
setting it on every `OpenAsync` + an integration test + RLS failing safe; (c) raw-SQL analyzer
violations under warnings-as-errors — mitigated by identifiers-from-metadata-only and
values-via-parameters-only.

---

# Impact

Architecture: new `HRMS.Platform.Data` kernel; modules depend on it, not on an ORM.
Database: unchanged schema strategy (schema-per-module, mandatory columns, RLS); migrations via
DbUp scripts instead of EF migrations. Security: tenant isolation via central predicate + RLS;
parameterized queries only. Performance: explicit column selects; Dapper materialization.
Development: all data access through repository bases; no raw Dapper strings outside the kernel.
Rollback / Migration: EF Core removed from `src/` before any module ships; no data migration
needed (no data exists yet).

---

# Security Impact

RBAC / ABAC impact: none directly; authorization stays in the identity/module layers.
Tenant isolation impact: mechanism changes from EF global filter to repository-injected predicate
**plus retained RLS**; the security guarantee (SEC-DESIGN-001 §4.6 "unfiltered query returns
zero rows") is unchanged because it is enforced by RLS regardless of ORM.
Audit impact: audit becomes a kernel interceptor (append-only, hash-chained, atomic).
Sensitive data / PII impact: audit masks by classification; secrets never stored.
Threat model updates required: SEC-DESIGN-001 §2/§4 wording updated to "enforced app-layer
tenant predicate (repository-injected)"; the RLS layer and CI zero-rows test are unchanged.

---

# Rollback and Operational Plan

Rollback approach: if the Dapper kernel proves unworkable before modules ship, revert to the
"EF Core default + Dapper hot paths" fallback; only foundation code and this ADR are affected.
Compensating action: none required at runtime (no data yet).
Monitoring and alerts: tenant-mismatch denials, RLS-blocked writes, fail-closed rejections
(per TECH-TENANT-001 §15) surface from the kernel.
Runbook impact: migration runbook changes from EF migrations to DbUp script deployment.
Post-decision validation: the FR-DATA integration test proves RLS blocks cross-tenant reads and
that a deliberately-unfiltered query returns zero rows.

---

# Approval

Solution Architect: ____ · Database Architect: ____ · Security Architect: ____ ·
Project Manager: ____ · Product Owner: ____

(Status: Proposed → Approved by the human owner. No FR-DATA kernel code may start until this
ADR and the companion documentation amendments are Approved — Golden Rule 1.)
