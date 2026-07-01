# Architecture & Product Review — Platform (Pre-Development)

Document Owner: Solution Architect (Agent 6), with HR Domain, Product, SaaS & Security Architect hats
Created Date: 2026-06-14
Version: 1.1
Status: Approved (Bhajan Lal, 2026-06-18)

> Purpose: a critical architecture + product review of the approved phased-delivery PRD
> (`docs/02-product-requirements/PRD-001-platform-phased-delivery.md`). This does **not** repeat the
> PRD — it stress-tests it, designs the two hardest platform engines (Workflow + Rules),
> recommends the multi-tenant model, surfaces commonly-missed enterprise requirements,
> catalogs risks, and lists the ADRs required before any code. Inputs honored:
> approved Phase 1 research, approved Phase 2 PRD/roadmap, ADR-004, ADR-005, ADR-006,
> ADR-007, ADR-008, ADR-009, ADR-010, ADR-011, ADR-027,
> `ARCHITECTURE_PRINCIPLES.md`, `SECURITY_STANDARDS.md`, and
> `docs/05-architecture/ARCH-REVIEW-002-provider-agnostic-architecture.md`.

---

## 1. Missing Strategic Features (Competitive Advantage)

The PRD is sound but feature-led in places. The durable advantages over greytHR / Keka /
HROne / Darwinbox / Zoho / BambooHR / Workday / SAP SF / UKG are **platform capabilities**,
not modules. Gaps worth elevating:

**A. Configuration-as-data, end to end.** Not just workflows/forms — make *navigation,
dashboards, list views, validation, notifications, permissions, and reports* all
tenant-configurable data. This is the moat none of the incumbents fully deliver
("config ceiling" was the #1 validated pain).

**B. Sandbox → Production config promotion.** Enterprise buyers expect to test config
changes safely. A per-tenant **config environment + promotion pipeline** (export/diff/
promote/rollback) is rare in this segment and a strong enterprise differentiator.

**C. Effective-dated / bitemporal core.** Salary, org, policy changes must support
*past-dated corrections* and *future-dated* changes with full history ("as-of" queries).
Most SMB tools fake this; Workday's strength is exactly this. Build it into the core.

**D. Compliance Intelligence (proactive).** Statutory deadline calendar + predictive
alerts ("ESI filing due in 3 days", "14 employees crossed PF wage ceiling"). Validated
gap; differentiates from reactive incumbents.

**E. Open extensibility (the real "no rewrite" play):** a documented **extension/plugin
SDK + webhook/event subscriptions + public API with scopes**. Turns the platform into an
ecosystem (the future Marketplace) without per-customer code.

**F. Embedded analytics + semantic/NL query layer** over a per-tenant data mart — feeds
the AI report builder and manager insights later.

**G. Observability for the tenant admin** — config audit ("who changed this workflow"),
job/run visibility, and a status page. Trust features that reduce support load (pain P1).

**Enterprise expectations often dropped from early phase planning:** delegation/proxy approvals,
maker-checker (segregation of duties), data residency, retention/erasure (DPDP/GDPR),
SSO/SCIM, multi-legal-entity, time zones, multi-currency, bulk ops with rollback, API
governance, and DR/RPO-RTO. (Full catalog in §5.)

---

## 2. Workflow Studio Architecture (first-class capability)

Treat Workflow Studio as a **platform service** consumed by every module (leave,
attendance regularization, expense, onboarding, salary revision, separation), never as
leave-specific code.

### 2.1 Component view (ASCII)

```
            ┌─────────────────────────────────────────────────────────┐
            │                    WORKFLOW STUDIO                        │
            │                                                           │
  Designer  │  ┌───────────┐   ┌────────────┐   ┌──────────────────┐   │
  (React)──►│  │ Definition │  │  Validator  │  │  Versioning &     │   │
            │  │  Builder   │  │ (DAG/cycle) │  │  Publishing       │   │
            │  └─────┬──────┘   └────────────┘  └─────────┬────────┘   │
            │        │  WorkflowDefinition (JSON, versioned)│          │
            │        ▼                                      ▼          │
            │  ┌──────────────────────────────────────────────────┐   │
            │  │            WORKFLOW ENGINE (runtime)             │   │
            │  │  Instance Mgr │ State Machine │ Token/Step exec  │   │
            │  └───┬─────────┬───────────┬──────────────┬────────┘   │
            │      │         │           │              │            │
            │   Approval   Timer/SLA   Rule Engine   Action/        │
            │   Resolver   Scheduler   (cond/route)  Connectors     │
            └──────┼─────────┼───────────┼──────────────┼───────────┘
                   ▼         ▼           ▼              ▼
              Org/Deleg.   Quartz/    §3 Rules     Notification /
              hierarchy    Hangfire   Engine       Event Bus / API
```

### 2.2 Process Definition Model

A **WorkflowDefinition** is versioned JSON (configuration-as-data), not code:

```
WorkflowDefinition
  id, tenantId, key (e.g. "leave.approval"), version, status(draft/published/retired)
  variables[]            // typed context (employeeId, leaveDays, amount…)
  startState, endStates[]
  states[]   : { key, type(task|approval|decision|wait|parallel|join|end),
                 entryActions[], exitActions[], slaMinutes, escalation }
  transitions[] : { from, to, condition(ruleRef|expression), priority, event }
  participants[] : approver resolution (role | ABAC attr | hierarchy | delegate)
```

Design choice: **declarative graph + interpreter**, not codegen. Engine reads the JSON
and drives execution. Validate at publish time: connected graph, no orphan states,
reachable end state, no illegal cycles, all rule refs resolve.

### 2.3 State Machine Design

Each running workflow is a **WorkflowInstance** carrying a context bag and a current
state (or multiple tokens for parallel branches). Pattern: **explicit state machine with
event-driven transitions** (not implicit if/else). Transitions fire on events
(`Submitted`, `Approved`, `Rejected`, `TimerElapsed`, `Escalated`). Use the
**Saga/process-manager** pattern for long-running, async, multi-step processes.

- **Build vs buy (.NET):** a custom interpreter gives full config-as-data control and
  multi-tenant isolation; **Elsa Workflows** is a credible accelerator but adds opinion.
  *Recommendation:* build a lean interpreter over the JSON model (we need tenant-scoped
  versioning and our own Rule Engine anyway); revisit Elsa only if velocity demands it.
  → **ADR-010.**

### 2.4 Versioning & Migration

- Definitions are **immutable once published**; edits create `version+1`.
- **Running instances pin their definition version** — never silently re-point (this is
  how incumbents cause "post-update regression", validated pain P5).
- **Migration strategy:** on publish, choose per new version: (a) *drain* — old instances
  finish on old version; (b) *migrate* — map current state→new state via an explicit
  migration map (fail closed if a state has no mapping); (c) *abort+restart* for trivial
  cases. Store a `WorkflowMigrationPlan` and require approval to migrate live instances.

### 2.5 Approval Chains, Escalations, SLA

- **Approval resolution** is pluggable: static role, reporting hierarchy (n levels up),
  ABAC attribute (department head), committee (quorum/all/any), or **delegate** (§5).
- **SLA**: each approval/task has `slaMinutes`; a timer service (Quartz.NET/Hangfire)
  emits `TimerElapsed` → escalation policy (notify, reassign, auto-approve/-reject, or
  jump state). Escalations are themselves config, not code.
- **Reminders, reassignment, withdrawal, recall** are first-class events.

### 2.6 Templates & Marketplace

- **WorkflowTemplate** = a published, parameterized definition shippable across tenants
  (e.g., "India leave approval — 2 level"). Tenants clone → customize.
- **Marketplace** (future) = catalog of templates/connectors with entitlement checks.
  Design now: templates are versioned content with metadata + compatibility range; do
  not build storefront yet (YAGNI), but reserve the model. → **ADR-018.**

### 2.7 Auditability

Every instance records an **append-only event log**: state entered/left, decision, actor
(incl. on-behalf/delegate), timestamp, payload before/after, SLA breaches. This feeds the
Time-Machine audit (FR-008) and is tamper-evident (hash chain optional).

### 2.8 Suggested tables (SQL Server, schema `workflow`)

```
workflow.Definition         (DefinitionId, TenantId, [Key], Version, Status, JsonSpec,
                             PublishedBy, PublishedDate, + audit cols)  UNIQUE(TenantId,Key,Version)
workflow.Instance           (InstanceId, TenantId, DefinitionId, DefinitionVersion,
                             BusinessKey, CurrentState, Status, ContextJson, + audit)
workflow.InstanceToken      (TokenId, TenantId, InstanceId, State, Status) -- parallel branches
workflow.Task               (TaskId, TenantId, InstanceId, State, AssigneeType, AssigneeId,
                             DueAt, Status, DecidedBy, DecidedAt, Comment)
workflow.EventLog           (EventId, TenantId, InstanceId, Type, FromState, ToState, ActorId,
                             OnBehalfOfId, PayloadJson, CreatedAt)        -- append-only
workflow.Timer              (TimerId, TenantId, InstanceId, FireAt, Type, Fired)
workflow.Template           (TemplateId, TenantId, [Key], Version, JsonSpec, Metadata)
```
Index every table on `TenantId`; partition `EventLog`/`Instance` by time as they grow.

---

## 3. Business Rule Engine Architecture

A **generic** engine consumed by Workflow (routing conditions), Payroll (formulas),
Leave (eligibility/accrual), Validation (forms), and Compliance (statutory checks).
Principle: **rules are data**, evaluated at runtime — never `if (leaveDays > 5)` in code
(Golden Rule 2).

### 3.1 Evaluation pipeline (ASCII)

```
  Inputs (facts/context)            RuleSet (versioned, tenant-scoped)
        │                                   │
        ▼                                   ▼
  ┌──────────┐   resolve   ┌────────────────────────────┐
  │ Context  │────────────►│  Rule Selector (by key,     │
  │  facts   │             │  priority, effective date)  │
  └──────────┘             └──────────────┬─────────────┘
                                          ▼
                          ┌────────────────────────────┐
                          │  Expression Evaluator       │
                          │  (safe sandbox; no eval of  │
                          │  arbitrary code)            │
                          └──────────────┬─────────────┘
                          conflict resolution (priority/first-match/all)
                                          ▼
                              Outcomes: route | value | validation error | action
```

### 3.2 Rule Definition & Storage

```
Rule
  id, tenantId, key (e.g. "leave.sick.eligibility"), version, effectiveFrom/To,
  priority, status, salience,
  when:  expression  (boolean over context)        // condition
  then:  action(s)   (set value | raise error | route | call action)
  description, tags
```
Store as JSON in `rules.RuleSet` (versioned) + `rules.Rule`. RuleSets are immutable on
publish; effective-dated for statutory changes (e.g., new wage code from a date).

### 3.3 Expression Language

Do **not** allow arbitrary C#. Options: **JSON-Logic-style** AST (safe, serializable,
UI-buildable) or a vetted expression lib (**NCalc / DynamicExpresso**) behind a
**whitelist** (allowed functions, no I/O, time-bounded). *Recommendation:* JSON-Logic-AST
as the canonical, UI-friendly form for config-as-data; compile to a delegate cache for
speed. Provide a curated function library (date math, statutory helpers, lookups).
→ **ADR-011.**

### 3.4 Evaluation Modes & Patterns

- **Decision tables** for payroll components / tax slabs (rows = conditions → outputs).
- **Sequential priority** for validation & routing (first/highest match wins).
- **Forward-chaining (Rete-lite)** only if needed; default to simple, fast, ordered
  evaluation — most HR rules don't need full Rete.
- **Compiled + cached** per (tenant, ruleSet, version); invalidate on publish.

### 3.5 Domain applications

- **Payroll rules:** salary structure formulas, statutory slabs (PF/ESI/PT/LWF/TDS),
  proration, arrears, FBP — all decision tables/formulas, effective-dated.
- **Compliance rules:** eligibility & threshold checks → Compliance Intelligence alerts.
- **Leave rules:** accrual, carry-forward, encashment, eligibility, clubbing rules.
- **Validation rules:** dynamic form field constraints.

### 3.6 Governance

Rule changes are audited, versioned, simulated (dry-run against sample data), and
promoted sandbox→prod. **Never hot-edit a published payroll ruleset mid-cycle** — create
a new effective-dated version.

---

## 4. Multi-Tenant Architecture

### 4.1 Model comparison

| Model | Isolation | Cost/density | Noisy-neighbor | Per-tenant restore | Residency | Ops complexity |
|---|---|---|---|---|---|---|
| Shared DB, shared schema (TenantId discriminator) | Logical only | Best | High risk | Hard (row-level) | Hard | Low |
| Shared DB, schema-per-tenant | Medium | Good | Medium | Medium | Hard | Medium |
| Database-per-tenant | Strong | Lowest density | None | Easy | Easy | High |
| Sharded pools (groups of tenants per DB) | Medium-strong | Good | Low | Medium | Per-shard | Medium-high |

### 4.2 Recommendation by scale

```
   100 tenants     →  Shared DB + shared schema, TenantId on every table,
                      GLOBAL query filter + Row-Level Security (defense in depth).
                      Premium/regulated tenants: optional dedicated DB.

  1,000 tenants     →  Sharded POOLS: many tenants per DB, multiple DBs (shards).
                      Tenant→shard map in a catalog DB. Big/regulated tenants get
                      their own DB. Same code path; connection resolved per request.

 10,000 tenants     →  Pooled shards at scale + tiered placement:
                      • Standard tier  : pooled (N tenants/DB)
                      • Premium/Enterprise/Residency: dedicated DB (or region)
                      Elastic pools (Azure SQL) for cost; automated shard rebalancing.
```

**Net recommendation (→ ADR-005):** *Hybrid pooled model.* Start shared-schema with
`TenantId` + EF Core global filter **and** SQL Server **Row-Level Security** (so a code
bug can't leak across tenants — belt and suspenders). Abstract data access behind a
**tenant context resolver** + **shard/catalog map** from day one, so moving a tenant to a
dedicated DB later is configuration, not a rewrite.

### 4.3 Cross-cutting

- **Isolation/security:** every request carries a validated `TenantId`; RLS enforces at
  the DB; never trust client-supplied tenant. Encryption per §SECURITY_STANDARDS.
- **Performance:** per-tenant quotas/rate limits; cache keys namespaced by tenant;
  per-tenant Elasticsearch index/alias; avoid one tenant's batch starving others.
- **Data residency:** tenant→region pinning via the catalog; region-local DB + storage +
  search; residency is a placement decision, enabled by the catalog abstraction.
- **Backup:** pooled → logical per-tenant export + PITR at DB level; dedicated → native
  PITR per tenant. Define RPO/RTO (→ ADR-021). Test restores.
- **White-label:** branding/domain/email-template are tenant config; per-domain DKIM/SPF;
  TLS cert automation per custom domain.

---

## 5. Enterprise Requirements Commonly Missed (60)

**Identity & Access:** 1) Delegation framework (act-on-behalf during leave) · 2) Proxy/
substitute approvers · 3) Maker-checker / segregation of duties · 4) Break-glass
emergency access · 5) JIT privilege elevation · 6) Support impersonation ("login as")
with audit · 7) SSO (SAML/OIDC) multi-IdP per tenant · 8) SCIM provisioning/
deprovisioning · 9) Service/API client identities & scopes · 10) Concurrent-session
limits + forced logout.

**Org & Data model:** 11) Multi-legal-entity within a tenant · 12) Multi-location/
multi-country org · 13) **Effective-dated/bitemporal** records · 14) Position management
(vacant positions) vs person · 15) Matrix reporting (solid/dotted) · 16) Cost centers/
dimensions · 17) Rehire & dual employment · 18) Employee-ID schemes per entity.

**Time & Locale:** 19) Time zones per user/location · 20) Multi-currency + FX + rounding ·
21) Locale i18n (dates/numbers/RTL) · 22) Holiday calendars by location/religion ·
23) Configurable fiscal year / payroll periods · 24) Working-week variants (6-day, shifts).

**Operations:** 25) Bulk import/export with validation + **rollback** · 26) Async job
framework + run visibility · 27) Idempotency keys on critical ops · 28) Legacy data
migration tooling · 29) Optimistic concurrency (VersionNumber) · 30) Save-as-draft for
long forms · 31) Record locking during payroll lock.

**Compliance & Governance:** 32) Data retention & purge per data-class/country ·
33) DPDP/GDPR DSAR + right-to-erasure workflow · 34) Consent capture & management ·
35) Audit immutability (WORM/tamper-evident) · 36) Legal hold (suspend deletion) ·
37) PII classification + field-level encryption/masking · 38) Salary/sensitive-field
visibility rules · 39) Compliance calendar + statutory deadline alerts · 40) Configurable
data-access approval (e.g., view CTC).

**SaaS Platform:** 41) Feature flags + **entitlement/licensing** per tenant · 42) Tenant
lifecycle (provision/suspend/offboard/export) · 43) **Config versioning + sandbox→prod
promotion** · 44) Per-tenant rate limits/quotas · 45) Notification preferences &
multi-channel (email/SMS/WhatsApp/push/in-app) · 46) Outbound **webhooks** · 47) **API
governance** (versioning, deprecation policy, keys, OAuth scopes, throttling) ·
48) Config-change audit · 49) Per-tenant observability (metrics/tracing/correlation IDs) ·
50) Tenant data export/portability.

**Reliability & Content:** 51) Backup/restore + PITR per tenant · 52) DR / RPO-RTO ·
53) Multi-env parity (dev/stage/prod) · 54) Per-tenant search indexing · 55) File
storage: virus scan, type/size validation, retention · 56) Email deliverability (DKIM/
SPF per white-label domain) · 57) PDF/print at scale (payslips, letters) · 58) Document
templating + e-signature · 59) Accessibility (WCAG) + keyboard nav · 60) In-app guidance/
help & onboarding tours.

> Many map to engines already named in the plan (Notification, Audit, Integration, AI).
> The ones to **decide explicitly now** (because they shape the schema): effective-dating,
> multi-legal-entity, delegation, retention/erasure, tenant catalog/sharding.

---

## 6. Future-Proof Design (add modules without rewrites)

Design tenets that let ATS, onboarding, offboarding, PMS, LMS, engagement, service desk,
documents/e-sign, advanced workforce scheduling, expenses, asset management, compensation review,
workforce planning, marketplace, country payroll plugins, and AI Agents bolt on later:

1. **Modular monolith with hard module boundaries** (ADR-004): each module owns its
   schema; cross-module access only via **published events** or **internal contracts** —
   never direct table reads. This is what makes future service extraction safe.
2. **Everything-as-data engines** (Workflow, Rules, Forms, Reports, Notifications):
   new modules reuse them instead of re-implementing logic.
3. **Event bus as the integration spine.** New modules subscribe to existing events
   (`EmployeeCreated`, `PayrollProcessed`) — additive, non-breaking.
4. **Stable public API + extension SDK + webhooks** → Marketplace and AI Agents consume
   the platform like any client. Reserve an `extension` schema and a plugin contract now.
5. **Canonical Employee/Org domain** as the shared kernel (DDD) all modules reference;
   keep it lean and stable.
6. **AI-ready data layer:** per-tenant document store + vector index abstraction for RAG;
   AI Agents act through the same API/permissions (no privileged backdoor).
7. **Capability/entitlement model** so a new module is switched on per tenant via flags.

### 6.1 Open/Closed Module Ingestion Contract

The platform must be **open for extension and closed for modification**. A future module
is accepted only if it integrates through documented extension points instead of changing
existing core module logic.

Each future module must provide:

1. **Module manifest** — key, version, dependencies, feature flags, tenant entitlements,
   routes, navigation entries, widgets, and localization keys.
2. **Owned schema/migrations** — the module owns its schema and never reaches into another
   module's tables directly.
3. **Permission contract** — RBAC permissions, ABAC attributes, sensitive fields, and
   audit events.
4. **API contract** — versioned `/api/v1` endpoints with OpenAPI documentation.
5. **Event contract** — published/subscribed domain events with versioning and
   idempotency rules.
6. **Workflow/Rules/Form metadata** — approval flows, validations, policies, and custom
   fields stored as configuration, not code.
7. **UI extension metadata** — menu items, dashboards, widgets, command-palette actions,
   and screen definitions registered through metadata.
8. **Report/search/AI hooks** — report definitions, search index mapping, and AI tool
   permissions scoped by tenant/RBAC/ABAC.
9. **Provider adapters if needed** — storage, messaging, email/SMS/push, identity, search,
   BI, or LLM provider integration through the provider abstraction framework.

Core platform changes are allowed only to add a reusable extension point or stable
contract. Customer-specific or module-specific behavior must live in configuration,
extensions, plugins, or provider adapters.

```
        ┌──────── Platform Engines (shared) ─────────┐
        │ Identity  Workflow  Rules  Forms  Reports  │
        │ Notify    Audit     Search  AI/RAG  Events │
        └──────▲───────▲────────▲───────▲────────────┘
   reuse       │       │        │       │     subscribe via Event Bus
        ┌──────┴───┐ ┌─┴────┐ ┌─┴────┐ ┌┴─────┐ ┌─────────┐
        │ Core HR  │ │Leave │ │Payrol│ │Attend│ │ FUTURE: │
        │ (kernel) │ │      │ │      │ │      │ │ ATS PMS │
        └──────────┘ └──────┘ └──────┘ └──────┘ │ LMS …   │
                                                 └─────────┘
```

---

## 7. Technical Risks (with mitigations)

### 7.1 Architecture risks (Top 20)
1. Module boundary erosion (hidden cross-module table reads) → enforce via schema
   ownership + ArchUnit-style tests. 2. Workflow engine over-engineering → start lean
   interpreter, defer Rete/marketplace. 3. Config-as-data complexity explosion → strong
   validation + sandbox. 4. Distributed transaction creep → sagas + eventual consistency,
   not 2PC. 5. Event schema drift → versioned event contracts + schema registry.
6. Tight coupling to a workflow library → wrap behind our interface (ADR-010). 7. God
   "Employee" entity → keep kernel lean, push concerns to modules. 8. Leaky tenant context
   → single resolver, fail-closed. 9. Synchronous chains (payroll calls 6 services) →
   async/event. 10. Cache invalidation bugs on published config → version-keyed caches.
11. Time/effective-dating done late → bitemporal in core schema now. 12. No idempotency →
   dup events double-pay → idempotency keys. 13. Reporting on OLTP kills payroll → CQRS
   read store/data mart. 14. Hard-coded org assumptions (single entity) → multi-entity
   model now. 15. Migration of running workflows ignored → explicit migration plans.
16. Monolith deploy = whole-app risk → modular deploy gates, feature flags. 17. Shared
   library version hell → internal contracts, semver. 18. No back-pressure on async jobs →
   queues + concurrency limits. 19. ORM N+1 / heavy EF graphs → explicit projections,
   profiling. 20. Lack of ADRs → decisions re-litigated (this doc + §8).

### 7.2 Scalability risks (Top 20)
1. Noisy neighbor in shared schema → pools + RLS + quotas. 2. Hot tenant (huge payroll) →
   shard placement + dedicated DB tier. 3. Unbounded audit/event tables → partition +
   archive. 4. Payroll batch contention → isolated batch workers + windows. 5. Per-tenant
   ES index sprawl → alias strategy/rollover. 6. Connection-pool exhaustion across shards →
   pooled drivers + limits. 7. Cache stampede on config → request coalescing. 8. Large bulk
   imports block OLTP → async + chunking. 9. Notification fan-out spikes → queue + rate
   limit. 10. Report queries scan whole tables → read store + indexes. 11. Global locks on
   payroll lock → row/period-scoped locks. 12. File/PDF generation at month-end → async
   render farm. 13. Workflow timer storm (SLA) → scalable scheduler (sharded Hangfire).
14. Search reindex cost → incremental indexing. 15. Cross-shard reporting → per-tenant
   marts, no cross-tenant joins. 16. Vector index growth (RAG) → per-tenant namespaces +
   TTL. 17. Event bus backlog → autoscale consumers, DLQ. 18. Cold-start config load →
   warm caches. 19. Multi-region latency → region-local stacks. 20. Tenant onboarding
   thundering herd → throttled provisioning.

### 7.3 Security risks (Top 20)
1. Cross-tenant data leak → TenantId everywhere + **RLS** + tests. 2. Broken access
   control (RBAC/ABAC gaps) → central policy engine, deny-by-default. 3. IDOR on record
   IDs → authorize every object, not just route. 4. JWT misuse (no expiry/rotation) →
   short tokens + refresh + revocation. 5. Expression-language RCE in Rule Engine →
   sandbox/whitelist, no arbitrary code (§3.3). 6. Workflow action SSRF via connectors →
   egress allowlist. 7. Secrets in code/config → Key Vault, never in repo. 8. PII at rest
   unencrypted → field-level encryption/masking. 9. File upload malware → AV scan +
   type/size validation. 10. Audit log tampering → append-only/WORM, hash chain.
11. Impersonation abuse → scoped, time-boxed, fully audited. 12. White-label domain
   spoofing → domain verification, per-domain certs. 13. SQL injection (dynamic rules/
   reports) → parameterized, no dynamic SQL. 14. Mass assignment → explicit DTOs.
15. CSRF/XSS in config-driven UI → output encoding, CSP. 16. Over-broad API scopes →
   least-privilege OAuth scopes. 17. Tenant admin → platform privilege escalation →
   strict role separation. 18. Backup data exposure → encrypted backups, access control.
19. Logging PII → redaction. 20. DSAR/erasure incompleteness → data map + erasure
   workflow.

### 7.4 Compliance risks (Top 20)
1. India statutory change breaks payroll → rules-as-data, effective-dated. 2. PF/ESI/PT
   state variations → state-scoped rule sets. 3. Wage code transition → versioned rules +
   simulation. 4. DPDP (India) data-residency/consent → residency placement + consent
   capture. 5. GDPR (future EU) erasure/portability → DSAR workflows. 6. TDS/Form-16
   accuracy → reconciliation + audit. 7. Retention over/under-keeping → per-class policies.
8. Cross-border transfer (UAE/USA/UK) → region pinning, SCCs. 9. Audit trail
   admissibility → immutable, time-stamped. 10. Statutory deadline misses → compliance
   calendar alerts. 11. Gratuity/FNF miscalculation → tested rule sets. 12. Payroll GL
   posting mismatch → reconciliation reports. 13. Working-hours/overtime law variance →
   configurable. 14. Minimum-wage compliance → rule checks. 15. POSH/maternity statutory
   records → configurable policy. 16. Document legal validity (e-sign) → compliant
   provider. 17. Data processor agreements per tenant → contractual + technical isolation.
18. Right-to-be-forgotten vs statutory retention conflict → legal-hold precedence rules.
19. Accessibility legal requirements → WCAG. 20. Multi-country payroll plugin certification
   → plugin compliance gating.

---

## 8. ADR Status Tracker (required before development)

Approved baseline:

- **ADR-001** React / Next.js frontend.
- **ADR-002** .NET primary backend.
- **ADR-003** SQL Server database.
- **ADR-004** Modular Monolith.
- **ADR-005** Multi-tenancy model: hybrid pooled + RLS + catalog/sharding.
- **ADR-006** Tenant context & data-access pattern: resolver, global filter, SQL Server RLS.
- **ADR-007** Effective-dated / bitemporal data strategy.
- **ADR-008** Identity & access: JWT, SSO/OIDC, SCIM, RBAC+ABAC policy engine.
- **ADR-009** Event-driven backbone: broker abstraction, outbox, idempotent consumers.
- **ADR-010** Workflow engine: lean interpreter over versioned definitions.
- **ADR-011** Rule engine model + safe expression language.
- **ADR-027** Provider-Abstraction Framework: storage, cache, messaging, notification,
  identity, search, BI, and LLM providers selected per tenant through configuration.

Tracked for Phase 6 AI approval:

- **ADR-019** AI/RAG architecture: multi-provider LLM abstraction, tenant/admin model registry,
  RBAC/ABAC-scoped RAG, no privileged AI backdoor. This is architecturally aligned here
  but formally approved with the AI Strategy gate.

Still to author / confirm before the relevant phase:

- **ADR-012** Forms/metadata storage strategy.
- **ADR-013** Reporting/analytics: CQRS read store / per-tenant mart.
- **ADR-014** Caching strategy: Redis, tenant-namespaced, config invalidation.
- **ADR-015** Search: Elasticsearch index-per-tenant vs shared index + filters.
- **ADR-016** File storage, AV scanning, retention.
- **ADR-017** Config versioning + sandbox-to-production promotion.
- **ADR-018** Extension/plugin SDK + Marketplace contract.
- **ADR-020** Localization/i18n + time zone + multi-currency.
- **ADR-021** Backup/DR, RPO/RTO, per-tenant restore.
- **ADR-022** Data retention, DPDP/GDPR erasure & consent.
- **ADR-023** API governance: versioning, deprecation, scopes, rate limits.
- **ADR-024** Audit immutability: append-only/WORM, hash chain.
- **ADR-025** Observability: logging, tracing, correlation IDs, per-tenant metrics.
- **ADR-026** CI/CD, migration & release safety.
- **ADR-028** Notification provider abstraction.
- **ADR-029** Reporting/BI provider abstraction.

---

## 9. Roadmap Validation (MoSCoW re-scope)

Re-scored on **business value × differentiation × complexity** vs the PRD.

**MUST (Phase 7A) — approved baseline:** Phase 7A must start with the foundation group,
then build the business modules that depend on it.

Foundation group:

- **Tenant Catalog + RLS** (FR-015) and multi-tenant isolation (FR-001).
- **Branch / Office Hierarchy and Scoped Administration** as a tenant-internal ABAC
  boundary.
- **Identity + RBAC/ABAC** (FR-002).
- **Effective-dated / bitemporal core** (FR-014).
- **Audit / Time-Machine** (FR-008).
- **Event Bus + Outbox** (FR-009).
- **Rule Engine core** (FR-013).
- **Workflow Engine / Studio core** (FR-007).
- **Configuration-as-Data** for workflows, rules, forms, reports, navigation, permissions,
  notifications, and tenant-specific behavior.

Business modules after the foundation group:

- Core HR/ESS (FR-003).
- Leave (FR-004).
- Attendance + one connector + Shift Foundation (FR-005).
- Payroll + India compliance including FBP and mid-cycle CTC (FR-006).
- Standard reporting (part of FR-012).

Delegation/proxy approvals remain part of FR-007 because approval workflows are not
enterprise-ready without them.

**SHOULD (Phase 7B–7C):** White-label (FR-010), RAG HR Assistant thin slice (FR-011),
Config sandbox→prod promotion, Compliance calendar/alerts (basic), Notification
preferences + multi-channel, Bulk ops with rollback, SSO/OIDC, document/letter/e-sign,
HR service desk, onboarding/offboarding basics, provider health, implementation wizard,
richer reporting/BI, mobile reliability hardening.

**NEXT (Phase 7D–7E):** Recruitment/ATS, advanced onboarding, Performance/PMS/goals/OKRs,
LMS, engagement/surveys/recognition, advanced roster/workforce scheduling, shift swap, expense/travel/reimbursements,
asset/IT requests, compensation review, multi-entity org graph UI.

**DEFER (later phases / validate first):** Workforce planning/forecasting, integration
marketplace, contingent workforce, multi-country payroll plugins, advanced manager
intelligence, marketplace storefront.

**Headline:** the approved PRD and roadmap are now correct: Phase 7A does not begin by
building Leave, Attendance, or Payroll in isolation. It begins by proving the platform
foundation group: Tenant Catalog + RLS, Branch / Office Hierarchy, Identity + RBAC/ABAC,
Effective Dating, Audit/Time Machine, Event Bus, Rule Engine, Workflow Engine, and
Configuration-as-Data.
Business modules are then layered on top. Later modules such as ATS, LMS, PMS, Service
Desk, workforce planning, and marketplace can be added through extension contracts, but
these foundations are costly and risky to retrofit.

---

## Approval

Solution Architect: Approved · Security Architect: Approved · Database Architect: Approved ·
Product Owner: Approved (Bhajan Lal, 2026-06-18)
