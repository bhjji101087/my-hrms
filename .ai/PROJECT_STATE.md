# PROJECT_STATE.md — Project Memory Checkpoint

This is the single source of truth for *where the project is right now*.
Every agent reads this first and updates it last. Keep it honest.

---

## Current Status

- **Product strategy (Owner, 2026-06-15):** **Full-product launch with phased delivery.**
  Build the complete application, then enter the market. Build order stays dependency-first
  (foundations → engines → modules). Provider adapters are added per customer demand
  (integration axis, not a launch gate). Product and roadmap docs now use phase-based
  language.
- **2026-06-16 scope refresh:** Phase 1 research, gap analysis, PRD, roadmap, and
  architecture review now include missing modules and phased priorities.
- **2026-06-17 owner approval:** refreshed Phase 1 market research, gap analysis,
  Product Owner positioning hypothesis, Phase 2 PRD, and phased roadmap are Approved.
- **2026-06-18 owner approval:** Phase 3 architecture package is Approved: architecture
  baseline, provider abstraction, key ADRs, DB foundations, tenant/identity DB designs,
  security threat model, and final gate review.
- **2026-06-18 Phase 4 alignment:** approved UI package was checked against refreshed
  architecture; provider-management UX was added to the design spec; Phase 4 is closed.
- **2026-06-22 owner approval:** Phase 5 foundational API specification,
  machine-readable OpenAPI YAML, and review checkpoint are Approved.
- **2026-06-22 Phase 6 hardening:** AI Strategy v2.0 now incorporates enterprise
  vector-store, observability, memory, cost, evaluation, cache, confidence, operations,
  security, API, acceptance, and sequential delivery requirements.
- **2026-06-22 owner approval:** AI Strategy v2.0 is Approved. Phase 6 remains open
  for the required architecture decisions and companion documents.
- **2026-06-22 Phase 6A architecture package:** ADR-019 was refreshed as the enterprise
  AI/RAG umbrella decision and ADR-030 Vector Store Strategy was created.
- **2026-06-22 owner vector-store decision:** self-hosted Qdrant is the first development
  and initial-deployment adapter to avoid a paid managed vector-search subscription.
  Azure AI Search is an optional later adapter through `IVectorStore`; existing vectors
  switch through controlled rebuild/validation rather than feature-code changes.
- **2026-06-22 owner approval:** ADR-030 Enterprise Vector Store Strategy is Approved.
  ADR-019 remains the only open Phase 6A architecture decision.
- **2026-06-23 owner approval:** ADR-019 Enterprise AI/RAG Platform Architecture is
  Approved. Phase 6A is complete and Phase 6B enterprise-control ADRs are unblocked.
- **2026-06-23 Phase 6B draft:** ADR-031 AI Observability and Telemetry defines an
  OpenTelemetry-based, self-hosted initial stack, privacy-safe telemetry, SLO/SLA evidence,
  dashboards, alerts, runbooks, retention, and managed-backend portability.
- **2026-06-23 owner approval:** ADR-031 AI Observability and Telemetry is Approved.
  ADR-032 Conversation Memory Strategy is now the next Phase 6B decision.
- **2026-06-23 Phase 6B draft:** ADR-032 Conversation Memory Strategy defines SessionOnly
  default memory, Redis short-term context, opt-in encrypted SQL summaries, per-turn
  reauthorization, event invalidation, deletion/retention, and stateless fallback.
- **2026-06-24 owner enhancement and approval:** ADR-032 now includes future Workspace
  Memory separation, summary turn lineage and quality metadata, role-matrix invalidation,
  conversation reset, enforced purpose boundaries, and governed 30/60/90-day retention;
  the document is Approved.
- **2026-06-25 Phase 6B draft:** ADR-033 AI Cost Governance defines explicit paid-service
  activation, normalized tenant usage/cost ledger, effective-dated prices, atomic budget
  reservation, configurable quotas, forecasts, showback/reconciliation, safe hard limits,
  and provider-independent cost controls.
- **2026-06-25 owner enhancement and approval:** ADR-033 now also includes reservation
  reasons, versioned forecast-confidence scores, trial/feature expiry, controlled emergency
  overrides, rebuildable utilization snapshots, tenant-specific commercial-term isolation,
  and ADR-036-gated exchange-rate governance; the document is Approved.
- **2026-06-25 owner documentation directive:** all new and refreshed project documents must
  meet enterprise implementation/governance standards and use current web research from
  authoritative primary sources where the subject can change or external evidence matters;
  sources and validation date must be recorded in the document.
- **2026-06-25 Phase 6B draft:** ADR-034 Enterprise AI and RAG Evaluation Framework defines
  risk-tiered use cases, full-system release candidates, sealed benchmark governance,
  multi-method metrics, employment fairness/human oversight, independent promotion gates,
  production drift, incident learning, approval expiry, and full-bundle rollback.
- **2026-06-25 owner enhancement and approval:** ADR-034 now also includes explicit
  hallucination rate/severity, approval-expiry reasons, dataset review/expiry, provider
  behavior drift, accountable risk owners, and reviewer agreement/consistency governance;
  the document is Approved.
- **2026-06-25 Phase 6B draft:** ADR-035 Enterprise Semantic and Retrieval Cache Architecture
  defines self-hosted Redis as the first cache/semantic-index adapter, keeps Qdrant for
  canonical knowledge vectors, and adds deny-by-default eligibility, hard tenant/security
  partitioning, per-hit reauthorization, versioned invalidation, poisoning defenses,
  provider prompt-cache boundaries, cost/operations controls, and safe miss behavior.
- **2026-06-25 owner enhancement and approval:** ADR-035 now also includes explicit cache
  effectiveness/quality metrics, policy review/expiry, governed warm-up, emergency
  disablement, Redis Sentinel/Cluster HA profiles, and namespace rotation evidence; the
  document is Approved and Phase 6B is complete.
- **2026-06-25 Phase 6C draft:** the Enterprise AI Operations Handbook now defines service
  ownership, on-call/incident command, SLO/error budgets, telemetry/alerts, degraded modes,
  release/rollback, provider/Qdrant/Redis/ingestion/evaluation/cost/security operations,
  DR/deletion, ORR, exercises, and 18 production runbooks.
- **2026-06-27 Phase 6C owner enhancement:** the Enterprise AI Operations Handbook v1.1
  now adds AI model lifecycle governance, business KPI monitoring, AI Governance Board,
  runbook reference matrix, and a reserved future AI Agent Operations section.
- **2026-06-27 owner approval:** AI-OPS-001 Enterprise AI Operations Handbook v1.1 is
  Approved. Phase 6C now moves to the AI Security Extension and retention/DR alignment
  documents.
- **2026-06-27 Phase 6C draft:** SEC-AI-001 AI Security Extension was created using
  current OWASP GenAI, NIST, NCSC, Qdrant, Redis, and EU AI Act guidance; it is Draft and
  ready for owner and specialist review.
- **2026-06-27 owner approval:** SEC-AI-001 AI Security Extension is Approved.
- **2026-06-27 Phase 6C drafts:** ADR-022 Data Retention, Archival, Legal Hold, and
  Deletion plus AI-DR-001 AI Disaster Recovery Design and Exercise Plan were drafted using
  current DPDP, GDPR, NIST, Microsoft, Qdrant, Redis, and RabbitMQ guidance.
- **2026-06-27 owner approval:** ADR-022 Data Retention, Archival, Legal Hold, and
  Deletion plus AI-DR-001 AI Disaster Recovery Design and Exercise Plan are Approved.
- **2026-06-27 Phase 6D draft:** AI API/OpenAPI package was created with API-SPEC-002,
  OPENAPI-002, and the Phase 6D review checkpoint using current OpenAPI, OWASP API
  Security, and RFC guidance.
- **2026-06-27 owner enhancement and approval:** the Phase 6D AI API/OpenAPI package now
  includes SSE streaming AI responses, batch AI operations, standardized rate-limit/retry
  headers, API versioning/deprecation policy, and bulk knowledge operations; API-SPEC-002,
  OPENAPI-002, and PHASE-6D-REVIEW-001 are Approved.
- **2026-06-27 Phase 6D implementation documentation draft:** the AI constitutional
  five-document implementation set is drafted: FEAT-AI-001, TECH-AI-001,
  DB-DESIGN-AI-001, UI-AI-001, and TEST-AI-001. Development remains locked until all five
  are Approved.
- **2026-06-27 owner approval:** FEAT-AI-001, TECH-AI-001, DB-DESIGN-AI-001,
  UI-AI-001, and TEST-AI-001 are Approved. The AI platform documentation gate is complete,
  including AI database design. Broader platform database implementation remains blocked
  until the first foundation feature companion docs, especially Tenant Catalog + RLS and
  Identity + RBAC/ABAC, are Approved.
- **2026-06-27 Tenant Catalog + RLS refresh:** the four remaining FR-015 companion docs
  were upgraded from thin Drafts to enterprise Review-ready documents using approved
  ADR-005/006, DB-DESIGN-TENANT-001, SEC-DESIGN-001, and current Microsoft/NIST/OWASP/WCAG
  references. DB-DESIGN-TENANT-001 is already Approved; FEAT-TENANT-001,
  TECH-TENANT-001, UI-TENANT-001, and TEST-TENANT-001 now need owner approval.
- **2026-06-27 owner approval:** Tenant Catalog + RLS five-document set is Approved:
  FEAT-TENANT-001, TECH-TENANT-001, DB-DESIGN-TENANT-001, UI-TENANT-001, and
  TEST-TENANT-001. FR-015 Tenant Catalog + RLS is now ready for implementation planning;
  the next foundation documentation blocker is Identity + RBAC/ABAC.
- **2026-06-28 Identity business requirements enhancement:** FEAT-IDENTITY-001 was updated
  from Draft to Review with enterprise security additions for break-glass emergency access,
  tenant-configurable password policy, device/session management, adaptive risk-based MFA,
  and account lockout/brute-force protection, using current NIST, OWASP, and Microsoft
  identity guidance.
- **2026-06-28 Identity technical design enhancement:** TECH-IDENTITY-001 was updated from
  Draft to Review with break-glass authentication flow, authentication/authorization
  sequence diagrams, JWT signing and key-management strategy, distributed session/token
  revocation architecture, and authorization decision traceability, using current RFC,
  OpenID, NIST, OWASP, and Microsoft identity/key-management guidance.
- **2026-06-28 Identity UI design enhancement:** UI-IDENTITY-001 was updated from Draft to
  Review with break-glass emergency login, active sessions/device management, complete
  password/account recovery, adaptive risk-based MFA experience, security dashboard/login
  history, and supporting enterprise identity administration screens.
- **2026-06-28 owner approval:** Identity + RBAC/ABAC five-document set is Approved:
  FEAT-IDENTITY-001, TECH-IDENTITY-001, DB-DESIGN-IDENTITY-001, UI-IDENTITY-001, and
  TEST-IDENTITY-001. FR-002 Identity + RBAC/ABAC is now ready for implementation planning.
- **2026-06-28 Identity database design amendment:** DB-DESIGN-IDENTITY-001 v1.2 is
  Approved with break-glass emergency-access tables, tenant password policy configuration,
  authentication security events, enhanced session/device fields, and effective-dated
  Role, RolePermission, AbacPolicy, and PasswordPolicy governance.
- **2026-06-28 Effective Dating business specification approval:** FEAT-EFFECTIVE-DATING-001
  v1.1 is Approved with platform standards for open-ended records, validation,
  tenant-local effective dates, UTC system timestamps, bulk-operation compatibility, and
  common `asOfDate` behavior.
- **2026-06-28 Effective Dating technical design approval:** TECH-EFFECTIVE-DATING-001
  v1.1 is Approved with optimistic concurrency, chunked bulk operations, shared valid-time
  boundary rules, temporal-history fallback providers, explain-history response contract,
  and outbox-backed event delivery guarantees.
- **2026-06-28 Effective Dating database design approval:** DB-DESIGN-EFFECTIVE-DATING-001
  v1.1 is Approved with explicit business-key standards, database check constraints,
  open-ended record rules, UTC system timestamps, supersession chains, soft-delete/history
  behavior, bulk-operation database rules, naming conventions, partitioning guidance, and
  optimistic concurrency.
- **2026-06-28 Effective Dating UI design approval:** UI-EFFECTIVE-DATING-001 v1.1 is
  Approved with effective-date preview, visual history timeline, real-time overlap
  detection, immutable-history UX, status labels and semantic colors, audit drawer,
  compare view, as-of historical-data indicator, responsive behavior, bulk-operation UX,
  and WCAG 2.2 AA alignment.
- **2026-06-28 Effective Dating test plan approval:** TEST-EFFECTIVE-DATING-001 v1.1 is
  Approved with bitemporal time-travel tests, time-zone/calendar boundary tests,
  optimistic concurrency, rollback/recovery, supersession, soft delete, bulk operations,
  API contracts, event reliability, UI, negative, scalability, DR, and regression coverage.
- **2026-06-28 Effective Dating documentation gate complete:** Effective Dating and
  Bitemporal Core now has all five required documents Approved.
- **Current Phase:** Phase 7A readiness — Tenant Catalog + RLS and Identity + RBAC/ABAC approved;
  Effective Dating five-document set approved
- **Current Sprint:** None (pre-development)
- **Current Owner:** Product Owner + Solution Architecture + Database + UI/UX + QA + Security
- **Next Agent:** Program Director to confirm whether to start implementation planning for the approved S1 foundations or refresh the Leave feature docs next
- **Last Updated:** 2026-06-28

---

## Approved Documents

| Document | Location | Status |
|---|---|---|
| HRMS Master Plan | `.ai/HRMS_Plan.md` | Approved |
| Architecture Principles | `.ai/ARCHITECTURE_PRINCIPLES.md` | Approved |
| Competitor Analysis (India, v1.3 refresh) | `docs/01-market-research/competitor-analysis-india.md` | Approved 2026-06-17 |
| Competitor Gap Analysis | `docs/03-gap-analysis/competitor-gap-analysis.md` | Approved 2026-06-17 |
| Product Owner Positioning Hypothesis | `docs/01-market-research/POSITIONING-HYPOTHESIS-001-product-owner.md` | Approved 2026-06-17 |
| PRD — Platform Phased Delivery (v1.1 refresh) | `docs/02-product-requirements/PRD-001-platform-phased-delivery.md` | Approved 2026-06-17 |
| Roadmap — Phased Delivery | `docs/04-roadmap/ROADMAP-001-phased-delivery.md` | Approved 2026-06-17 |
| Architecture & Product Review — Platform | `docs/05-architecture/ARCH-REVIEW-001-platform-architecture-review.md` | Approved 2026-06-18 |
| Provider-Agnostic Architecture Review | `docs/05-architecture/ARCH-REVIEW-002-provider-agnostic-architecture.md` | Approved 2026-06-18 |
| Phase 3 Final Review — Architecture Gate | `docs/05-architecture/PHASE-3-FINAL-REVIEW-001-architecture-gate.md` | Approved 2026-06-18 |
| Database Design — Platform Foundations v1.2 | `docs/06-database/DB-DESIGN-001-foundations.md` | Approved; Qdrant/VectorStore amendment 2026-06-22 |
| Database Design — Tenant Catalog + RLS | `docs/06-database/DB-DESIGN-TENANT-001.md` | Approved 2026-06-18 |
| Database Design — Identity & Access | `docs/06-database/DB-DESIGN-IDENTITY-001.md` | Approved; security DB amendment 2026-06-28 |
| Security Design & Threat Model | `docs/12-security/SEC-DESIGN-001-threat-model.md` | Approved 2026-06-18 |
| UI Design System (DESIGN-SYSTEM-001) | `docs/07-ui-ux/DESIGN-SYSTEM-001-foundations.md` | Approved 2026-06-14 |
| UI Screen Specs (SCREENS-001) | `docs/07-ui-ux/SCREENS-001-foundational-screens.md` | Approved 2026-06-14 |
| UI Design Spec v2.1 + prototype (DESIGN-SPEC-002) | `docs/07-ui-ux/DESIGN-SPEC-002-people-ops-platform.md` | Approved 2026-06-18 alignment refresh |
| Phase 4 UI Architecture Alignment Checkpoint | `docs/07-ui-ux/PHASE-4-ALIGNMENT-001-ui-architecture-checkpoint.md` | Approved 2026-06-18 |
| API Specification — Foundational Endpoints v1.2 | `docs/08-api-specs/API-SPEC-001-foundational.md` | Approved; extensible provider-category amendment 2026-06-22 |
| OpenAPI YAML — Foundational v1 (spec 1.2.0) | `docs/08-api-specs/OPENAPI-001-foundational-v1.yaml` | Approved; extensible provider-category amendment 2026-06-22 |
| Phase 5 Review — Foundational OpenAPI Package | `docs/08-api-specs/PHASE-5-REVIEW-001-openapi-foundational.md` | Approved 2026-06-22 |
| AI Strategy — Enterprise RAG Architecture, Operations, and Prompt Library v2.1 | `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md` | Approved; Qdrant-first amendment 2026-06-22 |
| ADR-006 Tenant context/data access | `docs/16-decisions/ADR-006-tenant-context-data-access.md` | Approved 2026-06-18 |
| ADR-008 Identity and access | `docs/16-decisions/ADR-008-identity-access.md` | Approved 2026-06-18 |
| ADR-009 Event-driven backbone | `docs/16-decisions/ADR-009-event-driven-backbone.md` | Approved 2026-06-18 |
| ADR-027 Provider-Abstraction Framework | `docs/16-decisions/ADR-027-provider-abstraction-framework.md` | Approved 2026-06-18 |
| ADR-019 Enterprise AI/RAG Platform Architecture | `docs/16-decisions/ADR-019-ai-rag-architecture.md` | Approved 2026-06-23 |
| ADR-030 Enterprise Vector Store Strategy | `docs/16-decisions/ADR-030-vector-store-strategy.md` | Approved 2026-06-22 |
| ADR-031 AI Observability and Telemetry | `docs/16-decisions/ADR-031-ai-observability-telemetry.md` | Approved 2026-06-23 |
| ADR-032 Conversation Memory Strategy | `docs/16-decisions/ADR-032-conversation-memory-strategy.md` | Approved 2026-06-24 |
| ADR-033 AI Cost Governance | `docs/16-decisions/ADR-033-ai-cost-governance.md` | Approved 2026-06-25 |
| ADR-034 Enterprise AI and RAG Evaluation Framework | `docs/16-decisions/ADR-034-rag-evaluation-framework.md` | Approved 2026-06-25 |
| ADR-035 Enterprise Semantic and Retrieval Cache Architecture | `docs/16-decisions/ADR-035-semantic-cache-architecture.md` | Approved 2026-06-25 |
| ADR-037 Data Access = Dapper + DbUp (supersedes EF Core mechanism) | `docs/16-decisions/ADR-037-data-access-dapper-dbup.md` | Approved 2026-07-09 |
| AI Operations Handbook v1.1 | `docs/15-ai/AI-OPS-001-enterprise-ai-operations.md` | Approved 2026-06-27 |
| AI Security Extension | `docs/12-security/SEC-AI-001-ai-security-extension.md` | Approved 2026-06-27 |
| ADR-022 Data Retention, Archival, Legal Hold, and Deletion | `docs/16-decisions/ADR-022-data-retention-archival-legal-hold-deletion.md` | Approved 2026-06-27 |
| AI Disaster Recovery Design and Exercise Plan | `docs/15-ai/AI-DR-001-disaster-recovery-and-exercise-plan.md` | Approved 2026-06-27 |
| AI API Specification v1 | `docs/08-api-specs/API-SPEC-002-ai-platform-v1.md` | Approved 2026-06-27 |
| OpenAPI YAML — AI Platform v1 | `docs/08-api-specs/OPENAPI-002-ai-platform-v1.yaml` | Approved 2026-06-27 |
| Phase 6D Review — AI OpenAPI Package | `docs/08-api-specs/PHASE-6D-REVIEW-001-ai-openapi-package.md` | Approved 2026-06-27 |
| AI Business Requirements | `docs/02-product-requirements/FEAT-AI-001-business-requirements.md` | Approved 2026-06-27 |
| AI Technical Design | `docs/05-architecture/TECH-AI-001-ai-platform-technical-design.md` | Approved 2026-06-27 |
| AI Database Design | `docs/06-database/DB-DESIGN-AI-001-ai-platform.md` | Approved 2026-06-27 |
| AI UI Design | `docs/07-ui-ux/UI-AI-001-screens.md` | Approved 2026-06-27 |
| AI Test Plan | `docs/10-testing/TEST-AI-001-test-plan.md` | Approved 2026-06-27 |
| Tenant Business Requirements | `docs/02-product-requirements/FEAT-TENANT-001-business-requirements.md` | Approved 2026-06-27 |
| Tenant Technical Design | `docs/09-development/TECH-TENANT-001-technical-design.md` | Approved 2026-06-27 |
| Tenant UI Design | `docs/07-ui-ux/UI-TENANT-001-screens.md` | Approved 2026-06-27 |
| Tenant Test Plan | `docs/10-testing/TEST-TENANT-001-test-plan.md` | Approved 2026-06-27 |
| Identity Business Requirements | `docs/02-product-requirements/FEAT-IDENTITY-001-business-requirements.md` | Approved 2026-06-28 |
| Identity Technical Design | `docs/09-development/TECH-IDENTITY-001-technical-design.md` | Approved 2026-06-28 |
| Identity UI Design | `docs/07-ui-ux/UI-IDENTITY-001-screens.md` | Approved 2026-06-28 |
| Identity Test Plan | `docs/10-testing/TEST-IDENTITY-001-test-plan.md` | Approved 2026-06-28 |
| Effective Dating Business Requirements | `docs/02-product-requirements/FEAT-EFFECTIVE-DATING-001-business-requirements.md` | Approved 2026-06-28 |
| Effective Dating Technical Design | `docs/09-development/TECH-EFFECTIVE-DATING-001-technical-design.md` | Approved 2026-06-28 |
| Effective Dating Database Design | `docs/06-database/DB-DESIGN-EFFECTIVE-DATING-001.md` | Approved 2026-06-28 |
| Effective Dating UI Design | `docs/07-ui-ux/UI-EFFECTIVE-DATING-001-screens.md` | Approved 2026-06-28 |
| Effective Dating Test Plan | `docs/10-testing/TEST-EFFECTIVE-DATING-001-test-plan.md` | Approved 2026-06-28 |
| ADR-005 Multi-tenancy | `docs/16-decisions/ADR-005-multi-tenancy-model.md` | Approved 2026-06-14 |
| ADR-007 Effective-dating | `docs/16-decisions/ADR-007-effective-dated-bitemporal-data.md` | Approved 2026-06-14 |
| ADR-010 Workflow engine | `docs/16-decisions/ADR-010-workflow-engine.md` | Approved 2026-06-14 |
| ADR-011 Rule engine | `docs/16-decisions/ADR-011-rule-engine-expression-language.md` | Approved 2026-06-14 |
| ADR-001 React/Next.js frontend | `docs/16-decisions/ADR-001-react-frontend.md` | Approved |
| ADR-002 .NET primary backend | `docs/16-decisions/ADR-002-dotnet-primary.md` | Approved |
| ADR-003 SQL Server database | `docs/16-decisions/ADR-003-sql-server.md` | Approved |
| ADR-004 Modular Monolith | `docs/16-decisions/ADR-004-modular-monolith.md` | Approved |

## Pending / In-Progress Documents

| Document | Target Folder | Owner | Status |
|---|---|---|---|
| Phase 1 market research refresh review | `docs/01-market-research/PHASE-1-REVIEW-001-market-research-refresh.md` | Codex Review Agent | Draft |
| Financial Exchange-Rate Governance ADR | `docs/16-decisions/ADR-036` | Solution Architect / Finance / Security | Reserved by ADR-033; required before cross-currency implementation |
| Leave feature — 5-doc set (S5, pattern proof) | `FEAT-LEAVE-001` · `TECH-LEAVE-001` · `DB-DESIGN-LEAVE-001` · `UI-LEAVE-001` · `TEST-LEAVE-001` | Cross-agent | Draft (all 5) |
| ADR-012–026 (remaining ADRs; +028 notif, +029 BI per ARCH-REVIEW-002) | `docs/16-decisions` | Solution Architect | Not started |
| Module backlog — phased product delivery | `docs/21-product-backlog/MODULE-BACKLOG-001-phased-modules.md` | Product Owner | Draft |

---

## Phase Gate Tracker

| Phase | Gate (must be Approved to advance) | State |
|---|---|---|
| 1 Market Research | Market analysis + gap analysis | Approved 2026-06-17 |
| 2 Product Discovery | PRD, roadmap | Approved 2026-06-17 |
| 3 Architecture | Architecture, DB, integration, security docs | Approved 2026-06-18 |
| 4 UX/UI | Design system + wireframes + **visual mockups signed off** | Approved 2026-06-18 alignment refresh |
| 5 API Design | OpenAPI specs | Approved 2026-06-22 |
| 6 AI Strategy | Prompt library, RAG design | Approved 2026-06-27 — Phase 6A/6B/6C/6D and AI five-document implementation set complete |
| 7 Development | (per-feature: 5 docs approved) + **UI visual designs signed off** | FR-015 Tenant Catalog + RLS, FR-002 Identity + RBAC/ABAC, and Effective Dating + Bitemporal Core ready for implementation planning; Leave feature docs remain Draft |
| 8 Testing | Test plans, coverage ≥ 85% | Locked |
| 9 Release | Security review, release notes | Locked |

**Hard sequential gate:** A phase may not start or advance until the prior phase is
complete and its required documents are Approved. Example: Phase 2 Product Discovery
cannot start until Phase 1 Market Research is complete and Approved.

---

## Change Log

Append one line per completed task. Newest at top.

- 2026-07-09 | Owner (Bhajan Lal) + Development (Claude) | **US-D2 (#115) — entity map registry + startup self-check.** Added the mapping layer the Dapper kernel reads to generate SQL: `[Table]/[Column]/[NotMapped]/[ConcurrencyToken]` attributes, `EntityMap`/`ColumnMap`, `IEntityMapRegistry`+`EntityMapRegistry` (convention: every public readable property is a column unless `[NotMapped]`; behaviour flags `IsTenantScoped`/`IsSoftDeletable`/`IsEffectiveDated` derived from SharedKernel marker interfaces; cached), and `EntityMapValidator` (fails startup if any table lacks the 7 mandatory columns, or a tenant-scoped/effective-dated entity lacks its required columns — aggregates all problems in one boot). New `HRMS.Platform.Data.Tests` project. Build 0/0; 21 tests pass (9 arch + 12 mapping). Startup DI wiring is deferred to US-D10 (`AddPlatformData`) | Status: US-D2 complete (PR pending owner review); next is US-D3 (SQL builder)
- 2026-07-09 | Owner (Bhajan Lal) + Development (Claude) | **Merged US-D1 (PR #128) — Dapper kernel scaffold.** Created `HRMS.Platform.Data` (Dapper 2.1.79, Microsoft.Data.SqlClient 7.0.2, `PlatformDataAssembly` anchor); adopted Central Package Management (`Directory.Packages.props`) + repo `src/nuget.config` (single mapped nuget.org source, fixes NU1507 under CPM); added `DataAccessBoundaryTests` (only `HRMS.Platform.Data` may reference Dapper/SqlClient; no assembly may reference EF Core). Also resolved a `main`→`development` realignment conflict (PR #127 merged; `main` is again an ancestor of `development`). Board: US-D1 (#114) Done (Estimate 4h / Actual 4h / 3 SP) | Status: US-D1 complete; US-D2 next

- 2026-07-09 | Owner (Bhajan Lal) + Development (Claude) | **Merged US-D0 (PR #126) → ADR-037 Approved.** Owner approved the EF→Dapper switch by merging PR #126; flipped ADR-037 `Status: Proposed → Approved (2026-07-09)`. Also merged the Feature #5 promotion PR #102 (`development`→`main`). FR-DATA kernel code (US-D1 onward) is now unblocked. Board: US-D0 (#113) Done (Estimate 6h / Actual 6h / 5 SP); realigned `development` with `main` after the promotion | Status: ADR-037 Approved; US-D1 (#114, scaffold `HRMS.Platform.Data`) is next
- 2026-07-09 | Development (Claude) | **Data-access strategy change to Dapper.** Owner decided to standardize on Dapper (not EF Core) with a one-time generic data-access kernel enforcing tenant isolation, soft delete, audit, and effective dating centrally, backed by SQL Server RLS. Abandoned US #7 (EF `ModuleDbContext`, never merged; issue closed NOT_PLANNED, branch deleted, EF removed from `src/`); Feature #5 completed on US #6 and promoted via PR #102 (`development`→`main`). Created new epic **FR-DATA — Platform Data Kernel** (#112) + 13 stories US-D0..D12 (#113–#125) + milestone. **US-D0 (docs, #113):** drafted **ADR-037 "Data Access = Dapper + DbUp"** (supersedes EF-Core mechanism in ADR-006 §3 / ADR-005 §1 and "EF Core Migrations Only" in ADR-003/ADR-002/DATABASE_STANDARDS; retains RLS + repository/UoW + all outcomes) and amended EF-Core-naming wording across ADR-002/003/005/006, TECH-TENANT-001 §7/§5/components/AC-004/AC-006, SEC-DESIGN-001 §2/§4, FEAT-TENANT-001, TEST-TENANT-001, DB-DESIGN-001/IDENTITY/PHASE-7A-STD, PRD-001, AI-OPS-001, and SharedKernel XML docs. Build green 0/0. Governing constraint honored: central predicate injection (no per-query discretion) + RLS backstop, per ADR-006's rejected "manual TenantId" alternative and SEC-DESIGN-001 §4.6 | Status: US-D0 Proposed — **owner approval required before any FR-DATA kernel code (Golden Rule 1)**
- 2026-07-09 | Owner (Bhajan Lal) + Development (Claude) | Merged PR #101 (US #6) into `development`: added `HRMS.ArchitectureTests` (NetArchTest 1.3.2, xUnit 2.9.3, Test.Sdk 18.7.0) enforcing modular-monolith boundaries (ADR-004) — `FoundationBoundaryTests` (SharedKernel dependency-free; Abstractions ⊥ Infrastructure/host; Infrastructure ⊥ host) and convention-based `ModuleBoundaryTests` (no module → another module's internals/Infrastructure; auto-activate as `HRMS.Modules.*` land); added `src/tests/Directory.Build.props` (warnings-as-errors kept, test-only analyzer rules relaxed); bumped CI `checkout@v6`/`setup-dotnet@v5` (cleared Node 20 deprecation); tests run via the existing `dotnet test HRMS.sln` step. Verified green in VS and CI on .NET 10. Board: US #6 Done (Estimate 5h / Actual 5h / 5 SP); Feature #5 stays In Progress (US #7 pending) | Status: US #6 complete; next is US #7 (schema-per-module EF base context)
- 2026-07-08 | Owner (Bhajan Lal) + Development (Claude) | Promoted Feature #2 to `main` (PR #99, `development`→`main`) and did repo housekeeping: enabled merge commits for `development`→`main` promotions (squash still enforced for US branches), then merged `main`→`development` (PR #100) so histories are reunified (`main` is now an ancestor of `development`, future promotions show clean diffs) | Status: Feature #2 on `main`; branch histories realigned
- 2026-07-08 | Owner (Bhajan Lal) + Development (Claude) | Merged PR #98 (US #4) into `development`: created the `HRMS.Api` ASP.NET Core host (.NET 10) with the `IModule` composition seam (`AddModule`/`MapEndpoints`), `ModuleRegistration` host module list (empty in S0), Swagger/OpenAPI via `Swashbuckle.AspNetCore` 10.2.3, `/health` endpoint, and `Program` exposed as `partial` for integration tests; CI green (`HRMS.Api.dll` built on net10.0). Board: US #4 Done (Estimate 5h / Actual 4h / 3 SP); **Feature #2 rolled up to Done** (stories #3+#4 complete); Epic #1 remains In Progress (features #5/#8/#10 pending). New rule: AI asks owner before each commit | Status: US #4 complete; Feature #2 done → `development`→`main` promotion due; next is US #6/#7 (architecture-boundary tests)
- 2026-07-02 | Owner (Bhajan Lal) + Development (Claude) | Merged PR #97 (US #3, first Phase 7A code) into `development`: created the .NET 10 `HRMS.sln` with the `src/foundation` building blocks — `HRMS.SharedKernel` (Entity, ITenantScopedEntity, ISoftDeletable, IEffectiveDated, Result/ResultError), `HRMS.Platform.Abstractions` (ITenantContext, IClock, IEventBus, IntegrationEvent), and `HRMS.Platform.Infrastructure` (SystemClock); added `Directory.Build.props`, `global.json`, and the CI workflow (build/test, green on .NET 10 SDK 10.0.301); renamed `building-blocks` → `foundation`; recorded owner-only PR approval rule. Board: US #3 Done, Estimate 6h / Actual 5h / 3 SP; Feature #2 and Epic #1 remain In Progress | Status: US #3 complete; next is US #4 (HRMS.Api host)
- 2026-06-28 | QA Architecture/Solution Architecture/Product Owner (Codex) | Updated and approved `TEST-EFFECTIVE-DATING-001-test-plan.md` v1.1 with enterprise test coverage for true bitemporal business-date vs system-time behavior, tenant-local/UTC and calendar boundary scenarios, optimistic concurrency, rollback and transaction recovery, supersession chains, soft delete with temporal/audit retention, bulk effective-dated operations, API contracts, event bus retries/duplicates/idempotency/exactly-once effective processing, UI timeline/compare/as-of/impact/responsive/accessibility tests, expanded negative testing, scalability and large history volume, disaster recovery/backup validation, and mandatory regression suite coverage for every new effective-dated entity | Status: TEST-EFFECTIVE-DATING-001 Approved; Effective Dating five-document documentation gate complete
- 2026-06-28 | UX/UI Architecture/Product Owner/Accessibility Review (Codex) | Updated and approved `UI-EFFECTIVE-DATING-001-screens.md` v1.1 with enterprise UX additions for Effective Date Preview, visual timeline states for Current/Future/Historical/Corrected/Superseded/Cancelled versions, real-time overlap detection, read-only immutable history, semantic status labels and color tokens, unsaved-change warnings, permission-aware disabled actions, Audit Information Drawer, Copy Previous Version and Restore as New Change, responsive behavior, bulk effective-dated operation UX, impact severity levels, persistent As-Of historical-data indicator, expanded Compare Versions View, and historical snapshot loading states | Status: UI-EFFECTIVE-DATING-001 Approved; Effective Dating test plan remains Draft
- 2026-06-28 | Database Architecture/Solution Architecture/Security Architecture (Codex) | Updated and approved `DB-DESIGN-EFFECTIVE-DATING-001.md` v1.1 with enterprise database additions for explicit `EntityBusinessKey` definition, mandatory database `CHECK` constraints, `EffectiveTo = NULL` open-ended active records, UTC system timestamps and temporal period columns, immutable supersession chain rules, soft-delete and temporal-history behavior, future bulk effective-dated operation rules, standard constraint/index naming, partitioning guidance for high-volume history, and `VersionNumber`/row-version optimistic concurrency | Status: DB-DESIGN-EFFECTIVE-DATING-001 Approved; Effective Dating UI/test documents remain Draft
- 2026-06-28 | Solution Architecture/.NET Architecture/Security Architecture (Codex) | Updated and approved `TECH-EFFECTIVE-DATING-001-technical-design.md` v1.1 with enterprise production-readiness additions for SQL Server `rowversion` optimistic concurrency, conflict rejection/retry/reconciliation behavior, chunked bulk effective-dated operations with transaction boundaries and progress tracking, DATE-based tenant-local valid-time semantics, inclusive effective-period boundaries, SQL temporal fallback providers, explain-history response contract, and outbox-backed event ordering, idempotency, retry, duplicate protection, and dead-letter handling | Status: TECH-EFFECTIVE-DATING-001 Approved; Effective Dating DB/UI/test documents remain Draft
- 2026-06-28 | Product Owner (Bhajan Lal) + Solution Architecture (Codex) | Updated and approved `FEAT-EFFECTIVE-DATING-001-business-requirements.md` v1.1 with platform-level standards for `EffectiveTo = NULL` open-ended records, single-active open-period control, automatic closure of prior open records, effective-date validation, tenant-local effective dates with UTC system timestamps, future bulk effective-dated operation compatibility, and common `asOfDate` query semantics | Status: FEAT-EFFECTIVE-DATING-001 Approved; companion technical/database/UI/test documents remain Draft
- 2026-06-28 | Program Director (Codex) | Counted remaining Phase 7A implementation documentation using the five-doc rule per module; Phase 7A has 13 module groups, 2 are fully Approved, and 11 remain, meaning 55 implementation documents are still not Approved; 5 Leave documents already exist as Draft and 50 documents still need to be drafted/refreshed for the remaining modules | Status: Phase 7A documentation completion count recorded
- 2026-06-28 | Program Director (Codex) | Clarified that Phase 7A roadmap/architecture is Approved, but full Phase 7A implementation documentation is not complete; only FR-015 Tenant Catalog + RLS and FR-002 Identity + RBAC/ABAC have all five required implementation documents Approved, while remaining Phase 7A modules still need their five-doc sets before coding | Status: Phase 7A docs partially complete; development allowed only for approved FR-015 and FR-002 scope
- 2026-06-28 | Program Director (Codex) | Guided the owner through planned module introduction order using the approved roadmap, PRD, and draft module backlog: Phase 7A starts with foundation modules, then Core HR/Leave/Attendance/Payroll/Reports; Phase 7B adds customer setup and service experience; Phase 7C adds intelligence/reporting/reliability; Phase 7D adds talent suite; Phase 7E adds workforce operations; later phases add enterprise ecosystem modules | Status: Module development order clarified
- 2026-06-28 | Program Director (Codex) | Clarified the official development phases from the approved PRD and roadmap: Phase 7A foundation/core operations first, Phase 7B deployment/customer-experience hardening, Phase 7C intelligence/reporting/reliability, Phase 7D talent-suite expansion, Phase 7E workforce/finance-adjacent operations, and later ecosystem/enterprise expansion; reiterated that each module still requires five Approved docs before build | Status: Development phase explanation complete
- 2026-06-28 | Program Director (Codex) | Reviewed Phase 7 development readiness after Identity database amendment; confirmed FR-015 Tenant Catalog + RLS and FR-002 Identity + RBAC/ABAC each have all five required documents Approved and can move into implementation planning, while Leave remains locked because its five-doc set is still Draft; noted remaining non-blocking/backlog documentation items: Phase 1 refresh review Draft, ADR-036 reserved for cross-currency, ADR-012-026/+028/+029 not started, and module backlog Draft | Status: Development may start only for approved foundation scope: FR-015 and FR-002
- 2026-06-28 | Owner (Bhajan Lal) + Database/Security Documentation (Codex) | Updated and re-approved `DB-DESIGN-IDENTITY-001.md` v1.2 with enterprise identity database enhancements: `security.BreakGlassAccess`, `security.BreakGlassSession`, `security.PasswordPolicy`, `security.PasswordHistory`, `security.AuthSecurityEvent`, enhanced `security.Session` device/security fields, and effective dating for `security.Role`, `security.RolePermission`, `security.AbacPolicy`, and password policy governance; added acceptance criteria and official SQL Server/NIST/OWASP/Microsoft references validated 2026-06-28 | Status: Identity Database Design Approved; Identity + RBAC/ABAC five-document set remains Approved
- 2026-06-28 | Owner (Bhajan Lal) + QA/Security Documentation (Codex) | Rebuilt and approved `TEST-IDENTITY-001-test-plan.md` with owner-recommended enterprise scenarios for break-glass emergency access, distributed session/token revocation, authentication attack testing, high availability/failover, audit/compliance/traceability, UI, performance, and automation; approved the full Identity + RBAC/ABAC five-doc set: `FEAT-IDENTITY-001-business-requirements.md`, `TECH-IDENTITY-001-technical-design.md`, `DB-DESIGN-IDENTITY-001.md`, `UI-IDENTITY-001-screens.md`, and `TEST-IDENTITY-001-test-plan.md` | Status: Identity + RBAC/ABAC documentation gate complete
- 2026-06-28 | UI/Security Documentation (Codex) | Updated `UI-IDENTITY-001-screens.md` with owner-recommended enterprise UI enhancements: Break Glass Emergency Login, Active Sessions and Device Management, complete Password and Account Recovery, Adaptive Risk-Based MFA UX, Security Dashboard and Login History; added acceptance criteria and official WCAG/OWASP/Microsoft references validated 2026-06-28 | Status: UI Design Review; Identity test plan still Draft
- 2026-06-28 | Security/.NET Architecture Documentation (Codex) | Updated `TECH-IDENTITY-001-technical-design.md` with owner-recommended enterprise technical enhancements: Break Glass Authentication Flow, authentication/authorization sequence diagrams, JWT signing and key-management strategy, distributed session and token revocation architecture, and authorization decision traceability; added acceptance criteria and official RFC/OpenID/NIST/OWASP/Microsoft references validated 2026-06-28 | Status: Technical Design Review; Identity UI/test docs still Draft
- 2026-06-28 | Product/Security Documentation (Codex) | Updated `FEAT-IDENTITY-001-business-requirements.md` with owner-recommended enterprise identity enhancements: Break Glass Emergency Access, Enterprise Password Policy, Device and Session Management, Adaptive Risk-Based MFA, and Account Lockout/Brute-Force Protection; added acceptance criteria and official NIST/OWASP/Microsoft references validated 2026-06-28 | Status: Business Requirements Review; Identity technical/UI/test docs still Draft
- 2026-06-27 | Program Director (Codex) | Checked next Phase 7A readiness step after Tenant Catalog + RLS approval; confirmed the next required approval package is Identity + RBAC/ABAC with `DB-DESIGN-IDENTITY-001.md` already Approved and four companion docs still Draft: `FEAT-IDENTITY-001-business-requirements.md`, `TECH-IDENTITY-001-technical-design.md`, `UI-IDENTITY-001-screens.md`, and `TEST-IDENTITY-001-test-plan.md` | Status: Next action routed to Identity + RBAC/ABAC document refresh/review
- 2026-06-27 | Owner (Bhajan Lal) + Program Director (Codex) | Approved the four remaining Tenant Catalog + RLS companion docs: `FEAT-TENANT-001-business-requirements.md`, `TECH-TENANT-001-technical-design.md`, `UI-TENANT-001-screens.md`, and `TEST-TENANT-001-test-plan.md`; together with already-approved `DB-DESIGN-TENANT-001.md`, FR-015 now has all five required documents Approved | Status: Tenant Catalog + RLS documentation gate complete; Identity + RBAC/ABAC docs next
- 2026-06-27 | Program Director/Solution Architecture/UI/QA (Codex) | Refreshed the four remaining Tenant Catalog + RLS companion docs to enterprise Review standard: `FEAT-TENANT-001-business-requirements.md`, `TECH-TENANT-001-technical-design.md`, `UI-TENANT-001-screens.md`, and `TEST-TENANT-001-test-plan.md`; aligned them with approved ADR-005/006, DB-DESIGN-TENANT-001, SEC-DESIGN-001, and current Microsoft SQL Server RLS/session context, EF Core query filter, Azure multitenancy, OWASP BOLA, NIST Zero Trust, and WCAG references | Status: FR-015 DB design Approved; four companion docs Review ready for owner approval
- 2026-06-27 | Owner (Bhajan Lal) + Program Director (Codex) | Approved the AI implementation five-document set: `FEAT-AI-001-business-requirements.md`, `TECH-AI-001-ai-platform-technical-design.md`, `DB-DESIGN-AI-001-ai-platform.md`, `UI-AI-001-screens.md`, and `TEST-AI-001-test-plan.md`; checked remaining documentation before database work and confirmed AI database design is approved, while broader platform database implementation is still blocked by Draft companion docs for Tenant Catalog + RLS and Identity + RBAC/ABAC | Status: AI documentation gate complete; next review is Tenant Catalog + RLS remaining docs
- 2026-06-27 | Owner (Bhajan Lal) + API Governance/Solution Architecture/DB/UI/QA (Codex) | Added owner-requested API enhancements to `API-SPEC-002-ai-platform-v1.md`, `OPENAPI-002-ai-platform-v1.yaml`, and `PHASE-6D-REVIEW-001-ai-openapi-package.md`: SSE streaming AI responses, batch AI operations, standardized rate-limit/retry headers, API versioning/deprecation policy, and bulk knowledge operations; approved all three Phase 6D API/OpenAPI docs; drafted the AI implementation five-document set: `FEAT-AI-001-business-requirements.md`, `TECH-AI-001-ai-platform-technical-design.md`, `DB-DESIGN-AI-001-ai-platform.md`, `UI-AI-001-screens.md`, and `TEST-AI-001-test-plan.md`; web research used OpenAPI, WHATWG SSE, OWASP API/GenAI, NIST AI RMF, WCAG, SQL Server RLS, Qdrant, and Redis sources | Status: AI API/OpenAPI package Approved; five implementation docs Draft ready for owner and specialist review
- 2026-06-27 | Owner (Bhajan Lal) + API Governance (Codex) | Approved `ADR-022-data-retention-archival-legal-hold-deletion.md` and `AI-DR-001-disaster-recovery-and-exercise-plan.md`; created the Phase 6D AI API/OpenAPI package: `API-SPEC-002-ai-platform-v1.md`, `OPENAPI-002-ai-platform-v1.yaml` with 21 AI API paths, and `PHASE-6D-REVIEW-001-ai-openapi-package.md`; web research used OpenAPI 3.0.3, OWASP API Security Top 10 2023, RFC 9457, and RFC 9562 | Status: ADR-022 and AI-DR-001 Approved; AI API/OpenAPI package Draft ready for review
- 2026-06-27 | Owner (Bhajan Lal) + Data Governance/Operations/Security (Codex) | Approved `SEC-AI-001-ai-security-extension.md`; drafted `ADR-022-data-retention-archival-legal-hold-deletion.md` with governed retention/legal-hold/deletion/tombstone/offboarding/restore-reconciliation controls and 15 acceptance criteria; drafted `AI-DR-001-disaster-recovery-and-exercise-plan.md` with AI recovery objectives, backup/restore design, Qdrant/Redis/event/provider recovery, DR exercises, evidence manifests, and 15 acceptance criteria; web research used DPDP, GDPR, NIST Privacy/800-88/800-34/800-61, Microsoft SQL/Azure Storage, Qdrant, Redis, and RabbitMQ sources | Status: SEC-AI-001 Approved; ADR-022 and AI-DR-001 Draft ready for review
- 2026-06-27 | Security Architect (Codex) | Created `SEC-AI-001-ai-security-extension.md` as a 30-section enterprise AI security Draft with 35 acceptance criteria covering prompt injection, RAG/vector security, ingestion poisoning, read-only tools, sensitive-data controls, memory/cache security, provider/model security, output guardrails, cost abuse, audit/telemetry, infrastructure, secure SDLC, incident response, employment-risk controls, OpenAPI security, and red-team testing; web research used OWASP GenAI Top 10 2025, NIST AI RMF/SSDF/incident guidance, NCSC secure AI guidance, Qdrant, Redis, and EU AI Act sources | Status: Draft ready for owner and specialist review
- 2026-06-27 | Owner (Bhajan Lal) + Program Director (Codex) | Approved `AI-OPS-001-enterprise-ai-operations.md` v1.1, moved it to the approved document set, and routed the next Phase 6C work to `SEC-AI-001-ai-security-extension.md` owned by the Security Architect | Status: AI-OPS-001 Approved; AI Security Extension next
- 2026-06-27 | Owner (Bhajan Lal) + Platform/Operations Architecture (Codex) | Updated `AI-OPS-001-enterprise-ai-operations.md` to v1.1 with owner-recommended enhancements: AI model lifecycle stages and bundle governance, Business KPI Monitoring, AI Governance Board workflow/cadence/emergency approvals, Runbook Reference Matrix aligned to AI-RUN-001 through AI-RUN-018, Future AI Agent Operations reserved section, ORR additions, and 6 new acceptance criteria | Status: Draft v1.1 ready for owner approval
- 2026-06-25 | Platform/Operations Architecture (Codex) | Corrected the previously empty/nonexistent next-document target and created `AI-OPS-001-enterprise-ai-operations.md` using current Google SRE, OpenTelemetry, Prometheus, NIST incident-response, Qdrant, Redis, OWASP, and FinOps guidance; added 33 operational sections, 18 production runbooks, an Operational Readiness Review gate, service ownership/SLO/error-budget/incident/degraded-mode/release/provider/vector/cache/memory/ingestion/evaluation/cost/security/DR/deletion controls, and 31 acceptance criteria | Status: Draft ready for owner and specialist review
- 2026-06-25 | Codex Program Director | Confirmed the Phase 6C sequence after Phase 6B approval: the next document is `docs/15-ai/AI-OPS-001-enterprise-ai-operations.md`, owned by the Platform/Operations Architect; AI Security Extension and retention/DR alignment remain gated behind its review/approval | Status: Routing confirmed
- 2026-06-25 | Owner (Bhajan Lal) + Solution Architect (Codex) | Added all seven owner-approved enhancements to ADR-035: cache effectiveness metrics, cache-policy review/expiry, governed warm-up, cache-quality drift signals, emergency global/tenant/use-case disablement, Redis Sentinel/Cluster HA and persistence/RPO/RTO strategy, and namespace rotation evidence; expanded the document to 41 acceptance criteria and approved ADR-035 | Status: ADR-035 Approved; Phase 6B complete; Phase 6C AI Operations Handbook next
- 2026-06-25 | Solution Architect (Codex) | Researched current Redis/RedisVL semantic caching, vector filtering, TTL and ACL guidance plus Anthropic/OpenAI/Google provider prompt caches, NIST GenAI, and OWASP injection risk; drafted ADR-035 Enterprise Semantic and Retrieval Cache Architecture with 29 governed decisions and 34 acceptance criteria covering Redis-first self-hosting, Qdrant boundary, eligibility, tenant/security partitioning, HMAC keys, per-hit reauthorization, invalidation, poisoning, provider caches, observability, deletion, recovery, APIs, and operations | Status: Draft ready for owner and specialist review; 9 external references validated 2026-06-25
- 2026-06-25 | Owner (Bhajan Lal) + Solution Architect (Codex) | Added all six owner-approved enhancements to ADR-034: explicit hallucination metrics, approval-expiry reason, dataset review/expiry, provider behavior drift, accountable risk owner, and human-review agreement/consistency governance; expanded the document to 38 acceptance criteria and approved ADR-034 | Status: ADR-034 Approved; ADR-035 unblocked
- 2026-06-25 | Solution Architect (Codex) | Researched current NIST AI RMF/GenAI Profile, ISO/IEC 42001, OWASP GenAI, EU AI Act, RAGAS, and official provider evaluation guidance; drafted ADR-034 Enterprise AI and RAG Evaluation Framework with 29 governed decisions and 32 acceptance criteria covering immutable system bundles, sealed benchmarks, statistical and human evaluation, employment fairness/oversight, security/privacy, promotion/canary/rollback, drift, incidents, APIs, and audit | Status: Draft ready for owner and specialist review; external references validated 2026-06-25
- 2026-06-25 | Owner (Bhajan Lal) + Solution Architect (Codex) | Added all seven owner-approved enhancements to ADR-033: reservation reason, forecast-confidence score, trial/feature expiry, controlled emergency override, rebuildable budget snapshot, tenant-specific commercial pricing, and ADR-036 exchange-rate governance; expanded APIs/events/controls to 31 acceptance criteria and approved ADR-033 | Status: ADR-033 Approved; ADR-034 next
- 2026-06-25 | Solution Architect (Codex) | Drafted ADR-033 AI Cost Governance with explicit paid-service activation, provider-neutral usage ledger, effective-dated pricing, atomic budget reservation, configurable quotas and hard limits, forecasting, showback, reconciliation, secure APIs/events, failure controls, and 22 acceptance criteria | Status: Draft ready for owner and specialist review
- 2026-06-24 | Codex Program Director | Audited documentation readiness before first development: 14 Phase 6 documents remain (including ADR-022/023 dependencies) plus 4 unapproved Tenant Catalog/RLS documents for the first feature, for a total of 18 required document approvals before coding starts | Status: Readiness count complete; ADR-033 next
- 2026-06-24 | Owner (Bhajan Lal) + Solution Architect (Codex) | Added all seven owner-approved enhancements to ADR-032: future Workspace Memory, summary turn lineage, summary quality metadata, TenantRoleMatrixChanged invalidation, conversation reset API, enforced purpose boundaries, and configurable 30/60/90-day retention; approved ADR-032 and advanced Phase 6B to ADR-033 | Status: ADR-032 Approved; ADR-033 next
- 2026-06-23 | Codex | Explained the attached Headland DMS Assessment-ingestion failure investigation in Hindi, including the validation/population/import flow, misleading completion counts, database evidence, root cause, and the two identified defects; omitted exposed credentials from the explanation | Status: Complete
- 2026-06-23 | Solution Architect (Agent 6 / Codex) | Drafted ADR-032 Conversation Memory Strategy with SessionOnly default, Redis short-term memory, opt-in encrypted SQL summaries, no Qdrant conversation embeddings or long-term profiles, per-turn authorization, event invalidation, safe summarization, context budgets, retention/deletion/legal hold, APIs, stateless fallback, and acceptance criteria | Status: Draft ready for review
- 2026-06-23 | Owner (Bhajan Lal) + Codex Program Director | Approved ADR-031 AI Observability and Telemetry and advanced the sequential Phase 6B gate to ADR-032 Conversation Memory Strategy | Status: ADR-031 Approved; ADR-032 next
- 2026-06-23 | Solution Architect (Agent 6 / Codex) | Drafted ADR-031 AI Observability and Telemetry with OpenTelemetry, self-hosted Prometheus/Grafana/Loki/Tempo/Alertmanager, Qdrant monitoring, privacy/cardinality controls, SLO/SLA evidence, dashboards, alerts, runbooks, sampling/retention, backend portability, and acceptance criteria; corrected stale AI ADR cross-references | Status: Draft ready for review
- 2026-06-23 | Codex Program Director | Explained the Product Owner's role in Phase 6B and routed the immediate work to Solution Architect drafting ADR-031 AI Observability and Telemetry | Status: Routing clarified
- 2026-06-23 | Owner (Bhajan Lal) + Codex Program Director | Approved ADR-019 Enterprise AI/RAG Platform Architecture, completed the Phase 6A architecture gate, and unblocked Phase 6B beginning with ADR-031 AI Observability and Telemetry | Status: ADR-019 Approved; Phase 6A complete
- 2026-06-22 | Owner (Bhajan Lal) + Codex Program Director | Approved ADR-030 Enterprise Vector Store Strategy with Qdrant first and Azure AI Search optional; corrected AI ADR references to approved Strategy v2.1; routed the remaining Phase 6A gate to ADR-019 review | Status: ADR-030 Approved; ADR-019 Proposed
- 2026-06-22 | Owner (Bhajan Lal) + Solution Architect (Codex) | Reversed the initial vector-store order: selected local/self-hosted Qdrant first to avoid paid managed search during initial development; retained Azure AI Search as an optional `IVectorStore` adapter; updated AI Strategy to approved v2.1, revised ADR-030, added registry-driven VectorStore provider type, and removed the closed provider-category OpenAPI enum | Status: Owner decision recorded; ADR-030 remains Draft for security review
- 2026-06-22 | Solution Architect (Agent 6 / Codex) | Refreshed ADR-019 as the enterprise AI/RAG umbrella architecture and created ADR-030 Vector Store Strategy with hard tenant partitioning, Azure AI Search first adapter, Qdrant portability path, immutable index lifecycle, DR, cost, migration, and acceptance gates | Status: ADR-019 Proposed; ADR-030 Draft; Phase 6A review ready
- 2026-06-22 | Owner (Bhajan Lal) + Codex Program Director | Approved AI Strategy v2.0; retained Phase 6 as open and routed the next gated work to refreshed ADR-019 plus ADR-030 Vector Store Strategy | Status: Strategy Approved; Phase 6A pending
- 2026-06-22 | Codex Documentation QA | Verified AI Strategy v2.0 against all ten enterprise-hardening areas, security/API/database standards, ADR numbering, and Phase 6 hard gates | Status: Draft verified
- 2026-06-22 | Codex Prompt/Context Architecture | Updated AI-STRATEGY-001 to v2.0 Draft from the Phase 6 enterprise-hardening review; added vector-store recommendation, memory/cache, observability, cost, evaluation, confidence, AIOps, security, AI API requirements, acceptance criteria, and hard-gated Phase 6 delivery; preserved ADR-028/029 reservations and assigned AI ADR-030 through ADR-035 | Status: Draft updated
- 2026-06-22 | Owner (Bhajan Lal) + Codex API Governance | Approved the Phase 5 foundational API specification, machine-readable OpenAPI YAML, and Phase 5 review checkpoint; advanced the current gate to Phase 6 AI Strategy | Gate 5: Approved
- 2026-06-18 | Codex API Governance | Listed Phase 5 review documents for owner: foundational API spec, OpenAPI YAML, and Phase 5 review checklist | Status: Complete
- 2026-06-18 | Codex API Governance | Started Phase 5 API Design; refreshed foundational API spec to v1.1 Review, created machine-readable OpenAPI YAML with 44 paths/53 operations, added provider-management APIs aligned to ADR-027, and created Phase 5 review checklist | Status: Review package ready
- 2026-06-18 | Owner (Bhajan Lal) + Codex UI Review | Closed Phase 4 UX/UI alignment checkpoint; refreshed DESIGN-SPEC-002 to v2.1 with Provider Management UX aligned to ADR-027; created Phase 4 alignment review and moved current gate to Phase 5 OpenAPI/API Design | Gate 4: Approved
- 2026-06-18 | Codex Program Director | Corrected phase routing inconsistency: after Phase 3 approval, current gate is Phase 4 UX/UI alignment checkpoint, not Phase 5; Phase 5 OpenAPI starts only after the UI package is confirmed against the refreshed architecture | Status: Routing corrected
- 2026-06-18 | Owner (Bhajan Lal) + Codex Final Review | Approved Phase 3 architecture package after final review; corrected provider DB impact, event/outbox DB design, tenant-scoped workflow/identity tables, and provider-boundary security notes; current gate moved to Phase 5 API Design | Gate 3: Approved
- 2026-06-17 | Codex Program Director | Identified the next owner approval package for Phase 3: architecture baseline, provider abstraction, key ADRs, database foundations, tenant/identity database designs, and security threat model must be reviewed before API/design-development work advances | Status: Routing complete
- 2026-06-17 | Codex | Corrected related docs to use the full Phase 7A foundation group before business modules: Tenant Catalog + RLS, Identity/RBAC/ABAC, Effective Dating, Audit/Time Machine, Event Bus, Rule Engine, Workflow Engine, and Configuration-as-Data; updated PRD, roadmap, architecture review, market research, positioning hypothesis, module backlog, and expert assessment | Status: Docs updated
- 2026-06-17 | Codex Architecture Review | Confirmed that the highest-ROI Phase 7A architecture foundations are Tenant Catalog + RLS, Identity/RBAC/ABAC, Effective Dating, Rule Engine, Workflow Engine, Event Bus, Audit/Time Machine, and Configuration-as-Data; clarified modules can come later but these foundations are costly to retrofit | Status: Clarification complete
- 2026-06-17 | Codex Architecture Review | Reviewed ARCH-REVIEW-001 and created expert assessment; conclusion: architecture direction is strong but document is not approval-ready until ADR statuses, Phase 7A baseline, provider abstraction, tenant-isolation traceability, AI provider wording, DB and security dependencies are refreshed | Status: Draft review created
- 2026-06-17 | Codex | Identified Phase 3 next work: Solution Architect must refresh architecture baseline and coordinate DB, security, integration/provider abstraction, and key ADR approvals before Phase 5 OpenAPI work proceeds | Status: Routing complete
- 2026-06-17 | Owner (Bhajan Lal) + Codex | Marked Phase 2 PRD — Platform Phased Delivery and Roadmap — Phased Delivery as Approved; Phase 2 refresh gate is now approved and current gate moved to Phase 3 architecture refresh | Gate 2 refresh: Approved
- 2026-06-17 | Codex | Clarified that FR numbers are stable requirement identifiers, not implementation sequence; confirmed FR-015 Tenant Catalog + RLS is first in the build sequence because it gates tenant-safe development | Status: PRD/Roadmap clarification added
- 2026-06-17 | Codex | Routed the next step after Phase 2 approval: Phase 3 architecture refresh/approval must absorb the approved PRD, roadmap, positioning, module priorities, extension rules, DB/security/integration impacts, and ADR updates before API/development proceeds | Status: Routing complete
- 2026-06-17 | Owner (Bhajan Lal) + Codex | Marked refreshed Phase 1 market research, competitor gap analysis, and Product Owner positioning hypothesis as Approved; Phase 1 refresh gate is now approved | Gate 1 refresh: Approved
- 2026-06-17 | Codex | Reviewed current phase gate status and identified the next action: owner review/approval of refreshed Phase 1 research and positioning documents before Product Discovery/API work proceeds further | Status: Routing complete
- 2026-06-17 | Codex | Created dedicated Product Owner strategic positioning hypothesis research document and marked the positioning hypothesis as HIGH IMPORTANCE in Phase 1 market research; added buyer-validation rules and phase-priority implications | Status: Draft/Review docs updated
- 2026-06-16 | Codex | Added missing HRMS modules/features to research, PRD, roadmap, architecture, and product backlog; organized modules into Phase 7A/7B/7C/7D/7E/later phases; added open-for-extension/closed-for-core-change module ingestion rules | Status: Review/Draft docs updated
- 2026-06-16 | Codex | Explained SMB meaning in the HRMS market context and how it maps to employee-size segments | Status: Complete
- 2026-06-16 | Codex Review Agent | Created Phase 1 market research refresh review comparing HRMS vendor portals and customer-review themes against current docs; identified missing modules, customer happiness/irritation patterns, and feature refinements | Status: Draft review created
- 2026-06-16 | Codex | Explained OpenAPI documentation meaning with HRMS API examples and why it is mandatory before API development | Status: Complete
- 2026-06-16 | Codex | Explained event-driven architecture meaning with HRMS examples and why it matters for modules like attendance, payroll, notifications, audit, and reports | Status: Complete
- 2026-06-16 | Codex | Removed old launch-scope wording from documents, renamed PRD/roadmap to phased-delivery files, converted release labels to Phase 7A/7B/7C, and added explicit sequential phase-gate rule | Status: Complete
- 2026-06-16 | Codex | Explained documented project phases, expected deliverables per phase, and the practical difference between phase and stage | Status: Complete
- 2026-06-16 | Codex Review Agent | Reviewed coding-readiness gates and identified remaining Draft/Proposed documents required before development can start | Status: Review complete
- 2026-06-16 | Codex | Explained the project review in Hindi with practical feature examples for HRMS capabilities, architecture direction, status, and next steps | Status: Complete
- 2026-06-16 | Codex Review Agent | Reviewed project memory and documentation folders; produced a concise project brief covering vision, differentiators, architecture, current phase, risks, and next steps | Status: Review complete
- 2026-06-15 | Owner (Bhajan Lal) | **Strategy decision: full-product launch with phased delivery** — build the full application, then enter the market. Reframing PRD/roadmap from limited launch scope to full-product phased scope; deferred modules to be re-scoped per owner's chosen launch scope | Decision recorded
- 2026-06-15 | Solution Architect | Provider-agnostic architecture review → ARCH-REVIEW-002 (storage/cache/messaging/notification/identity/search/BI abstraction; per-tenant TenantProviderConfig; health/fallback; lock-in risks) + ADR-027 umbrella. Key stance: design seams now, build adapters on demand (Azure defaults in Phase 7A) | Status: Draft / ADR Proposed
- 2026-06-14 | Cross-agent (PO/Arch/DBA/UI/QA) | **S1 documentation complete** — full 5-doc sets for FR-015 (Tenant Catalog + RLS) and FR-002 (Identity + RBAC/ABAC), the two foundations first to build per ROADMAP critical path | Status: Draft (10 docs) — S1 is now development-ready pending your approval
- 2026-06-14 | Cross-agent (PO/Arch/DBA/UI/QA) | **Leave feature 5-doc set** (Rule 1, dev-ready): Business Req, Technical Design, DB Design (ledger-based balances), UI Design, Test Cases — reuses Workflow/Rules/effective-dating/events | Status: Draft (all 5) — first development-ready feature
- 2026-06-14 | Owner (Bhajan Lal) | New requirement: AI must be **model-switchable** (Claude/OpenAI/Gemini), **admin-only** setting → updated ADR-019 + AI-STRATEGY §8 (ILlmProvider, model registry, AI.ManageModels, BYO keys) + prototype "AI Settings" screen | Status: Draft
- 2026-06-14 | Prompt/Context Engineer | AI strategy → docs/15-ai/AI-STRATEGY-001 (RAG architecture, per-tenant isolation, prompt library, guardrails, eval) + ADR-019 (multi-provider LLM, default Claude Opus 4.8/Haiku 4.5, per-tenant vector store, RBAC/ABAC-scoped, grounded+cited) | Status: Draft / ADR Proposed
- 2026-06-14 | .NET Architect | Foundational API spec → docs/08-api-specs/API-SPEC-001 (auth, employees [effective-dated], leave [rules+workflow], workflow/approvals [delegation/SLA], search/notif/AI); envelope, pagination, idempotency, tenant+RBAC/ABAC per API_STANDARDS | Status: Draft
- 2026-06-14 | Owner (Bhajan Lal) | **Approved UI** — DESIGN-SYSTEM-001, SCREENS-001, DESIGN-SPEC-002 + prototype; Phase 4 UI sign-off gate satisfied; advanced to Phase 5 | Gate 4 (UI): Approved
- 2026-06-14 | UX/UI Architect | Prototype v2.1 — configurability proof: Configuration Center, Form Builder, Role/Permission Builder, Tenant Admin, Feature Management, Integration Hub, Navigation Builder, White-Label, Search results, Widget Catalog; connected Workflow Studio execution paths; interactive Org tree + detail; AI Copilot recommended actions. DESIGN-SPEC-002 §21 added (no future modules) | Status: Draft — awaiting your visual sign-off
- 2026-06-14 | UX/UI Architect | Prototype v2 — AI-native People Ops Platform: metadata-driven role dashboards + dynamic nav, ⌘K command center, persistent AI, density modes, dark mode, Workflow Studio 2.0, Rule Builder, Audit/Time-Machine, Compliance & Payroll command centers, Activity, Org chart. Authored DESIGN-SPEC-002 (all 20 areas + component hierarchy) | Status: Draft — awaiting your visual sign-off
- 2026-06-14 | UI/Figma Designer | Owner rejected flat SVGs (theme/positioning/appeal). Chose **Modern & Friendly** direction + interactive prototype → built docs/07-ui-ux/prototype/index.html (dashboard, people, leave, approvals, workflow studio); updated DESIGN-SYSTEM tokens | Status: Superseded by v2
- 2026-06-14 | UI/Figma Designer | Created viewable SVG visual mockups for 5 screens → docs/07-ui-ux/figma/; added **UI Design Sign-off gate** (visual designs must be approved before implementation) | Status: Superseded by prototype
- 2026-06-14 | UI Architect / UX | Design system (DESIGN-SYSTEM-001) + 5 foundational screen specs (SCREENS-001: login/tenant, directory, apply-leave, approvals inbox, Workflow Studio) → docs/07-ui-ux | Status: Draft
- 2026-06-14 | Security Architect | Security design & threat model → docs/12-security/SEC-DESIGN-001 (STRIDE, tenant isolation defense-in-depth, OWASP, data protection, DPDP) | Status: Draft
- 2026-06-14 | Solution Architect | Authored ADR-006 (tenant context/data-access), ADR-008 (identity/SSO/SCIM/RBAC+ABAC), ADR-009 (event backbone + outbox) | Status: Proposed
- 2026-06-14 | Database Architect | Foundational DB design → docs/06-database/DB-DESIGN-001 (catalog, security, effective-dated core, workflow, rules, audit schemas) | Status: Draft
- 2026-06-14 | Project Manager | Phased delivery roadmap → docs/04-roadmap/ROADMAP-001 (Phase 7A/7B/7C/later phases; 10-sprint plan; critical path FR-015→002→013/007→006) | Status: Draft
- 2026-06-14 | Owner (Bhajan Lal) | Approved PRD v1.1 + ADR-005/007/010/011; advanced to Phase 3 | Gate 2: Approved
- 2026-06-14 | Solution Architect | Authored 4 foundational ADRs (005 multi-tenancy, 007 effective-dating, 010 workflow engine, 011 rule engine) | Status: Approved
- 2026-06-14 | Product Owner | PRD v1.1 — pulled 3 foundations into Phase 7A (FR-013 Rule Engine, FR-014 effective-dating, FR-015 tenant catalog/RLS); added delegation to FR-007 | Status: Draft
- 2026-06-14 | Solution Architect (+panel) | Drafted Architecture & Product Review → docs/05-architecture/ARCH-REVIEW-001 (Workflow + Rule engine designs, multi-tenant model, 60 missed reqs, 80 risks, 22 ADRs to write, MoSCoW re-scope) | Status: Draft. Key call: move Rule Engine + effective-dating + tenant catalog/RLS INTO Phase 7A
- 2026-06-14 | Product Owner | Drafted phased-delivery PRD → docs/02-product-requirements/PRD-001-platform-phased-delivery.md (12 FRs; Phase 7A anchored on Workflow Studio + payroll/compliance + reliability) | Status: Draft
- 2026-06-14 | Owner (Bhajan Lal) | Approved Phase 1 docs (competitor analysis + gap analysis); advanced to Phase 2 | Gate 1: Approved
- 2026-06-14 | Competitor Gap Analyst | Created gap analysis → docs/03-gap-analysis/competitor-gap-analysis.md; validated §9 (A & L confirmed, N refuted, C/B reframed) | Status: Draft
- 2026-06-14 | HR Domain Expert | v1.2 — web-verified module coverage matrix, pricing, sources; nuanced AI claims (enterprise AI now exists) | Status: Draft
- 2026-06-14 | HR Domain Expert | v1.1 — added §9 Hidden Gaps (15 unsolved gaps A–O) + §10 Roadmap Positioning to competitor analysis | Status: Draft (gap hypotheses to validate in 03-gap-analysis)
- 2026-06-14 | HR Domain Expert | Drafted India-first competitor market analysis → docs/01-market-research/competitor-analysis-india.md | Status: Draft (needs web verification + your approval)
- 2026-06-14 | Setup | Scaffolded CLAUDE.md, agents, commands, ADRs, numbered docs tree | Status: Approved
- 2026-06-28 | Codex Documentation Architecture | Drafted/refreshed the remaining Phase 7A implementation documentation set using approved architecture decisions plus current market/web references: created 50 new documents and refreshed the existing 5 Leave documents so Effective Dating, Audit/Time Machine, Event Bus, Rule Engine, Workflow Studio, Configuration-as-Data, Core HR/ESS, Leave, Attendance + first connector, Payroll + India compliance, and Standard Reports each have Business Requirements, Technical Design, Database Design, UI Design, and Test Plan documents; all documents include tenant isolation, RBAC/ABAC, audit, effective dating, event-driven behavior, configuration-as-data, OpenAPI expectations, acceptance criteria, and external references validated 2026-06-28 | Status: 55 Phase 7A docs Draft and ready for owner/specialist review
- 2026-06-28 | Codex Documentation Audit | Scanned `docs/` for markdown files whose `Status:` does not start with `Approved`; confirmed Effective Dating five-doc set is now Approved and identified the remaining not-approved document paths for owner review/approval | Status: Scan complete
- 2026-06-28 | Codex Documentation Review | Reviewed attached Phase 7A Documentation Review Report; confirmed its recommendations are broadly valid and enterprise-oriented, but noted current-repo mismatch: Effective Dating five-doc set is already Approved, leaving 50 Phase 7A implementation docs not approved; also noted the report's old MVP wording should be translated to phase-based validation language | Status: Review complete
- 2026-06-29 | Codex Documentation Architecture | Applied Phase 7A review recommendations by creating four shared hardening standards for API/event/NFR/runbooks, database PII classification/migration/rollback, UI accessibility/states, and test traceability/multi-tenant abuse coverage; created Phase 7A hardening backlog with module-specific recommendations; linked the 10 remaining module technical designs, 10 database designs, 10 UI designs, and 10 test plans to the new standards; updated ADR/PRD templates, module dependency map, market assumptions, and architecture assessment resolution note; verified no old launch-scope wording remains in `docs/` | Status: Draft hardening standards and backlog ready for owner/specialist review
- 2026-06-29 | Codex Program Director | Clarified why all Phase 7A documents are not automatically approved: repository constitution requires explicit human-owner approval before any Draft/Review document status can be changed to Approved | Status: Clarification complete
- 2026-06-29 | Owner (Bhajan Lal) + Codex Program Director | Owner confirmed review and approved all Phase 7A development documentation; marked 55 Phase 7A implementation documents plus 5 Phase 7A hardening standard/backlog documents as `Status: Approved`; verified 60/60 relevant Phase 7A development docs are Approved with no remaining Draft/Review status markers or old launch-scope wording in docs | Status: Phase 7A documentation approval gate complete
- 2026-06-29 | Codex Release Documentation | Created the Phase 7A Approved Development Brief PDF and presentation deck for end-user/stakeholder communication; summarized what has been approved, what will be developed, who the phase serves, the simple operating model, architecture foundations, security/quality controls, development order, out-of-scope items, and web/source credits; used web-sourced Wikimedia Commons visuals and visually verified the 8-page PDF plus 12-slide PPT preview renders | Status: Phase 7A release summary package complete
- 2026-06-29 | Codex Release Documentation | Created a detailed Phase 7A Approved AI Source Reference PDF plus matching Markdown source for AI ingestion; covered 13 approved Phase 7A module packs (65 module documents) plus 5 shared hardening documents with module conclusions, architecture, database schemas/tables, API examples, event examples, operating examples, test focus, source paths, sequencing, security/quality rules, and AI usage guidance; rendered and visually checked all 35 PDF pages, verified text extraction, and confirmed no old launch-scope wording | Status: Phase 7A AI source reference complete
- 2026-06-29 | Codex Documentation Review | Checked approved Phase 7A documents for two owner concerns: tenant child branches/branch-admin isolation and employee custom shift assignment. Found branch/location/legal-entity/department ABAC scope partially documented, but explicit parent tenant -> child branch hierarchy with complete tenant admin and branch admin data boundaries is not fully specified. Found shift/roster/workforce scheduling explicitly deferred to Phase 7E, with only calendar/attendance policy references in Phase 7A | Status: Gap confirmation complete; owner decision needed before development if either item must move into Phase 7A
- 2026-06-29 | Codex Product/Architecture Review | Recommended adding Branch / Office Hierarchy and Scoped Administration to Phase 7A and adding only a limited Shift Foundation to Phase 7A, while keeping advanced roster/workforce scheduling in a later phase. Rationale: Attendance and Payroll need shift definitions and employee shift assignment for correct late/early/overtime/night/weekly-off calculations, but full rostering is a larger workforce-planning module | Status: Recommendation recorded; awaiting owner confirmation before documentation amendments
- 2026-06-29 | Owner (Bhajan Lal) + Codex Documentation Architecture | Added owner-approved Phase 7A documentation amendments for Branch / Office Hierarchy and Scoped Administration plus Shift Foundation; created and approved the full five-document packs for both capabilities, patched PRD/roadmap/architecture and affected Tenant, Identity, Core HR, Attendance, Payroll, Reporting, market, gap-analysis, and backlog documents; regenerated the Phase 7A Approved Development Brief PDF and the Phase 7A Approved AI Source Reference PDF/Markdown to reflect 15 module packs, 75 implementation docs, and 80 total approved Phase 7A release documents; visually rendered and checked all 40 AI-source pages and all 8 brief pages | Status: Approved documentation and PDFs updated
- 2026-07-01 | Codex PDF QA | Verified `docs/11-release/PHASE-7A-approved-ai-source-reference.pdf` against the current Phase 7A approved documentation inventory: 15 module packs, 80 expected source documents, all files present, all `Status:` fields approved, no source document newer than the PDF, Branch / Office Hierarchy and Shift Foundation included, and no stale MVP/launch/13-module/65-document/60-approval wording found | Status: PDF up to date
- 2026-07-01 | Codex Architecture Clarification | Clarified that Phase 7A is designed as a modular HRMS platform where Leave, Attendance, Payroll, Core HR, Reporting, and platform foundations are separate modules/bounded contexts with their own SQL Server schemas inside one primary database, while sharing tenant isolation, RBAC/ABAC, audit, events, effective dating, workflow, rules, and configuration services | Status: Clarification complete
- 2026-07-01 | Codex Architecture Clarification | Clarified the deployment style for Phase 7A: the approved design should be treated as a modular monolith first, not pure microservices, with separate bounded modules/schemas and event/API boundaries so selected modules can be extracted into microservices later if scale, team ownership, or operational needs justify it | Status: Clarification complete
- 2026-07-01 | Codex Source Review | Reviewed the current `src/` folder structure and explained all real source/config files: solution file, SDK pinning, shared build props, SharedKernel primitives, Platform.Abstractions interfaces/events, Platform.Infrastructure clock implementation, and generated `bin/obj` folders; confirmed current source is foundation building blocks only, with business modules still to be added later | Status: Review complete
- 2026-07-02 | Codex Architecture Clarification | Explained the purpose of the `src/building-blocks` folder as shared platform foundation code for the modular monolith, clarified that it must not become a dumping ground for business logic, and documented naming alternatives such as `platform`, `shared`, `foundation`, or `libs`; recommended `src/platform` as the clearest enterprise naming option if the owner wants to rename it | Status: Clarification complete
