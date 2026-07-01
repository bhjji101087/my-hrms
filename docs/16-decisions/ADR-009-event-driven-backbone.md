# ADR-009 — Event-Driven Backbone

Architecture Decision Record

Date: 2026-06-14
Status: Approved (Bhajan Lal, 2026-06-18)

---

# Context

`ARCHITECTURE_PRINCIPLES.md` mandates event-driven communication between modules
(AttendanceApproved → Payroll → Notifications → Reports). In a modular monolith (ADR-004)
that must later extract services, modules must communicate via events, not direct calls.
We need reliable, ordered, exactly-once-effect delivery without distributed transactions.
See `ARCH-REVIEW-001` §6, §7.1(#4,#5,#12).

# Decision

1. **Broker:** **Azure Service Bus** in cloud (managed, ordering via sessions, DLQ,
   topics/subscriptions); **RabbitMQ** as the portable/self-host option. Abstract behind a
   `IMessageBus` interface so the choice is swappable.
2. **Transactional Outbox pattern:** domain changes and their events are written in the
   **same DB transaction** (outbox table); a dispatcher publishes asynchronously. This
   removes the dual-write problem — no 2PC.
3. **Idempotent consumers:** every consumer dedupes on a message/idempotency key
   (ARCH-REVIEW §7.1#12) so redelivery is safe.
4. **Versioned event contracts** with a schema registry; events are additive/backward-
   compatible; consumers tolerate unknown fields.
5. **In-process now, out-of-process later:** within the monolith, events flow through the
   bus abstraction (could be in-memory + outbox). When a module is extracted, the same
   contracts move to the broker with no consumer rewrite.
6. **DLQ + retry with back-pressure**; per-tenant fairness so one tenant can't starve the
   bus.

# Alternatives Considered

- **Direct synchronous calls between modules** — tight coupling, cascading failures,
  blocks future extraction. Rejected.
- **Dual-write (DB then publish, no outbox)** — loses events on crash between steps.
- **Event sourcing as the primary store** — powerful but heavy; not needed for Phase 7A
  (we use events for integration, not as the system of record).

# Consequences

Positive: loose coupling, resilience, future service extraction, audit-friendly. Negative:
eventual consistency to reason about; outbox + dispatcher infrastructure. Risks: ordering/
duplicates (mitigated: sessions + idempotency); backlog (mitigated: autoscale consumers,
DLQ, monitoring).

# Impact

Architecture: outbox table per module schema; dispatcher; bus abstraction. Database:
`Outbox` tables (+ processed markers). Security: events carry TenantId; no PII beyond need.
Performance: async, autoscaled consumers. Development: state changes emit domain events;
consumers must be idempotent.

# Approval

Solution Architect: Approved · .NET Architect: Approved · Security Architect: Approved ·
Product Owner: Approved (Bhajan Lal, 2026-06-18)
