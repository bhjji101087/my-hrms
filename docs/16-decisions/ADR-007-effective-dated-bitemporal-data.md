# ADR-007 — Effective-Dated / Bitemporal Data Strategy

Architecture Decision Record

Date: 2026-06-14
Status: Approved (Bhajan Lal, 2026-06-14)

---

# Context

HR data is inherently time-variant: salary revisions, transfers, org changes, and policy
assignments take effect on a date, may be **future-dated**, and sometimes need
**back-dated corrections** — while payroll, audits, and reports must reproduce "what was
true as of date X". Retrofitting time-variance after launch is extremely costly (it
touches every core table and query). See `ARCH-REVIEW-001` §1C, §7.1(#11).

# Decision

Build **effective-dating into the core domain from day one**, with **bitemporal** support
for the entities that need it (employee, org assignment, position, salary/compensation,
policy/grade assignment):

- **Valid time** (`EffectiveFrom`, `EffectiveTo`) = when a fact is true in the real world.
- **Transaction/system time** (`CreatedDate`, plus row versioning) = when we recorded it.
- Changes create a **new versioned row** rather than overwriting; "current" = the row
  whose valid-time window contains today.
- Provide an **"as-of" query** capability (valid-time and, where needed, system-time).
- Use **SQL Server temporal tables** for system-time history where appropriate, combined
  with explicit valid-time columns for business effective-dating.

Not every table is bitemporal — transactional/event tables stay append-only; only
slowly-changing master/assignment data is effective-dated.

# Alternatives Considered

- **Mutable "current value" only** — simplest, but loses history and can't reproduce past
  payroll; rejected (this is exactly how SMB tools fail audits).
- **Audit log only (no valid time)** — captures *who changed what* but not future-dating
  or clean as-of business queries.
- **Full bitemporal everywhere** — maximal correctness but heavy; reserved for entities
  that genuinely need it.

# Consequences

Positive: future-dated changes, back-dated corrections, reproducible payroll/reporting,
strong audit. Negative: more complex queries and writes; developers must always think in
time windows. Risks: query mistakes ignoring effective dates (mitigated: repository
helpers that default to "as-of today"); performance (mitigated: indexes on TenantId +
valid-time).

# Impact

Architecture: a temporal access pattern in the data layer. Database: valid-time columns +
temporal tables on selected master entities. Security: history is immutable. Performance:
time-window indexing. Development: standard "as-of" repository APIs; UI must expose
effective dates on changes.

# Approval

Solution Architect: ____ · Database Architect: ____ · Product Owner: ____
