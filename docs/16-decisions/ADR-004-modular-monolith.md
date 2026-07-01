# ADR-004 — Modular Monolith now, Microservices later

Architecture Decision Record

Date: 2026-06-14
Status: Approved

---

# Context

The platform is large (many modules) and ambitious, but the team is in early stages.
We need low operational complexity now without closing the door on independent scaling
later.

# Decision

Adopt a **Modular Monolith** as the initial architecture style, with strict module
boundaries (schema-per-module, event-driven communication, no cross-module data
reach-in) so individual modules can later be **extracted into microservices** without
rework. Customer customization happens only via configuration, feature flags,
extensions, and plugins — never by modifying core modules.

# Alternatives Considered

- Microservices from day one — high operational/infra complexity, premature for the
  current team size and unproven domain boundaries.
- Traditional layered monolith — risks tangled modules and hard future extraction.

# Consequences

Positive: low ops complexity now, fast iteration, clean boundaries enable future split.
Negative: discipline required to keep boundaries clean. Risks: boundary erosion;
mitigated by event-driven contracts and architecture reviews.

# Impact

Architecture: module boundaries + event bus are mandatory. Database: schema-per-module.
Security: tenant isolation enforced uniformly. Development: communicate via events,
not direct cross-module calls.

# Approval

Solution Architect: Approved · Project Manager: Approved · Product Owner: Approved
