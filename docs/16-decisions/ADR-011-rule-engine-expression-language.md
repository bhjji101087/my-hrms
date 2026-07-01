# ADR-011 — Rule Engine Model & Expression Language

Architecture Decision Record

Date: 2026-06-14
Status: Approved (Bhajan Lal, 2026-06-14)

---

# Context

Golden Rule 2 forbids hardcoded business rules. Leave eligibility/accrual, payroll
formulas, statutory slabs (PF/ESI/PT/LWF/TDS), workflow routing conditions, and form
validation must all be **data**, evaluated at runtime, versioned, and effective-dated for
statutory change. We must choose a rule model and a safe expression language. See
`ARCH-REVIEW-001` §3.

# Decision

Build a **generic, rules-as-data Business Rule Engine** with a **safe, serializable
expression language**:

- **Canonical form: a JSON-Logic-style AST** — UI-buildable (config-as-data), storable,
  diffable, and safe (no arbitrary code execution). Compiled to cached delegates for speed.
- **Rule model:** `key`, `version`, `effectiveFrom/To`, `priority/salience`, `when`
  (boolean expression), `then` (set value | raise validation error | route | call action).
- **Evaluation strategies:** decision tables (payroll components, tax slabs), sequential
  priority/first-match (validation, routing). Forward-chaining (Rete) is **not** adopted
  now (most HR rules don't need it; revisit only if a use case demands it).
- **Governance:** rulesets immutable on publish; statutory changes create a new
  **effective-dated** version; dry-run simulation against sample data before promotion;
  all changes audited and promoted sandbox→prod.
- A curated, sandboxed **function library** (date math, statutory helpers, lookups) — no
  I/O, time-bounded evaluation.

# Alternatives Considered

- **Arbitrary C# / Roslyn scripting** — maximally flexible but an RCE risk and not
  config-as-data; rejected for tenant-authored rules.
- **NCalc / DynamicExpresso** — usable expression libraries; viable behind a strict
  whitelist, but a JSON AST is more UI-friendly and safer as the canonical form. May be
  used internally as an evaluation backend behind the AST.
- **Full Rete engine (e.g. NRules)** — powerful but heavyweight for predominantly simple,
  ordered HR rules; deferred.

# Consequences

Positive: no hardcoded rules, safe tenant-authored logic, effective-dated statutory
versioning, fast cached evaluation, UI-buildable. Negative: we build/maintain the
evaluator and function library. Risks: expression-language injection/RCE (mitigated:
AST + whitelist + sandbox, no eval); rule-conflict ambiguity (mitigated: explicit
priority + conflict-resolution policy); performance on large decision tables (mitigated:
compile + cache, indexes).

# Impact

Architecture: Rule Engine is a shared platform service (used by Workflow, Payroll, Leave,
Validation, Compliance). Database: `rules` schema (RuleSet, Rule), versioned + effective-
dated. Security: sandboxed evaluation, no dynamic SQL/code. Performance: delegate cache
keyed by (tenant, ruleset, version). Development: domains express logic as rules, not
`if` statements.

# Approval

Solution Architect: ____ · Security Architect: ____ · Database Architect: ____
