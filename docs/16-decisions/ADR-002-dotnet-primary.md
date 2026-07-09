# ADR-002 — .NET as the primary backend, Node.js for specialized services

Architecture Decision Record

Date: 2026-06-14
Status: Approved

---

# Context

The platform needs a robust, enterprise-grade backend for core business logic
(payroll, compliance, employee lifecycle) plus real-time/connector workloads
(attendance devices, websockets, integration workers, event processing).

# Decision

Use **.NET (latest LTS) as the primary backend** for core business services and APIs.
Use **Node.js for specialized services**: real-time notifications, WebSockets,
attendance device connectors, integration workers, event processing.

# Alternatives Considered

- All-Node backend — weaker for heavy business/compliance logic and typed domains.
- All-.NET including real-time connectors — less ergonomic for some device/websocket
  ecosystems.
- Java/Spring — viable, but team strength and tooling favor .NET.

# Consequences

Positive: strong typing, Clean Architecture/DDD fit, mature ecosystem for the core;
Node where it is genuinely better. Negative: two runtimes to operate and skill.
Risks: integration complexity between runtimes; mitigated by event-driven boundaries.

# Impact

Architecture: clear core (.NET) vs. edge (Node) split. Database: DbUp SQL-script migrations
(see ADR-037). Security: unified JWT/tenant validation across both. Development: two toolchains.

# Approval

Solution Architect: Approved · Project Manager: Approved · Product Owner: Approved
