# ADR-010 — Workflow Engine: Lean Interpreter vs Library

Architecture Decision Record

Date: 2026-06-14
Status: Approved (Bhajan Lal, 2026-06-14)

---

# Context

Workflow Studio is the platform's core differentiator (PRD FR-007): a no-code engine for
approval chains, conditional routing, SLAs, escalations, and delegation, reused by every
module. It must be **multi-tenant, config-as-data, versioned**, and integrate with our own
Rule Engine (ADR-011) and event bus. We must decide whether to build the engine or adopt a
.NET workflow library. See `ARCH-REVIEW-001` §2.

# Decision

**Build a lean, declarative workflow interpreter** over a versioned JSON
`WorkflowDefinition` model, rather than adopting a third-party engine for the core.

- Definitions are immutable on publish (`version+1` on edit); **running instances pin
  their definition version** (prevents post-update regression — validated pain P5).
- Explicit **state machine** with event-driven transitions; **saga/process-manager**
  pattern for long-running async flows.
- Approval resolution is pluggable (role / hierarchy / ABAC / committee / **delegate**);
  SLA timers via a scalable scheduler (Hangfire/Quartz.NET) emitting escalation events.
- Routing conditions delegate to the **Rule Engine** (ADR-011) — no duplicate logic.
- Append-only event log per instance feeds the Time-Machine audit (FR-008).
- **Migration:** publishing a new version offers drain / migrate (explicit state map) /
  abort; migrating live instances requires approval.

# Alternatives Considered

- **Elsa Workflows (.NET)** — capable accelerator, but imposes its own model/persistence,
  and bending it to our tenant-scoped versioning, Rule-Engine integration, and
  config-as-data needs risks more friction than building lean. Re-evaluate if delivery
  velocity becomes the binding constraint.
- **Windows Workflow Foundation / commercial BPM** — heavyweight, poor fit for embedded
  multi-tenant SaaS.
- **Hardcoded per-module approval logic** — violates Golden Rule 2; rejected outright.

# Consequences

Positive: full control of config-as-data, tenant isolation, versioning, and Rule-Engine
integration; no external model lock-in. Negative: we own engine correctness, migration,
and test burden. Risks: over-engineering (mitigated: start with sequential/parallel
approvals + SLA, defer marketplace/advanced patterns — YAGNI); engine bugs in payroll-
critical flows (mitigated: extensive tests, version pinning).

# Impact

Architecture: Workflow is a first-class platform service. Database: `workflow` schema
(Definition, Instance, Task, EventLog, Timer, Template). Security: actions use an egress
allowlist (anti-SSRF); approvals authorized per tenant. Performance: sharded timers,
partitioned event log. Development: modules consume the engine, never re-implement
approvals.

# Approval

Solution Architect: ____ · Product Owner: ____ · Security Architect: ____
