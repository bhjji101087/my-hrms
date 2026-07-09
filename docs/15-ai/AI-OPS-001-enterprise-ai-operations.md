# AI-OPS-001 - Enterprise AI Operations Handbook

Version: 1.1
Date: 2026-06-27
Status: Approved
Owner: Platform/Operations Architect
Reviewers: Security, Data Governance, Solution Architecture, Product/AI, HR Domain

Related approved documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md`
- `docs/16-decisions/ADR-009-event-driven-backbone.md`
- `docs/16-decisions/ADR-019-ai-rag-architecture.md`
- `docs/16-decisions/ADR-027-provider-abstraction-framework.md`
- `docs/16-decisions/ADR-030-vector-store-strategy.md`
- `docs/16-decisions/ADR-031-ai-observability-telemetry.md`
- `docs/16-decisions/ADR-032-conversation-memory-strategy.md`
- `docs/16-decisions/ADR-033-ai-cost-governance.md`
- `docs/16-decisions/ADR-034-rag-evaluation-framework.md`
- `docs/16-decisions/ADR-035-semantic-cache-architecture.md`

Required companion documents before implementation:

- `docs/12-security/SEC-AI-001-ai-security-extension.md`
- ADR-022 Data Retention, Archival, Legal Hold, and Deletion
- AI disaster-recovery design and exercise plan
- `docs/08-api-specs/API-SPEC-002-ai-platform-v1.md`
- `docs/08-api-specs/OPENAPI-002-ai-platform-v1.yaml`
- AI Business, Technical, Database, UI, and Test documents

---

# 1. Purpose

This handbook defines how the HRMS AI platform is operated safely and reliably in production.
It converts the approved AI architecture into an operating model for:

- Service ownership and on-call response.
- Service levels, error budgets, alerting, and tenant communication.
- Deployment, promotion, rollback, maintenance, and change control.
- Provider, model, prompt, Qdrant, Redis, memory, cache, evaluation, and ingestion operations.
- Capacity, cost, credentials, queues, telemetry, backup, disaster recovery, and deletion.
- Security, privacy, quality, cross-tenant, and harmful-output incidents.
- Model lifecycle, governance-board review, business KPI monitoring, and future agent operations.
- Operational readiness, exercises, evidence, and continuous improvement.

This is a production-control document. It is not a substitute for implementation designs,
OpenAPI contracts, security procedures, test plans, provider contracts, legal assessments,
or tenant-specific business-continuity requirements.

---

# 2. Scope and Operational Boundaries

The handbook covers these AI platform capabilities:

- AI gateway/orchestrator and context assembly.
- LLM, embedding, reranking, and evaluator provider adapters.
- RAG ingestion, retrieval, citations, confidence, guardrails, and read tools.
- Qdrant vector indexes and canonical-source rebuild coordination.
- Redis session memory, exact/retrieval/embedding/semantic caches, and cache controls.
- SQL Server AI configuration, audit, evaluation, cost, memory, and operational records.
- Object storage for approved source/evaluation/backup artifacts.
- Event/outbox consumers, queues, background jobs, and notification routes.
- OpenTelemetry Collector and the self-hosted Prometheus, Alertmanager, Grafana, Loki, and
  Tempo observability stack.
- Cost budgets, quotas, provider credentials, retention, deletion, and tenant offboarding.

The handbook does not authorize state-changing AI actions. Core HRMS business workflows,
authorization, tenant catalog, payroll calculation, and employment decisions remain outside
AI authority and follow their own approved operational procedures.

---

# 3. Non-Negotiable Operating Principles

1. **Safety and tenant isolation before availability.** No SLO, deadline, or cost target may
   bypass tenant context, RBAC/ABAC, grounding, citation, safety, privacy, or audit controls.
2. **No ungrounded availability fallback.** The platform does not invent an answer to avoid
   an outage response.
3. **Provider independence.** Failover and replacement use approved adapters/configuration,
   never customer-specific feature changes.
4. **Configuration as data.** SLOs, thresholds, routes, budgets, retention, and recovery
   policies are effective-dated, approved, and audited.
5. **Everything is versioned.** Production identifies the complete prompt/model/index/
   policy/cache/memory/evaluation bundle and its rollback bundle.
6. **Derived stores are rebuildable.** Qdrant indexes, Redis caches, and permitted summaries
   are reconstructed from authorized canonical sources and approved configuration.
7. **Observability is not audit.** Telemetry may be sampled; durable security, cost,
   evaluation, deletion, and business audit records use reliable stores/outbox paths.
8. **No sensitive debug by default.** Prompts, responses, employee data, secrets, retrieved
   content, and tenant identifiers are excluded from general telemetry.
9. **Explicit degraded mode.** Every dependency has a documented safe fallback, bypass, or
   feature-disable action.
10. **Evidence-based recovery.** Service is restored only after validation proves current
    authorization, isolation, integrity, quality, and data state.
11. **No automatic paid-service activation.** Capacity pressure or outage cannot silently
    enable a paid provider/managed service.
12. **Human accountability.** Models, agents, providers, and automation do not own incidents,
    accept residual risk, or approve production changes.

---

# 4. Service Catalog and Critical Dependencies

Every production component has a registered owner, support route, deployment version,
dependency map, health contract, data classification, RTO/RPO, SLOs, capacity limit,
dashboard, alerts, and runbook.

| Component | Primary responsibility | Critical dependencies | Safe degraded behavior |
|---|---|---|---|
| AI Gateway/Orchestrator | Tenant-safe request policy, routing, context, response release | Identity, tenant context, policy/config, audit | Disable AI request when authorization/policy unavailable |
| LLM adapter | Grounded generation | Provider, credentials, budget, network | Approved fallback provider/model, retrieval-only, or unavailable |
| Embedding adapter | Query/document embeddings | Provider/local model, registry | Exact cache/retrieval where permitted; pause ingestion or return unavailable |
| Reranker | Candidate ranking | Provider/local service | Approved no-rerank retrieval profile if evaluated |
| Qdrant | Tenant-partitioned vector retrieval | Network, storage, snapshots, canonical sources | Approved keyword/source navigation or unavailable; never cross-partition |
| Redis memory | Short-lived conversation continuity | Redis topology, key builder, authorization | Stateless conversation turn |
| Redis AI cache | Exact/retrieval/embedding/semantic cache | Redis vector/search, invalidation, policy | Safe cache miss/bypass |
| SQL Server AI data | Configuration, versions, cost, evaluation, durable workflows | SQL HA/backup, RLS, session context | Fail closed for authorization/config; no uncontrolled AI execution |
| Object storage | Source/evaluation/backup artifacts | Storage, encryption, malware scan | Pause affected ingestion/evaluation |
| Event/outbox workers | Invalidation, usage, deletion, domain coordination | SQL/outbox, broker, consumers | Durable backlog with bounded processing; no event loss |
| Ingestion pipeline | Validate/chunk/embed/index approved knowledge | Source, malware scan, object storage, embedding, Qdrant | Pause publication; keep prior approved index |
| Evaluation service | Quality/security/fairness evidence and promotion gates | Suites, providers, SQL, object storage | Freeze promotion/renewal; current healthy production may continue by policy |
| Cost governance | Reservation, budget, ledger, forecast | SQL, price catalog, provider usage | Paid non-essential AI fails closed |
| OpenTelemetry pipeline | Metrics, traces, logs, dashboards, alerts | Collector/backends/notification | AI continues; local health alert and bounded telemetry loss |

Dependencies are represented in an operational service catalog. An unregistered dependency
cannot enter production.

---

# 5. Operating Model and Accountability

## 5.1 Core roles

| Role | Accountability |
|---|---|
| Service Owner | Reliability, lifecycle, support, capacity, runbooks, and operational acceptance |
| Product/AI Owner | Intended use, quality targets, feature scope, tenant communication, residual product risk |
| Platform/Operations | On-call, infrastructure, telemetry, incidents, changes, capacity, recovery exercises |
| Security | Threat monitoring, SEV-0 response, evidence protection, containment and clearance |
| Data Governance/Privacy | Classification, retention, deletion, legal hold, residency, provider processing |
| Domain Owner | HR/payroll/policy correctness, escalation, quality-incident validation |
| Finance/FinOps | Budgets, price catalog, reconciliation, cost anomalies and showback |
| Legal/Compliance | Jurisdictional/high-impact employment requirements and reportable-event advice |
| Tenant Administrator | Own-tenant policy, entitlement, approved contacts, maintenance and incident coordination |

## 5.2 RACI requirements

Every service, alert, runbook, maintenance window, provider, dataset, index, model assignment,
and recovery plan has one accountable owner. Shared accountability without a named owner is
not accepted at operational readiness review.

Segregation of duties applies to:

- Change author, reviewer, production approver, and deployer.
- Evaluation author/reviewer and release approver.
- Budget/price author and finance approver.
- Incident commander and affected change owner where conflict exists.
- Backup operator and restore validator.
- Deletion requester, approver, and completion verifier.

## 5.3 On-call readiness

Production support requires:

- Primary and secondary on-call coverage with tested contact routes.
- Current escalation matrix, provider contacts, tenant communication contacts, and deputies.
- Access provisioned before duty, least privilege, MFA, and time-bound elevation.
- Runbook training and simulation before independent on-call duty.
- Handoff containing incidents, active changes, risks, capacity, expiring approvals, and
  degraded services.
- Fatigue/escalation policy; unresolved incidents are handed over, not abandoned.

---

# 6. Environment and Deployment Controls

The minimum environment separation is:

- Local development.
- Shared integration/test.
- Security/performance/evaluation environment.
- Staging/pre-production.
- Production.

Production tenant data is not copied to non-production by default. Approved test data is
synthetic/de-identified and tenant-scoped. Any exception requires purpose, minimization,
encryption, access, retention, deletion, and audit approval.

Each environment has separate credentials, tenant catalog, encryption keys, provider
accounts/quotas, Qdrant collections, Redis namespaces/placements, object storage, telemetry,
and network boundaries. Production secrets or provider keys cannot be used in lower
environments.

Deployments are immutable, reproducible, signed/verified where supported, and refer to:

- Application/container/package version and dependency manifest.
- Database migration version.
- Provider adapter/model registry version.
- Prompt, safety, confidence, memory, cache, budget, and evaluation policy versions.
- Embedding/chunking/reranker/vector-index versions.
- OpenTelemetry schemas, dashboards, alert rules, and runbook versions.

No direct manual production configuration change is allowed outside an audited emergency
procedure. Emergency changes are time-bound, reviewed afterward, and converted to the normal
source-controlled configuration path.

---

# 7. Service Levels, Error Budgets, and Tenant SLA Evidence

Initial configurable SLOs inherited from ADR-031 are:

| SLO | Initial target | Measurement source |
|---|---|---|
| AI API availability | >= 99.9% monthly | Eligible successful responses / eligible requests |
| Retrieval latency | p95 <= 1.5 seconds | Retrieval and vector-search spans |
| Full knowledge-answer latency | p95 <= 10 seconds | Accepted end-to-end AI request span |
| Citation completeness | >= 98% on approved policy benchmark | ADR-034 evaluation evidence |
| Cross-tenant retrieval incidents | 0 | Security incidents and continuous isolation tests |
| Critical alert detection | <= 5 minutes | Event/signal occurrence to alert creation |

Targets are effective-dated by use case, risk, region, and service tier. Correct
authentication, authorization, budget, quota, safety, eligibility, and validation rejections
do not count as service failures. A valid approved fallback counts as available but is
reported separately.

Error-budget policy:

- Uses rolling and calendar-period views as defined by service policy.
- Uses multi-window burn-rate alerts for rapid and sustained consumption.
- Freezes risky prompt/model/index/cache/provider promotions when exhausted.
- Requires owner/operations/security approval and recovery evidence before unfreezing.
- Never trades tenant isolation, grounding, security, privacy, or prohibited-use controls for
  availability.

External SLA reports are generated from governed SLO evidence but remain separate from
internal objectives. Commercial exclusions, credits, and terms are effective-dated contract
data. A tenant sees only its own authorized SLA information.

---

# 8. Telemetry, Dashboards, and Data Protection

## 8.1 Telemetry architecture

Applications emit OpenTelemetry signals through shared instrumentation contracts. The
OpenTelemetry Collector receives, processes/redacts/samples, batches, and exports to the
approved self-hosted initial stack:

- Prometheus for metrics.
- Alertmanager for routing, grouping, inhibition, and silences.
- Grafana for dashboards.
- Loki for redacted operational logs.
- Tempo for sampled traces.

Managed backends remain optional exporters. Application code does not depend on a monitoring
vendor SDK.

## 8.2 Required dashboards

- **Platform operations:** availability, latency, throughput, saturation, queues, ingestion,
  Qdrant, Redis, providers, collectors, fallbacks, and degraded modes.
- **AI quality:** retrieval, groundedness, citations, hallucination severity/rate, confidence,
  refusals, languages/slices, evaluation and drift.
- **Security:** injection, leakage, denied tools, extraction patterns, cross-tenant canaries,
  incidents, and emergency controls.
- **Cost/FinOps:** usage, reservations, budgets, forecast, unpriced usage, provider
  reconciliation, cache value, and anomalies.
- **Executive/Product:** adoption, successful grounded answers, quality, availability, cost,
  incidents, and approved business-value measures.
- **Tenant admin:** own-tenant service, usage, quality, budget, entitlement, maintenance, and
  incident status through authorized application APIs.

## 8.3 Telemetry prohibitions

General telemetry does not contain raw prompts, responses, retrieved text, conversation
memory, employee/applicant identifiers, tenant IDs, source IDs, cache keys, vector values,
credentials, protected attributes, commercial terms, or hidden reasoning.

Low-cardinality dimensions use approved enums/versions. Restricted high-cardinality drilldown
uses authorized durable records, not metric labels. Debug capture is disabled by default.

## 8.4 Sampling and retention

- Metrics remain unsampled and low-cardinality.
- Tail-based trace/log sampling retains errors, slow requests, security blocks, fallbacks,
  degraded modes, and anomalies.
- Routine successes are sampled under effective-dated policy.
- Collector buffers are bounded and cannot create recursive alert/log storms.
- ADR-022 determines final retention, deletion, legal hold, and backup-erasure controls.

---

# 9. Alert Design and Severity Model

Alerts are symptom- and user-impact-oriented, actionable, deduplicated, grouped, inhibited
during parent outages, and linked to a dashboard, owner, severity, and tested runbook. Alerts
do not page only because an internal metric moved when no action is required.

| Severity | Examples | Initial response expectation |
|---|---|---|
| SEV-0 | Suspected cross-tenant disclosure, confirmed sensitive leakage, prohibited employment action | Immediate containment; page Security and Operations; incident command; preserve evidence |
| SEV-1 | Widespread AI outage, Qdrant corruption/unavailable, provider fallback storm, critical deletion failure | Page on-call; degraded mode/failover; tenant status communication |
| SEV-2 | SLO burn, sustained latency, quality/citation/hallucination regression, ingestion or invalidation backlog | Tracked incident; owner investigation within service target |
| SEV-3 | Capacity forecast, approval expiry warning, low-risk drift, maintenance action | Planned work with due date and owner |

Severity may increase as scope, sensitivity, duration, affected tenants, legal impact, or
uncertainty increases. A lower observed request count does not lower a potential cross-tenant
or sensitive-data incident.

Alert thresholds and response targets are configuration. Silences require scope, reason,
owner, start/end time, and audit; they do not silence durable security/audit events.

---

# 10. Incident Command and Response Lifecycle

Incident response follows a prepared lifecycle aligned with enterprise risk management:

1. Detect and validate signal.
2. Declare severity and affected scope.
3. Assign incident roles.
4. Contain harm and preserve evidence.
5. Diagnose with timeline and hypotheses.
6. Recover through an approved path.
7. Validate isolation, integrity, quality, and business behavior.
8. Communicate status and resolution.
9. Monitor for recurrence.
10. Complete blameless post-incident review and tracked actions.

## 10.1 Incident roles

- **Incident Commander:** owns priorities, decisions, roles, and closure criteria.
- **Operations Lead:** containment, infrastructure, recovery execution.
- **Security Lead:** security classification, evidence, breach/notification coordination.
- **Product/Domain Lead:** business impact, quality/domain validation, tenant use-case decision.
- **Communications Lead:** internal, executive, tenant, provider, and status updates.
- **Scribe/Timeline:** decisions, actions, evidence references, handoffs, and timestamps.
- **Provider Liaison:** external provider escalation and evidence without delegating command.

One person may hold multiple roles only for low-severity incidents. SEV-0/SEV-1 require a
dedicated commander and scribe as soon as practical.

## 10.2 Evidence handling

Evidence is minimized, encrypted, access-restricted, integrity-protected, and referenced from
the incident record. Prompts/responses or employee data are collected only when necessary and
approved. Evidence is not placed in chat, general tickets, dashboards, or telemetry labels.

## 10.3 Closure criteria

An incident is not resolved only because traffic recovered. Closure requires:

- Affected scope and timeline understood to an approved confidence.
- Containment complete and unsafe paths disabled.
- Current tenant isolation, authorization, data integrity, source/index/cache/memory state,
  and quality validated.
- Backlogs/retries/reconciliation/deletion tasks complete or explicitly owned.
- Tenant/regulatory/provider communication obligations addressed.
- Regression tests/evaluation cases and prevention actions recorded.

---

# 11. Degraded Mode and Recovery Order

The mandatory degraded-mode order is:

1. Retry only safe transient failures with bounded exponential backoff, jitter, timeout,
   idempotency, and circuit breaker.
2. Use an already approved fallback model/provider only when capability, privacy, residency,
   quality, evaluation, credential, and budget rules permit.
3. Serve retrieval-only results with current authorized source links when the use case and
   policy permit.
4. Disable the affected capability with a clear unavailable status and human support route.

The platform never:

- Removes tenant/permission/source filters to restore retrieval.
- Uses stale memory/cache/index/policy after failed validation.
- Switches to an unapproved paid provider or credential.
- Produces an ungrounded answer to preserve uptime.
- Executes state-changing HR actions.

Recovery order prioritizes tenant context, authorization, audit/security, configuration,
canonical source integrity, retrieval, output safety, then optimizations such as cache,
memory continuity, and detailed telemetry.

---

# 12. Change, Release, and Rollback Management

## 12.1 Normal production change

Every change has owner, reason, risk classification, affected tenants/use cases, dependency
impact, test/evaluation evidence, security/privacy review, rollout plan, monitoring, rollback,
maintenance/communication, and approval.

Material AI changes use ADR-034 release candidates and progress through sandbox, evaluation,
review, canary, and production. Production deployment binds the exact approved system-bundle
hash. Direct alias changes are prohibited.

## 12.2 Database and data-store change

- SQL changes use reviewed DbUp SQL-script migrations (ADR-037) and rollback/forward-fix plan.
- Qdrant indexes use shadow build, validation, alias/placement switch, rollback window, and
  retirement; no in-place unvalidated mutation.
- Redis entry/index schema changes use namespace/version migration and safe miss behavior.
- Event contracts are versioned and maintain consumer compatibility.

## 12.3 Rollback

Rollback restores a compatible full bundle, not only application binaries or model name.
The rollback manifest includes prompt, provider/model, embedding, index, source snapshot,
tool, guardrail, confidence, memory, cache, budget-routing, and evaluation versions.

Rollback is rehearsed at approved cadence. Failed rollback triggers feature disablement or
retrieval-only/manual support mode.

## 12.4 Emergency change

Emergency change requires incident, reason, authorized requester/approver, exact scope,
time limit, evidence, monitoring, rollback, and post-event review. It cannot bypass tenant
isolation, security/privacy, audit, prohibited use, or evaluation hard blocks.

---

# 13. Model and Provider Operations

Provider/model activation requires:

- Approved adapter/capabilities, model registry, region, and data-processing terms.
- Tenant entitlement, credential reference, budget, rate/capacity limit, and allowed data
  classification.
- ADR-034 evaluation and approved fallback/degraded behavior.
- Connection/health test, timeout/retry/circuit policy, dashboards, alerts, and runbook.

Operational controls:

- Pin provider model IDs/versions/fingerprints where available.
- Detect behavior drift even when a provider name/alias is unchanged.
- Separate credentials by environment and tenant/account policy.
- Rotate credentials without downtime and revoke compromised credentials immediately.
- Measure provider latency, errors, throttling, token usage, cache behavior, cost, and
  residency route.
- Limit retries to idempotent/safe calls; unknown outcome is reconciled.
- Test fallback regularly without silently sending prohibited data to another region/provider.

Provider status pages and support statements are signals, not the only health evidence.
Failover decisions are made by platform policy and accountable operators.

---

# 14. Qdrant and Vector Index Operations

## 14.1 Deployment and health

- Version-pinned self-hosted Qdrant is the first adapter.
- Production topology, replication, sharding, failure domains, TLS/authentication, storage,
  quotas, and dedicated-tenant placement follow ADR-030.
- Monitor readiness, cluster/peer health, collection/shard status, operation latency, errors,
  storage, memory, CPU, disk, compaction, replication, and snapshot health.
- No public network exposure; credentials are secret references.

## 14.2 Index lifecycle

`Draft -> Building -> Validating -> Approved -> Active -> Retiring -> Retired`

Index publication requires canonical source manifest, embedding/chunking/metadata versions,
tenant/permission/effective-date tests, retrieval evaluation, snapshot/rebuild evidence, and
rollback pointer. Late builds cannot overwrite a newer approved version.

## 14.3 Backup, restore, and rebuild

- Canonical approved source documents and metadata remain the rebuild authority.
- Snapshots are encrypted, versioned, access-controlled, integrity-checked, retained, and
  mapped to source/index manifests.
- Restore occurs into an isolated placement/collection first.
- Validation re-runs tenant isolation, payload filters, source versions, effective dates,
  retrieval quality, and sample citations before activation.
- If snapshot trust is uncertain, rebuild from canonical source rather than serve it.

## 14.4 Qdrant failure behavior

An outage cannot trigger cross-tenant/global retrieval or an unfiltered SQL/object-store
fallback. Approved use cases may provide current source navigation or retrieval-only alternate
search; otherwise AI knowledge response is unavailable.

---

# 15. Redis, Memory, and Cache Operations

## 15.1 Redis placement

Local development may use standalone Redis. Production uses the ADR-035 approved standalone-
bypass, Sentinel, Cluster, or dedicated profile with failure-domain placement and tested
failover. Session memory, semantic cache, and critical platform keys use separate placement,
keyspaces, or eviction domains according to risk/capacity.

## 15.2 Memory operations

- Monitor memory hit/miss/expiry/eviction, invalidation, summary generation, deletion, and
  stateless fallback.
- Permission, role-matrix, employment, purpose, and source changes invalidate context.
- Redis loss degrades to stateless mode; provider-hosted hidden memory is never enabled.
- Summary-store outage uses fresh authorized context only.

## 15.3 Cache operations

- Monitor cache value, false positive/negative, semantic drift, stale/unauthorized hits,
  invalidation backlog, namespace rotation, warm-up, capacity, and poisoning signals.
- Emergency cache disablement supports global, tenant, and use-case scope without deployment.
- Policy expiry disables reads/writes safely.
- Warm-up uses approved manifests and normal eligibility/security/quality/budget controls.
- Cache loss is a safe miss; no stale or broader-scope fallback.

## 15.4 Persistence and recovery

Semantic cache persistence/backups are disabled by default. If enabled, expiry, namespace,
deletion, encryption, restore isolation, and RPO/RTO are tested. Cache content is not restored
when rebuilding it is safer.

---

# 16. Knowledge Ingestion and Index Publication Operations

Ingestion stages are independently observable:

`Received -> Scanning -> Validating -> Normalizing -> Chunking -> Embedding -> Indexing ->
Evaluating -> Approved -> Published`

Operational requirements:

- Idempotent source/document/version processing.
- Malware/type/size validation before parsing.
- Quarantine for failed or suspicious content.
- Bounded queues, retries, dead letters, poison-message handling, and backpressure.
- Tenant/source/version/effective-date lineage at every stage.
- No partial publication; prior approved index remains active until new alias switch.
- Reconciliation detects missing source chunks, duplicate vectors, stale indexes, and orphaned
  artifacts.
- Deletion/supersession invalidates retrieval, memory, and cache and removes eligible vectors.

Backlog SLOs are defined by source/use-case priority. Capacity controls prevent bulk ingestion
from starving interactive retrieval or another tenant.

---

# 17. Evaluation, Quality, and Promotion Operations

Operations coordinates ADR-034 execution without owning domain approval:

- Ensure evaluation environments, datasets, providers, capacity, and sealed-holdout access.
- Monitor run queue, evaluator failures, human-review backlog, gate status, and approval expiry.
- Block deployment when evidence is missing, stale, contaminated, expired, or failed.
- Monitor production hallucination rate/severity, citations, confidence, refusals, languages,
  slices, provider behavior drift, and reviewer quality.
- Route confirmed incidents into regression suites and revalidation.

Model-as-judge is never the sole approval signal. Budget pressure cannot skip mandatory
cases, slices, security/fairness tests, or human review.

Quality regression response order:

1. Freeze promotion and determine affected bundle/scope.
2. Disable unsafe feature/scope or roll back when critical.
3. Preserve minimized evidence.
4. Validate source/index/prompt/model/provider/guardrail/evaluator changes.
5. Add regression case, evaluate fix and baseline, obtain independent approval.

---

# 18. Cost, Budget, Quota, and Credential Operations

Operations and Finance monitor:

- Usage/reservations/settlement by tenant, use case, provider, model, and environment.
- Soft/hard budget thresholds, forecasts, expiry, unpriced usage, and reconciliation variance.
- Token/request/embedding/rerank/vector/cache/storage/telemetry infrastructure cost.
- Provider throttling, concurrency, credential failures, and unexpected billing mode.
- Cache/provider-prefix savings without double counting.

Paid non-essential AI fails closed when reservation/cost enforcement is unavailable. Budget
exhaustion does not block core HRMS, audit, deletion, security, cost viewing, or AI disablement.

Cost incidents check for traffic growth, retry/fallback storms, cache loss, credential abuse,
price version error, provider drift, batch/warm-up/evaluation jobs, and tenant isolation.

Credentials are secret references, environment-scoped, least privilege, rotated on schedule
and incident, never logged/exported, and tested after rotation. Tenant-direct keys do not
bypass platform security, quotas, residency, or provider approval.

---

# 19. Security and Privacy Operations

Security monitoring covers:

- Direct/indirect prompt injection and jailbreak campaigns.
- Sensitive-data leakage, extraction patterns, prompt/cache probing, and memorization signals.
- Unauthorized tool/source access, IDOR, RBAC/ABAC failures, and cross-tenant canaries.
- Poisoned documents, vector/cache poisoning, malicious files, and supply-chain/provider
  changes.
- Credential/key compromise, abnormal provider use, denial-of-service, and cost amplification.
- Prohibited employment action or hidden employee profiling.

SEV-0 containment may disable AI globally/tenant/use-case, revoke credentials, rotate cache
namespaces, suspend indexes/providers, invalidate memory, and block ingestion. Core audit and
evidence preservation remain available.

Potential breach notification, employee/tenant communication, regulator/law-enforcement
engagement, and legal privilege are decided by authorized Security/Privacy/Legal roles, not
the model or on-call engineer alone.

---

# 20. Events, Queues, Outbox, and Background Jobs

Operational requirements:

- Transactional outbox for durable domain/security/deletion/usage events.
- Consumer idempotency and inbox/deduplication where required.
- Versioned event contracts and compatibility policy.
- Bounded retries with jitter and dead-letter routing.
- Poison-message quarantine and controlled replay.
- Per-tenant/use-case quotas, fair scheduling, backpressure, and bulkheads.
- End-to-end correlation without sensitive payloads.
- Reconciliation jobs for missed invalidation, cost, permission, deletion, and index events.

Monitor queue depth, oldest-message age, processing rate, retry/dead-letter count, consumer
lag, partition/tenant fairness, and outbox age. Increasing retries without containment is not
a recovery strategy.

Replay requires reason, scope, event range, owner, approval, dry-run/impact assessment,
idempotency proof, monitoring, stop condition, and audit. Cross-tenant bulk replay is
platform-restricted.

---

# 21. Capacity, Performance, and Load Management

Capacity planning uses demand forecasts by tenant, use case, region, model, source volume,
embedding dimensions, index size, cache/memory, evaluation workload, and telemetry volume.

Controls include:

- Rate limits, concurrency, queue limits, timeouts, circuit breakers, load shedding,
  backpressure, bulkheads, and provider quotas.
- Qdrant shard/replica/collection placement and storage growth.
- Redis memory/index/connection/eviction and tenant quota forecasts.
- SQL connection pool, query/RLS/index/partition health.
- Object storage, upload/scan/chunk/embed/index throughput.
- Collector/backend buffers, cardinality, retention, and disk capacity.

Load tests represent multi-tenant concurrency, noisy neighbors, long prompts, large documents,
provider throttling, cache cold start, ingestion burst, failover, and degraded mode. They
include p50/p95/p99 latency, errors, saturation, cost, quality, and security invariants.

Capacity changes use approved configuration/infrastructure changes and cannot silently
activate a paid managed service.

---

# 22. Backup, Restore, and Disaster Recovery

## 22.1 Business-impact tiers

| Tier | AI data/capability | Recovery principle |
|---|---|---|
| Critical control | Tenant/identity references, authorization/config, audit/security, deletion/legal hold | Restore through platform DR; AI remains disabled until trustworthy |
| Durable AI governance | SQL cost, evaluation, policies, memory metadata/summaries where enabled | Restore with RLS, encryption, lineage, reconciliation, and approval |
| Canonical knowledge | Approved source documents/metadata and index manifests | Restore canonical source before rebuilding/activating index |
| Derived AI data | Qdrant indexes, embeddings, Redis cache, permitted summaries | Rebuild/restore only after validation; safe loss preferred to stale exposure |
| Operational telemetry | Metrics/logs/traces | Restore per retention/business need; never substitute for audit |

## 22.2 RPO and RTO

RPO/RTO are effective-dated per service tier and data class. Each component records:

- Business impact and dependency order.
- Backup/rebuild source, frequency, retention, encryption, location, and owner.
- Recovery procedure, infrastructure prerequisites, validation, and rollback.
- Maximum tolerable outage/data loss and tenant/SLA commitments.

Derived cache may have RPO of no restored entries and immediate safe-bypass RTO. Qdrant may
restore a validated snapshot or rebuild from canonical sources. Durable SQL and audit follow
platform database recovery requirements.

## 22.3 Recovery validation

Before traffic returns:

- Restore into isolated environment/placement.
- Verify integrity, encryption/key access, schema/version compatibility, and malware status.
- Re-establish trusted tenant context and RLS.
- Reconcile source/index/cache/memory/config/event/cost/deletion state.
- Re-run cross-tenant, authorization, retrieval, citation, safety, quality, and smoke tests.
- Confirm expired/deleted/offboarded data did not reappear.
- Record evidence, approver, scope, and monitoring period.

## 22.4 Exercise cadence

Restore, provider failover, Qdrant rebuild, Redis failover, event replay, cache cold start,
telemetry outage, and regional/dependency loss exercises occur at risk-approved intervals.
Tabletop-only exercises do not replace technical restore/rebuild tests.

---

# 23. Retention, Deletion, Legal Hold, and Tenant Offboarding

ADR-022 is a Phase 6C hard dependency. Until approved, no AI implementation may claim final
retention/deletion compliance.

The deletion/offboarding orchestrator covers:

- Source documents and derived chunks/embeddings/vector indexes.
- Conversation session memory, summaries/metadata, and provider temporary state.
- Exact/retrieval/embedding/semantic caches and provider prompt-cache residual TTL.
- Evaluation cases/outputs where eligible, exports, object artifacts, and reviewer mappings.
- Usage/cost/telemetry data subject to legal/financial/security retention.
- Replicas, snapshots, backups, dead letters, warm-up inputs, and restored environments.

Operational controls:

- Scope from trusted tenant/user and approved request/legal basis.
- Legal-hold check before deletion.
- Idempotent staged workflow with status, retries, evidence, and reconciliation.
- Immediate access/namespace disable before asynchronous physical purge where needed.
- Completion proof without exposing deleted content.
- Backup erasure/expiry schedule and restore-time tombstone/reconciliation.
- Tenant-facing status through authorized APIs.

Legal hold prevents eligible deletion but does not make held content available to AI or
general operations.

---

# 24. Maintenance, Patching, and Vulnerability Management

Maintain an inventory of application, container, operating system, .NET/Node dependencies,
SQL, Qdrant, Redis, RabbitMQ/service bus, OpenTelemetry, Prometheus/Grafana/Loki/Tempo,
embedding/model/provider adapters, and evaluation libraries.

Requirements:

- Supported/version-pinned releases and license review.
- Vulnerability and end-of-support monitoring.
- Severity/risk-based remediation targets.
- Staging test, compatibility, migration, rollback, and maintenance communication.
- Rolling/blue-green/canary update where supported.
- Post-change health, isolation, quality, cost, and data validation.
- Emergency security patch procedure and post-event review.

Provider model/service changes are treated as supply-chain/runtime changes even without local
deployment. Behavior drift can trigger suspension and revalidation.

---

# 25. Operational Records and Audit

Durable operational records include:

- Service ownership, dependency, SLO, and runbook versions.
- Production changes, approvals, deployments, rollbacks, and emergency changes.
- Incidents, severity, timeline, decisions, evidence references, communication, and actions.
- Maintenance windows and silences.
- Failover/restore/rebuild/deletion/offboarding exercises and outcomes.
- Provider/model/index/config/cache/memory/evaluation approval and expiry.
- Administrative access/elevation and break-glass use.

Conceptual SQL entities:

```text
AI.AiServiceComponent
  AiServiceComponentId, TenantId, ComponentKey, OwnerRole, OwnerId,
  DependencyManifestJson, DataClassification, ServiceTier,
  SloPolicyVersion, RpoPolicyVersion, RtoPolicyVersion,
  RunbookVersion, DashboardReference, AlertPolicyVersion,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiOperationalIncident
  AiOperationalIncidentId, TenantId, IncidentKey, Severity,
  AffectedScopeJson, CommanderId, SecurityLeadId,
  DetectionDate, DeclaredDate, ContainedDate, RecoveredDate, ClosedDate,
  RootCauseCategory, EvidenceManifestReference,
  CommunicationReference, PostIncidentReviewReference, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiOperationalExercise
  AiOperationalExerciseId, TenantId, ExerciseType,
  ScopeJson, ScenarioVersion, PlannedDate, ExecutedDate,
  RpoObserved, RtoObserved, EvidenceReference,
  FindingsJson, RemediationReference, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiOperationalReadinessReview
  AiOperationalReadinessReviewId, TenantId, UseCaseKey,
  ReleaseCandidateId, ServiceCatalogVersion,
  ChecklistVersion, EvidenceManifestHash,
  Decision, DecisionReason, ApprovedScopeJson,
  EffectiveFrom, EffectiveTo, ApprovedBy, ApprovedDate,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber
```

All tables use tenant context/RLS, mandatory audit/version columns, tenant-leading indexes,
and effective dating where policy/configuration changes. Platform-global records use the
approved system-tenant/control-plane context and remain inaccessible to tenant roles.

Telemetry cannot replace these records.

---

# 26. Tenant and Stakeholder Communication

Communication plans define audience, channel, owner, approval, cadence, localization, and
content classification for:

- Planned maintenance.
- Service degradation/outage and fallback behavior.
- Security/privacy incident where notification is authorized/required.
- Quality/harmful-output issue and affected feature scope.
- Provider/model/index change affecting behavior or availability.
- Budget/entitlement/quota expiry.
- Recovery completion and follow-up actions.

Updates state known facts, impact, affected services/regions/tenants, mitigation, safe user
action, next update time, and support route. They do not speculate, expose another tenant,
publish attack details prematurely, or promise unvalidated recovery times.

Status communication does not replace direct legal/contractual notification.

---

# 27. Standard Runbook Contract

Every runbook contains:

1. ID, title, owner, version, approval, review/expiry date.
2. Purpose and affected components/use cases/data classes.
3. Detection signals, alerts, dashboard, and declaration criteria.
4. Preconditions, access, safety warnings, and prohibited actions.
5. Severity and escalation matrix.
6. Immediate containment actions in priority order.
7. Diagnostic decision tree and evidence to collect.
8. Recovery/failover/rollback steps with idempotency.
9. Validation checklist for tenant isolation, security, integrity, quality, cost, and backlog.
10. Communication templates/routes and update cadence.
11. Stop conditions, abort/disable path, and failed-recovery escalation.
12. Closure, reconciliation, regression evidence, and post-incident actions.

Runbooks are source-controlled, peer-reviewed, linked from alerts, tested through exercises,
and reviewed after use or relevant architecture/provider change. A runbook that depends on
one person's memory is not operationally ready.

---

# 28. Required Runbook Catalog

## AI-RUN-001 - Model/provider outage and fallback storm

- **Detect:** provider errors/timeouts/throttling, circuit open, fallback rate/latency/cost.
- **Contain:** stop unsafe retries, open circuit, enforce budget and approved routing.
- **Recover:** provider restore or approved fallback; retrieval-only/disable if unavailable.
- **Validate:** residency, capability, quality, citations, cost, no duplicate/unknown requests.

## AI-RUN-002 - Qdrant outage, corruption, restore, and re-index

- **Detect:** readiness/peer/shard/storage/snapshot/retrieval errors or quality anomaly.
- **Contain:** stop affected index publication, disable unsafe retrieval, retain prior alias.
- **Recover:** failover, isolated snapshot restore, or canonical-source rebuild.
- **Validate:** tenant partition, filters, effective dates, lineage, retrieval and citations.

## AI-RUN-003 - Latency/SLO degradation and capacity saturation

- **Detect:** burn alerts, p95/p99, queues, CPU/memory/disk/connections, provider latency.
- **Contain:** load shed, backpressure, quotas, circuit breakers, pause background jobs.
- **Recover:** scale approved component, resolve bottleneck, staged traffic restoration.
- **Validate:** quality/security/cost unaffected and error budget stabilizing.

## AI-RUN-004 - Citation, groundedness, refusal, or hallucination regression

- **Detect:** ADR-034 drift, incidents, domain review, complaint, provider behavior drift.
- **Contain:** freeze promotion, narrow/disable scope, rollback unsafe bundle.
- **Recover:** source/index/prompt/model/guardrail correction and re-evaluation.
- **Validate:** hard gates, languages/slices, domain approval, regression case.

## AI-RUN-005 - Prompt injection, data leakage, and cross-tenant incident

- **Detect:** detectors, canaries, unauthorized evidence, user/provider report.
- **Contain:** SEV-0 declaration, disable scope, revoke credentials, invalidate cache/memory,
  preserve restricted evidence.
- **Recover:** root-cause correction and independent Security clearance.
- **Validate:** isolation negative tests, deletion/notification assessment, monitored re-entry.

## AI-RUN-006 - Token/cost spike, credential abuse, and quota exhaustion

- **Detect:** usage anomaly, reservation/forecast/price/reconciliation alert.
- **Contain:** revoke/rotate credential, hard limit, disable job/use case, stop retries.
- **Recover:** correct routing/price/cache/job/credential and reconcile costs.
- **Validate:** no unauthorized tenant billing, budgets and forecasts accurate.

## AI-RUN-007 - Telemetry collector/exporter/backend outage

- **Detect:** collector queue/drop/export health and dashboard gaps.
- **Contain:** bounded buffering, sampling, stop recursive logging, retain audit/security paths.
- **Recover:** collector/backend/exporter restore or optional approved exporter.
- **Validate:** no application blocking, cardinality/sensitive data, alert and data-gap record.

## AI-RUN-008 - Ingestion backlog and index-promotion failure

- **Detect:** oldest job, stage lag/error, dead letters, vector/source mismatch.
- **Contain:** pause source/tenant, quarantine poison file, keep prior active index.
- **Recover:** fix stage, controlled replay/rebuild, new shadow index.
- **Validate:** lineage, counts, permissions, effective dates, evaluation and alias switch.

## AI-RUN-009 - Cache poisoning, staleness, and invalidation failure

- **Detect:** false/stale/unauthorized hit, poisoning signal, invalidation lag/dead letter.
- **Contain:** emergency disable, namespace rotate, purge, block warm-up/writes.
- **Recover:** correct policy/key/filter/event/threshold and rebuild eligible entries.
- **Validate:** isolation, source reauthorization, semantic drift, deletion and incident suite.

## AI-RUN-010 - Conversation memory corruption or authorization drift

- **Detect:** security-context mismatch, invalidation failure, summary lineage/quality issue.
- **Contain:** disable memory, reset affected context, prevent summary reuse.
- **Recover:** reconcile permissions/sources, regenerate authorized summary or remain stateless.
- **Validate:** no Qdrant conversation vectors, purpose, deletion, role-matrix invalidation.

## AI-RUN-011 - Evaluation regression, gate failure, or approval expiry

- **Detect:** failed/expired suite, reviewer-quality issue, drift, provider change.
- **Contain:** freeze promotion/renewal, suspend affected candidate when required.
- **Recover:** dataset/evaluator/candidate correction and independent review.
- **Validate:** sealed evidence, statistical/slice results, approvals, rollback candidate.

## AI-RUN-012 - Tenant deletion, offboarding, or legal-hold conflict

- **Detect:** approved request, workflow failure, stale artifact, restore/reappearance.
- **Contain:** disable access/namespaces/provider routes; resolve legal-hold authority.
- **Recover:** idempotent purge/retry/reconciliation across stores/providers/backups.
- **Validate:** completion evidence, no reachable eligible data, audit retained lawfully.

## AI-RUN-013 - Redis outage, failover, corruption, or saturation

- **Detect:** Sentinel/Cluster/node/replica/index/memory/eviction/connection signals.
- **Contain:** stateless memory, cache bypass, protect critical key domains, rate-limit cold load.
- **Recover:** failover/rebuild/replace; restore cache only when safer than miss.
- **Validate:** no stale/rotated/deleted entries, isolation, TTL, ACL, warm-up approval.

## AI-RUN-014 - Event/outbox backlog, dead letter, or replay

- **Detect:** outbox/queue age, consumer lag, retries, dead letters, reconciliation mismatch.
- **Contain:** pause poison scope, preserve ordering/idempotency, stop retry storm.
- **Recover:** fix consumer/contract/dependency; approved scoped replay.
- **Validate:** no duplicate business/cost/deletion action, tenant fairness, backlog cleared.

## AI-RUN-015 - Backup/restore or regional/dependency disaster

- **Detect:** declared disaster, integrity/availability loss, recovery trigger.
- **Contain:** freeze writes/promotions, protect evidence, communicate status.
- **Recover:** dependency-ordered restore/rebuild into isolated environment.
- **Validate:** RPO/RTO, tenant/RLS, deletion tombstones, source/index/quality/security.

## AI-RUN-016 - Prompt/model/embedding/index/config rollback

- **Detect:** incident, failed canary, quality/cost/security/latency regression.
- **Contain:** stop rollout, retain current/previous immutable bundles.
- **Recover:** one-step compatible full-bundle rollback.
- **Validate:** health, isolation, grounding, citations, fallback, cache/memory compatibility.

## AI-RUN-017 - Secret/key compromise and emergency rotation

- **Detect:** secret exposure, anomalous use, provider/security notification.
- **Contain:** revoke, disable provider/scope, rotate dependent sessions/caches where needed.
- **Recover:** issue least-privilege secret, update references, validate connectivity.
- **Validate:** no old-key use, logs/artifacts cleaned, cost/data impact assessed.

## AI-RUN-018 - Retention, archival, legal-hold, or backup-erasure failure

- **Detect:** overdue purge/archive, hold mismatch, restored expired data, deletion evidence gap.
- **Contain:** block affected reuse/export/restore, preserve legal authority/evidence.
- **Recover:** correct policy/workflow, purge/archive/reconcile and verify backups/providers.
- **Validate:** retention clock, hold scope, no AI availability of held/expired content.

---

# 29. Operational Readiness Review

No AI use case enters production until the Operational Readiness Review (ORR) confirms:

- Approved constitutional five-document set, Security design, OpenAPI, and required ADRs.
- Named service/product/security/domain/data/finance owners and on-call coverage.
- Complete dependency/service catalog and environment separation.
- SLOs/error budgets, dashboards, actionable alerts, and tenant reporting.
- Business KPI definitions, owners, review cadence, and tenant-safe dashboard scope.
- Capacity/load evidence, quotas, provider limits, and cost budget.
- Approved lifecycle state, evaluation release candidate, Governance Board decision, and
  rollback bundle.
- Tested degraded modes, provider fallback, Qdrant/Redis behavior, queue backpressure.
- Runbooks, access, provider contacts, communication templates, and escalation.
- Backup/rebuild, RPO/RTO, restore/isolation/deletion validation, and exercise evidence.
- Retention, legal hold, deletion/offboarding, residency, and provider processing approval.
- No unresolved critical/high risk or expired policy/approval.

ORR produces an immutable evidence manifest and scoped, effective-dated decision. Failed or
conditional items have owners, deadlines, compensating controls, and expiry. Critical
security, tenant, privacy, legal, deletion, or prohibited-use gaps cannot receive a waiver.

---

# 30. Exercises and Continuous Improvement

The exercise program covers:

- On-call paging and incident command.
- Cross-tenant/data-leak tabletop and technical containment.
- Provider outage/fallback and credential revocation.
- Qdrant snapshot restore and canonical rebuild.
- Redis Sentinel/Cluster failover and safe cache/memory bypass.
- Queue/backlog/dead-letter replay.
- Telemetry backend outage.
- Cost spike and cache cold-start storm.
- Evaluation regression and full-bundle rollback.
- Tenant offboarding/deletion and restore-time reappearance test.
- Regional/dependency disaster recovery.

Exercises record scenario/version, participants, evidence, observed RPO/RTO/MTTD/MTTR,
control failures, communication, findings, owners, deadlines, and retest. Repeated findings
cannot remain accepted indefinitely; they escalate through risk governance.

Post-incident and exercise actions feed backlog, architecture decisions, evaluation cases,
runbooks, capacity plans, security controls, and training.

---

# 31. Operational API and Automation Requirements

Phase 6D API/OpenAPI must expose only governed operational capabilities, including:

- Own-tenant AI health, maintenance, degraded mode, usage, budget, and incident status.
- Restricted platform component/provider/index/cache/evaluation health.
- Approved emergency disablement, namespace rotation, failover, rollback, and invalidation
  workflows with idempotency and audit.
- Deletion/offboarding and operational-exercise status.

Administrative automation uses JWT/service identity, server-resolved tenant, RBAC plus ABAC,
least privilege, correlation/request IDs, rate limits, idempotency, optimistic concurrency,
reason, approval, and audit. It never exposes prompts, responses, employee data, raw cache
entries, vectors, credentials, or cross-tenant details.

Destructive/recovery operations support preview/dry run where meaningful, bounded scope,
approval, progress, cancellation/stop conditions, reconciliation, and immutable evidence.

---

# 32. AI Model Lifecycle and Deployment Bundle Governance

AI production governance applies to the complete deployment bundle, not only the model name.
A production AI bundle includes:

- Provider adapter, provider account, model identifier, model version where available, and
  model capability profile.
- Prompt library, safety policy, grounding policy, citation policy, confidence thresholds,
  tool permissions, and purpose boundary.
- Retrieval profile, source corpus, chunking, embedding, reranking, vector-index, Qdrant
  collection/alias, cache, and memory policy versions.
- Evaluation suite, approved dataset versions, hallucination/fairness/security evidence,
  approval record, cost policy, and rollback bundle.

The standard lifecycle is:

`Draft -> Evaluation -> Approved -> Canary -> Production -> Deprecated -> Retired`

| Stage | Entry criteria | Exit criteria and controls | Accountable owners |
|---|---|---|---|
| Draft | Business purpose, tenant/data scope, risk tier, provider/model candidate, expected value, and initial cost estimate are recorded. | Bundle is complete enough for evaluation; prohibited use, residency, and data-processing conflicts are screened. | Product/AI Owner, Service Owner |
| Evaluation | Draft bundle is immutable for test, evaluation data is approved, and security/privacy prechecks are complete. | ADR-034 quality/security/fairness/cost gates pass; failures create findings and block promotion. | Evaluation Owner, Domain Owner, Security, Data Governance |
| Approved | Evaluation evidence, rollback bundle, budget, ORR prerequisites, and governance approval are recorded. | Change is scheduled for canary with communication, monitoring, and stop conditions. | AI Governance Board, Service Owner |
| Canary | Limited tenants/users/use cases are enabled under explicit canary policy and enhanced monitoring. | Promotion requires stable SLOs, business KPIs, no critical safety/security/cost regression, and canary sign-off; otherwise rollback occurs. | Operations, Product/AI Owner, Security where applicable |
| Production | Bundle is generally available within approved scope, monitored, and included in service catalog/runbooks. | Bundle remains active until superseded, deprecated, disabled, or retired by approved lifecycle decision. | Service Owner, Product/AI Owner |
| Deprecated | Replacement or retirement plan exists; no new tenant/use-case onboarding occurs unless explicitly approved. | Existing traffic is migrated or disabled; rollback compatibility and support window are maintained. | Product/AI Owner, Operations |
| Retired | Traffic is zero, dependent indexes/caches/prompts are disabled, and retention/legal-hold obligations are checked. | Retirement evidence, deletion/archival actions, audit records, and post-retirement monitoring are complete. | Service Owner, Data Governance, Security |

Lifecycle rules:

- A model cannot move to `Canary` or `Production` without an approved full-bundle rollback
  plan and tested rollback path.
- Any provider behavior drift, safety policy change, model replacement, prompt change,
  retrieval-index replacement, or high-risk threshold change re-enters the lifecycle at
  `Evaluation` unless the Governance Board approves a narrower emergency path.
- Deprecated bundles remain observable and auditable until retirement is complete.
- Retired bundles cannot be reactivated; they must be cloned into a new `Draft` bundle and
  pass the current lifecycle gates.
- Emergency rollback may move `Canary` or `Production` traffic back to the last approved
  healthy bundle immediately, with post-incident governance review.

---

# 33. Business KPI Monitoring

Operational health does not prove business success. Production AI services also measure
business outcomes so Product and Operations can decide whether a capability is useful,
trusted, affordable, and worth expanding.

Business KPIs complement SLOs, security telemetry, evaluation evidence, and cost controls.
They do not replace authorization, safety, quality, or compliance gates.

| KPI | Purpose | Initial owner |
|---|---|---|
| AI Adoption Rate | Measures eligible users/tenants actively using approved AI capabilities. | Product/AI Owner |
| User Satisfaction Score | Measures direct user satisfaction from feedback, surveys, or tenant review channels. | Product/AI Owner |
| AI Deflection Rate | Measures how often AI resolves a request without needing a human support or operations path. | Product/AI Owner, Operations |
| Human Escalation Rate | Measures how often users or controls escalate AI interactions to a human. | Product/AI Owner, Domain Owner |
| Successful AI Resolution Rate | Measures completed, grounded, authorized, and accepted AI outcomes. | Product/AI Owner, Domain Owner |
| Average User Feedback Rating | Measures per-response or per-session user feedback trends. | Product/AI Owner |
| Cost per Successful AI Request | Combines FinOps cost ledger with accepted successful outcomes. | Finance/FinOps, Product/AI Owner |
| Business Value Delivered | Measures agreed value such as time saved, ticket reduction, faster policy lookup, or improved self-service. | Product/AI Owner, Business Sponsor |

Business KPI controls:

- KPI definitions are versioned and effective-dated by use case, tenant segment, region, and
  service tier where needed.
- KPI dashboards are tenant-scoped and do not expose cross-tenant comparisons unless legally,
  contractually, and commercially approved.
- Feedback collection must avoid coercive employee monitoring and must follow privacy,
  retention, and jurisdictional requirements.
- KPI degradation can trigger product review, model/prompt evaluation, feature disablement,
  tenant communication, or lifecycle rollback when tied to quality, safety, cost, or trust.
- Business KPIs are reviewed with operational SLOs during monthly service review and during
  Governance Board decision cycles for significant AI changes.

---

# 34. AI Governance Board

The AI Governance Board owns significant AI production decisions. Operations owns reliable
execution; the board owns risk acceptance, promotion authority, policy direction, and
cross-functional accountability.

Minimum board membership:

- Product/AI Owner.
- Service Owner or Platform/Operations representative.
- Security Architect or delegate.
- Data Governance/Privacy representative.
- HR/Payroll Domain Owner for affected domain use cases.
- Finance/FinOps representative for paid providers, high-volume usage, or budget policy.
- Legal/Compliance representative for high-impact employment, regulated, cross-border, or
  contractual-risk scenarios.
- Solution Architect for architecture-significant changes.

Board responsibilities:

- Approve new AI providers, new production models, provider fallback strategies, and major
  model replacements.
- Approve material prompt-library changes, safety policy changes, grounding/confidence
  policy changes, evaluation policy updates, and cost-policy changes.
- Approve major RAG architecture changes, vector-store strategy changes, memory/cache policy
  changes, and tenant/data-scope changes.
- Review canary outcomes, business KPIs, incident learnings, recurring exceptions, expired
  approvals, and drift signals.
- Accept, reject, or time-bound residual risk; critical tenant isolation, privacy, security,
  prohibited-use, or legal gaps cannot be accepted as normal business risk.

Workflow:

1. Change owner submits a decision pack containing purpose, scope, impacted tenants/data,
   lifecycle stage, evaluation evidence, business KPI expectations, cost impact, security and
   privacy assessment, rollback plan, tenant communication impact, and requested decision.
2. Board validates prerequisites and either approves, rejects, requests changes, or grants a
   time-bound conditional approval with owners and expiry.
3. Approved decisions are recorded as immutable operational records and linked to bundle,
   policy, ADR, ORR, incident, or release evidence.
4. Conditional approvals are automatically reviewed before expiry; expired approvals block
   promotion or expansion.

Cadence and emergency process:

- Standard cadence is at least monthly while AI capabilities are in active development or
  production operation.
- High-risk or production-impacting changes require explicit quorum defined by governance
  policy.
- Emergency approval may be granted by the designated Product/AI, Operations, Security, and
  Data Governance approvers for containment, rollback, provider disablement, policy tightening,
  or urgent safety/cost control.
- Emergency approvals are time-bound, audited, and reviewed by the full board at the next
  available meeting.

---

# 35. Runbook Reference Matrix

Incident responders use this matrix to quickly locate the primary runbook. Some incidents
require multiple runbooks; the incident commander decides the active path and supporting
paths.

| Incident or operational condition | Primary runbook |
|---|---|
| Provider outage, throttling, provider behavior drift, or degraded model response | AI-RUN-001 |
| Qdrant outage, shard/collection issue, snapshot failure, or vector-index corruption | AI-RUN-002 |
| Latency/SLO degradation, capacity saturation, noisy-neighbor, or traffic surge | AI-RUN-003 |
| Retrieval quality, citation, groundedness, refusal, or hallucination regression | AI-RUN-004 |
| Prompt injection, data leakage, cross-tenant incident, unsafe content, or excessive tool attempt | AI-RUN-005 |
| AI cost spike, quota exhaustion, budget reservation failure, or billing anomaly | AI-RUN-006 |
| Telemetry pipeline outage, dashboard failure, or alert routing failure | AI-RUN-007 |
| Ingestion backlog, failed source publication, or index-publication stall | AI-RUN-008 |
| Cache poisoning, stale cache hit, namespace issue, or invalidation failure | AI-RUN-009 |
| Conversation memory corruption, purpose drift, role-matrix change, or authorization drift | AI-RUN-010 |
| Evaluation failure, approval expiry, quality drift, or hallucination regression | AI-RUN-011 |
| Tenant deletion, offboarding, legal-hold conflict, or provider residual-state issue | AI-RUN-012 |
| Redis outage, failover, corruption, saturation, or safe memory/cache bypass | AI-RUN-013 |
| Event/outbox backlog, dead-letter growth, invalidation failure, or replay need | AI-RUN-014 |
| Backup restore, disaster recovery, regional dependency event, or integrity loss | AI-RUN-015 |
| Prompt/model/embedding/index/config rollback | AI-RUN-016 |
| Secret/key compromise or emergency credential rotation | AI-RUN-017 |
| Retention, archival, legal-hold, backup-erasure, or restore-time deletion failure | AI-RUN-018 |

---

# 36. Future AI Agent Operations - Reserved for Future Capability

This section is intentionally reserved. The current architecture does not authorize
autonomous AI agents or agent-to-agent workflow execution. Future agent capability must not
be introduced informally through prompts, tools, background workers, or customer-specific
customization.

Before any AI agent capability enters design or implementation, a dedicated architecture and
operations package must define:

- Agent lifecycle management, approval, canary, rollback, deprecation, and retirement.
- Agent registration, ownership, purpose boundaries, tenant scope, and data classification.
- Agent health monitoring, liveness, readiness, task queues, timeout, retry, and stop rules.
- Multi-agent orchestration, handoff, supervision, and failure isolation.
- Agent permission boundaries using RBAC, ABAC, tool scopes, policy-as-data, and explicit
  denial of unauthorized state-changing action.
- Agent-to-agent communication contracts, event schemas, correlation, idempotency, and audit.
- Agent memory governance, including separation from conversation memory and future Workspace
  Memory.
- Agent versioning, deployment bundles, model/prompt/tool compatibility, and rollback.
- Agent observability, business KPIs, cost attribution, safety metrics, and evaluation gates.
- Agent-specific incident handling for runaway loops, excessive agency, tool misuse,
  cross-tenant leakage, harmful output, cost amplification, and unavailable supervisors.

Any future agent operations design must preserve the same constitutional rules: tenant
isolation, RBAC/ABAC/audit, event-driven contracts, OpenAPI documentation, approved
five-document feature set, and no hardcoded business rules.

---

# 37. Acceptance Criteria Before Approval/Implementation

| ID | Criterion |
|---|---|
| OPS-AC-001 | Every production AI component has a named accountable owner, dependency map, classification, SLO, capacity limit, RPO/RTO, dashboard, alerts, and approved runbook. |
| OPS-AC-002 | Production on-call has primary/secondary coverage, tested escalation, least-privilege access, provider/tenant contacts, training, and handoff. |
| OPS-AC-003 | Production and non-production credentials, tenant data, provider accounts, Qdrant, Redis, storage, and telemetry are separated. |
| OPS-AC-004 | Deployments bind immutable application, prompt/model/index/policy/cache/memory/evaluation and telemetry versions plus a compatible rollback manifest. |
| OPS-AC-005 | SLO/error-budget policies are effective-dated, use eligible-request definitions and multi-window burn alerts, and cannot weaken tenant/security/quality controls. |
| OPS-AC-006 | Platform, quality, security, FinOps, executive, and tenant dashboards enforce approved data scope and contain no prohibited sensitive telemetry. |
| OPS-AC-007 | Every page is actionable, severity-routed, deduplicated/inhibited, linked to a dashboard/runbook, and tested. |
| OPS-AC-008 | SEV-0/SEV-1 incidents assign command, operations, security, communications, domain, provider, and timeline roles with protected evidence. |
| OPS-AC-009 | Degraded mode follows safe retry, approved fallback, retrieval-only, then unavailable; ungrounded or unauthorized fallback is impossible. |
| OPS-AC-010 | Emergency changes are scoped, approved, time-bound, monitored, reversible, audited, and cannot bypass critical controls. |
| OPS-AC-011 | Provider/model operations pin identity where possible, monitor behavior drift, enforce residency/budget/capability, and rehearse approved fallback. |
| OPS-AC-012 | Qdrant operations monitor cluster/shard/storage/snapshot health and use isolated restore/rebuild plus tenant/filter/effective-date/quality validation before activation. |
| OPS-AC-013 | Redis operations use an approved topology, safe memory/cache bypass, workload isolation, tested failover, namespace/TTL/deletion checks, and controlled warm-up. |
| OPS-AC-014 | Ingestion is idempotent, staged, malware/content validated, tenant-version traced, backpressured, reconciled, and publishes only an evaluated complete index. |
| OPS-AC-015 | Evaluation failure/expiry/drift freezes promotion and critical quality/security/harm regressions trigger scoped disablement or full-bundle rollback. |
| OPS-AC-016 | Cost operations detect and contain reservation, forecast, price, credential, retry/fallback, cache-loss, and provider-billing anomalies without blocking mandatory controls. |
| OPS-AC-017 | Security monitoring covers injection, leakage, extraction, cross-tenant, poisoning, tools, credentials, denial/cost amplification, and prohibited employment behavior. |
| OPS-AC-018 | Durable events use outbox, idempotent consumers, versioned contracts, bounded retry, dead letters, fair scheduling, reconciliation, and approved replay. |
| OPS-AC-019 | Capacity/load tests cover multi-tenant/noisy-neighbor, provider throttle/outage, cache cold start, ingestion burst, failover, cost, quality, and security invariants. |
| OPS-AC-020 | Backup/DR defines dependency-ordered RPO/RTO and validates isolated restore, RLS/tenant isolation, deletion tombstones, integrity, source/index/cost/event/quality state. |
| OPS-AC-021 | ADR-022-approved retention, deletion, legal hold, tenant offboarding, backup erasure, provider residual state, and restore-time reconciliation are operationally testable. |
| OPS-AC-022 | Vulnerability/patch management inventories all AI infrastructure, dependencies, adapters, providers, licenses, support dates, remediation, rollback, and validation. |
| OPS-AC-023 | Durable incident/change/exercise/ORR records use tenant isolation, audit/version columns, integrity, access controls, and cannot be replaced by sampled telemetry. |
| OPS-AC-024 | Tenant communications are scoped, approved, timely, factual, localized where required, and expose no other tenant or sensitive evidence. |
| OPS-AC-025 | Runbooks AI-RUN-001 through AI-RUN-018 contain detection, containment, diagnosis, recovery, validation, communication, rollback/stop, reconciliation, and closure. |
| OPS-AC-026 | ORR blocks production when ownership, docs, OpenAPI, security, evaluation, observability, capacity, runbooks, DR, retention/deletion, or critical-risk evidence is missing/expired. |
| OPS-AC-027 | Exercises technically validate provider/Qdrant/Redis/queue/telemetry/rollback/deletion/DR controls at approved cadence and track findings to retest. |
| OPS-AC-028 | Operational APIs are versioned, OpenAPI-documented, tenant-isolated, RBAC/ABAC protected, idempotent, audited, rate-limited, and never expose prohibited content. |
| OPS-AC-029 | Core HRMS remains available when AI, provider, vector store, Redis, evaluation, or telemetry capabilities are disabled. |
| OPS-AC-030 | No outage, capacity event, or recovery action automatically activates a paid service, broader data scope, stale content, or unapproved provider. |
| OPS-AC-031 | Unit coverage is at least 85%, with integration, isolation, security, performance, chaos/failover, restore, deletion, replay, operational API, and end-to-end tests. |
| OPS-AC-032 | Every production AI model or provider deployment follows the full Draft/Evaluation/Approved/Canary/Production/Deprecated/Retired lifecycle with immutable bundle identity and rollback evidence. |
| OPS-AC-033 | Business KPI definitions, dashboards, review cadence, and owners are approved for each production AI use case and kept separate from operational SLO compliance. |
| OPS-AC-034 | Significant AI changes are reviewed by an AI Governance Board with recorded decision packs, quorum/approval rules, emergency approval controls, and expiry for conditional decisions. |
| OPS-AC-035 | Incident response materials include a runbook reference matrix mapping common operational/security/cost/quality/DR conditions to AI-RUN-001 through AI-RUN-018. |
| OPS-AC-036 | Autonomous AI agent capabilities remain prohibited until a dedicated approved architecture, operations, security, database, API/OpenAPI, UI, and test package exists. |
| OPS-AC-037 | Governance-board decisions, lifecycle transitions, KPI reviews, emergency approvals, and retirement records are tenant-safe, auditable, and linked to supporting evidence. |

---

# 38. Official and Primary References

- Google SRE Workbook - Alerting on SLOs:
  `https://sre.google/workbook/alerting-on-slos/`
- Google SRE Workbook - Incident Response:
  `https://sre.google/workbook/incident-response/`
- OpenTelemetry Collector:
  `https://opentelemetry.io/docs/collector/`
- OpenTelemetry generative AI semantic conventions:
  `https://opentelemetry.io/docs/specs/semconv/gen-ai/`
- Prometheus alerting practices:
  `https://prometheus.io/docs/practices/alerting/`
- NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for
  Cybersecurity Risk Management:
  `https://csrc.nist.gov/pubs/sp/800/61/r3/final`
- NIST AI Risk Management Framework:
  `https://www.nist.gov/itl/ai-risk-management-framework`
- Qdrant monitoring guidance:
  `https://qdrant.tech/documentation/guides/monitoring/`
- Redis Sentinel documentation:
  `https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/`
- OWASP prompt injection risk:
  `https://genai.owasp.org/llmrisk/llm01-prompt-injection/`
- FinOps Framework - Budgeting:
  `https://www.finops.org/framework/capabilities/budgeting/`

References were selected as primary/official sources. Product/provider behavior, security
guidance, and regulatory obligations must be revalidated before implementation and each
material production change.

References last validated: 2026-06-25.

---

# Approval

Platform/Operations Architect: Drafted by Codex 2026-06-25  
Solution Architect: ____  
Security Architect: ____  
Data Governance/Privacy: ____  
Database Architect: ____  
Product/AI Owner: ____  
HR/Payroll Domain Owner: ____  
Product Owner: Approved by Bhajan Lal 2026-06-27

(Status: Approved - owner approved 2026-06-27)
