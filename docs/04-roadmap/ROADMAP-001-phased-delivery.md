# Delivery Roadmap — Phased Delivery

Document Owner: Project Manager (Agent 5)
Created Date: 2026-06-14
Version: 1.0
Status: Approved

> Sequences the approved PRD (v1.1, FR-001…015) and ARCH-REVIEW-001 §9 MoSCoW into
> phases and sprints. Dates are **relative** (T0 = first development sprint) because
> Phases 3–6 (architecture, DB, UX, API, AI) must complete before build (Golden Rule 1).
> This roadmap is a plan of record, not a commitment date.
>
> **Important:** FR IDs are requirement identifiers, not build order. The build sequence
> is dependency-led. That is why Sprint 1 starts with FR-015 Tenant Catalog + RLS and
> FR-002 Identity before business modules. Leave, Attendance, Payroll, and Compliance
> must not start until the foundation group they depend on is designed and proven.

---

## 1. Guiding Sequencing Principles

1. **Foundations before features.** Tenant Catalog + RLS, Identity + RBAC/ABAC,
   Effective Dating, Audit/Time Machine, Event Bus, Rule Engine, Workflow Engine, and
   Configuration-as-Data gate everything else.
2. **Differentiator early.** Workflow Studio (FR-007) is the moat *and* the biggest risk
   → prototype in the foundation phase, harden through Phase 7A.
3. **Vertical slices.** Each module ships end-to-end (DB → API → UI → tests) behind
   feature flags, not horizontal layers.
4. **Compliance is non-negotiable in Phase 7A.** Payroll + India statutory must be correct at
   launch (validated trust pain).
5. **Everything ships in phases.** No phase may absorb later-phase modules without a
   PRD and roadmap update approved by the owner.
6. **Open for extension, closed for core changes.** Future modules are added through
   module manifests, feature flags, APIs, events, configuration, extensions, plugins,
   and provider adapters.

---

## 2. Pre-Development Gate (Phases 3–6) — must finish first

| Phase | Deliverable | Owner | Status |
|---|---|---|---|
| 3 Architecture | ADR-005/007/010/011 approved; ARCH-REVIEW refresh must align with approved PRD/roadmap | Solution Architect | Refresh pending |
| 3 Architecture | Remaining ADRs 006, 008, 009, 012–026 | Solution Architect | Pending |
| 3 Database | Foundational schema design | Database Architect | In progress |
| 3 Security | Security design / threat model | Security Architect | Pending |
| 4 UX/UI | Design system + key wireframes | UX/UI | Pending |
| 4 UX/UI | **Visual mockups signed off by owner** (figma/ or hi-fi Figma) | UI/Figma Designer | **Gate — required before build** |
| 5 API | OpenAPI specs for Phase 7A modules | .NET Architect | Pending |
| 6 AI | RAG design (for FR-011) | Prompt/Context Eng | Pending |

> **No build starts** until each module's 5 docs (Business, Technical, DB, UI, Test) are
> Approved per Golden Rule 1.

---

## 3. Phase Delivery Plan

```
 Phase 7A        Foundation group first:
                  Tenant Catalog/RLS + Branch/Office Hierarchy
                  + Identity/RBAC/ABAC + Effective Dating
                  + Audit/Time Machine + Event Bus + Rule Engine
                  + Workflow Studio + Configuration-as-Data
                  Then Core HR + Leave + Attendance with Shift Foundation
                  + Payroll/Compliance
                  + standard reports                                  [MUST]
 Phase 7B        White-label, SSO/OIDC, notification preferences,
                  config sandbox->promotion, documents/letters/e-sign,
                  HR service desk, onboarding/offboarding basics,
                  provider health, implementation wizard             [SHOULD]
 Phase 7C        RAG HR Assistant, richer reporting/BI, compliance
                  intelligence, mobile reliability hardening,
                  attendance connector #2-3                          [SHOULD]
 Phase 7D        Recruitment/ATS, advanced onboarding, performance/
                  goals/OKRs, LMS, engagement/surveys/recognition    [NEXT]
 Phase 7E        Advanced roster/workforce scheduling, shift swap,
                  expense/travel/reimbursements, assets/
                  IT requests, compensation review, multi-entity UI   [NEXT]
 Later phases    Workforce planning, integration marketplace,
                  contingent workforce, multi-country payroll plugins,
                  advanced manager intelligence                      [DEFER]
```

---

## 4. Phase 7A Sprint Plan — vertical slices

Assumes 2-week sprints. Sequence reflects dependencies, not a fixed calendar.

| Sprint | Theme | Primary FRs | Exit criteria |
|---|---|---|---|
| S1 | **Platform foundation I** | FR-015 tenant catalog + RLS + branch/office hierarchy, FR-002 identity/JWT + RBAC/ABAC | A request is tenant-resolved; RLS blocks cross-tenant even with a missing code filter; branch admin is restricted to assigned branch scope |
| S2 | **Platform foundation II** | FR-014 effective-dating core, FR-008 audit/time-machine, FR-009 event bus + outbox | As-of query works; every write audited (old→new); an event flows end-to-end |
| S3 | **Rule + Workflow engines (core)** | FR-013 Rule Engine, FR-007 Workflow Studio (prototype), Configuration-as-Data pattern | A data-defined rule evaluates; a 2-level conditional approval runs & is version-pinned; workflow/rule/form metadata is stored as configuration |
| S4 | **Core HR & ESS** | FR-003 employee master, org, branch assignment, ESS | Employee CRUD with effective-dating + audit; branch assignment works as-of date; ESS profile edit via workflow |
| S5 | **Leave (configurable)** | FR-004 leave types/accrual + Workflow approval | Tenant admin creates a leave type + approval chain with no code/deploy |
| S6 | **Attendance + connector + Shift Foundation** | FR-005 web/mobile/manual/CSV + 1 biometric connector + shift definition/assignment | Add-device (vendor→IP→save) with no custom code; punches use effective employee shift and feed payroll |
| S7 | **Payroll engine + components** | FR-006 structures, formula engine (via Rule Engine), payroll run, payslips | Correct sample run; payslip generated; GL/reconciliation stub |
| S8 | **India statutory compliance** | FR-006 PF/ESI/PT/LWF/TDS/Form16 + FBP + mid-cycle CTC | Compliant statutory outputs; FBP + mid-cycle revision with **no manual workaround** |
| S9 | **Workflow Studio hardening** | FR-007 delegation, SLA/escalation, migration | Delegate routing, SLA escalation, live-instance migration plan all work |
| S10 | **Reporting + hardening** | FR-012 standard reports/exports, perf, security, UAT | Core reports; P95 < 2s; security tests pass; ≥85% coverage |

> **Workflow Studio spans S3→S9** (prototype → harden) because it's the differentiator and
> the top schedule risk.

---

## 5. Dependency Graph (ASCII)

```
 FR-015 catalog/RLS + Branch ─┬─► FR-002 identity ─┬─► FR-003 Core HR ─┬─► FR-004 Leave
                              │                    │                   ├─► FR-005 Attendance + Shift ─► FR-006 Payroll/Compliance
 FR-014 effective ───┤                    │                   │
 FR-008 audit ───────┤                    └─► FR-007 Workflow ─┤  (Leave/Attendance/Payroll consume Workflow)
 FR-009 events ──────┘                         ▲              │
 FR-013 Rule Engine ───────────────────────────┴──────────────┘  (Workflow routing + Payroll formulas + Leave rules)
 FR-012 Reporting ◄── reads CQRS store fed by events (FR-009)
```

Critical path: **FR-015 → FR-002 → FR-013/FR-007 → FR-006**. Slips here slip the release.

---

## 6. Milestones

- **M0** Pre-dev docs approved (all Phase 7A modules) → build may start.
- **M1** (end S3) Foundations + engines demoable (the "platform proof").
- **M2** (end S6) Core HR + Leave + Attendance usable end-to-end.
- **M3** (end S8) Payroll + India compliance correct → **the trust milestone**.
- **M4** (end S10) Phase 7A feature-complete, hardened → security review → release.

---

## 7. Schedule Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Workflow Studio complexity (FR-007) | High — it's on the critical path | Prototype in S3; timebox; engine choice locked (ADR-010); descope marketplace/advanced patterns |
| Payroll/statutory correctness | High — launch blocker | Start rules early (S3/S7), dry-run simulation, compliance review before M3 |
| Pre-dev doc bottleneck (Rule 1) | Schedule slip before M0 | Parallelize Phase 3–5 docs; prioritize Phase 7A modules' specs |
| Foundation underestimation (Tenant/RLS, identity, effective-dating, audit/events, rules/workflow, configuration-as-data) | Ripples through all modules | Dedicate S1–S3 fully; no business module work until the foundation group is proven |
| Scope creep from deferred modules | Dilution | Enforce PRD OUT-of-scope list; change = PRD revision |

---

## 8. Later-Phase Module Backlog

| Phase | Modules | Required platform contracts before build |
|---|---|---|
| Phase 7B | Documents/letters/e-sign, HR service desk, onboarding/offboarding basics, provider health, implementation wizard | Document template engine, workflow templates, notification channels, audit, provider registry |
| Phase 7C | RAG assistant, richer reporting/BI, compliance intelligence, mobile reliability hardening, more attendance connectors | AI/RAG guardrails, semantic reporting layer, connector health, telemetry |
| Phase 7D | Recruitment/ATS, advanced onboarding, performance/goals/OKRs, LMS, engagement/surveys/recognition | Dynamic forms, workflow templates, assessment forms, document store, notification templates |
| Phase 7E | Advanced roster/workforce scheduling, shift swap, expense/travel/reimbursements, assets/IT requests, compensation review, multi-entity org graph UI | Rules engine, workflow, effective-dated core, approval matrix, payroll integration contracts, Shift Foundation from Phase 7A |
| Later phases | Workforce planning, integration marketplace, contingent workforce, multi-country payroll plugins, manager intelligence | Extension SDK, marketplace manifest, country plugin contract, analytics mart, AI tools |

No later-phase module may require changes to existing core modules. If a core contract is
missing, the contract must be added as a platform extension point and documented through
an ADR before implementation.

---

## Approval

Project Manager: ____ · Product Owner: ____ · Solution Architect: ____
(Status: Draft → Approved)
