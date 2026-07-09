# ADR-003 — SQL Server as the primary database

Architecture Decision Record

Date: 2026-06-14
Status: Approved

---

# Context

The HRMS is highly relational (employees, payroll, attendance, leave, compliance)
and must be multi-tenant, auditable, performant, and scalable, with first-class
.NET integration.

# Decision

Use **SQL Server** as the primary relational database. Schema changes are applied via
**versioned SQL-script migrations (DbUp)** only — see ADR-037, which supersedes the earlier
"EF Core migrations only" wording. Redis for caching, Elasticsearch for search, Azure Blob for
storage — each for its specific role, not as a system of record.

# Alternatives Considered

- PostgreSQL — strong and lower-cost, but team/tooling and .NET alignment favor SQL Server.
- MySQL — weaker for complex enterprise reporting/partitioning needs.
- NoSQL primary — poor fit for the highly relational, transactional HR domain.

# Consequences

Positive: mature tooling, strong .NET/Dapper fit, partitioning and indexing maturity.
Negative: licensing cost. Risks: large-table growth; mitigated by indexing, partitioning,
and archival standards in DATABASE_STANDARDS.md.

# Impact

Architecture: relational system of record. Database: schema-per-module, mandatory
TenantId, soft delete, audit. Security: parameterized queries only. Performance:
mandatory TenantId index, explicit column selects.

# Approval

Solution Architect: Approved · Database Architect: Approved · Project Manager: Approved
