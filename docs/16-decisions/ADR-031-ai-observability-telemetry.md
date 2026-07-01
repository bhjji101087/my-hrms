# ADR-031 - AI Observability and Telemetry

Architecture Decision Record

Date: 2026-06-23
Status: Approved
Approved By: Bhajan Lal (Product Owner)
Approved Date: 2026-06-23

Related documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md` - Approved v2.1
- ADR-005 Multi-Tenancy Model
- ADR-006 Tenant Context and Data Access
- ADR-008 Identity and Access Management
- ADR-009 Event-Driven Backbone
- ADR-019 Enterprise AI/RAG Platform Architecture - Approved
- ADR-027 Provider-Abstraction Framework - Approved
- ADR-030 Enterprise Vector Store Strategy - Approved

---

# Context

The AI platform has more failure modes than a normal API. A request may pass through tenant
and permission policy, conversation context, semantic cache, Qdrant retrieval, reranking,
read-only HR tools, an external model provider, output guardrails, citation validation, and
confidence calculation. A successful HTTP response can still be slow, costly, weakly
grounded, over-refusing, or operating in fallback mode.

The platform must therefore observe:

- End-to-end and stage-level latency.
- Qdrant, cache, model, embedding, reranker, tool, and guardrail health.
- Token consumption, estimated cost, cache effectiveness, and fallback activity.
- Retrieval quality, citations, refusals, hallucination incidents, and user feedback.
- Security detections, blocked responses, anomalous usage, and tenant-isolation incidents.
- Service-level objectives (SLOs), alerting, incident response, and runbook execution.

The user has chosen a cost-conscious initial-development approach. Observability must work
without a paid managed monitoring service while preserving a plug-in path to managed tools
later. Telemetry must not become a second store of sensitive HR content.

---

# Decision

## 1. Standardize application telemetry on OpenTelemetry

All AI application code emits metrics, traces, and structured logs through OpenTelemetry
APIs/SDKs and the OpenTelemetry Protocol (OTLP). Application code does not reference a
monitoring-vendor SDK.

An OpenTelemetry Collector receives, filters, redacts, samples, batches, and routes
telemetry. Backend switching happens through collector/exporter deployment configuration,
not AI feature-code changes.

OpenTelemetry generative-AI semantic conventions may be mapped where they are stable and
fit the platform. Because those conventions evolve, the platform maintains a versioned,
vendor-neutral `hrms.ai.*` telemetry contract and maps it to external conventions in the
collector or adapter layer.

## 2. Use a self-hosted open-source stack for initial development

The initial local/development stack is:

| Signal/capability | Initial component | Purpose |
|---|---|---|
| Instrumentation and transport | OpenTelemetry SDK + Collector | Vendor-neutral collection and routing |
| Metrics | Prometheus | Time-series metrics and SLO inputs |
| Dashboards | Grafana OSS | Operations, quality, security, and executive views |
| Logs | Loki | Structured operational logs without sensitive content |
| Traces | Tempo | Distributed request and stage traces |
| Alerts | Prometheus Alertmanager | Routing, grouping, inhibition, and escalation |

These components may run locally/self-hosted, so initial development does not require a
paid observability subscription. Production self-hosting still requires compute, storage,
backup, upgrades, monitoring, security, and operational ownership.

Qdrant health and metrics are collected from its supported monitoring endpoints. AI
application spans correlate Qdrant operations through trace/correlation identifiers; no
query vectors or retrieved source text are exported.

## 3. Keep managed backends replaceable

Managed backends such as Azure Monitor/Application Insights, Grafana Cloud, Datadog, or
New Relic may be adopted later by adding/configuring an approved OpenTelemetry exporter.
The application instrumentation and `hrms.ai.*` telemetry contract remain unchanged.

The operational backend is environment/platform configuration, not a tenant-selectable
business setting. A future customer-specific telemetry export requires a separate security
and data-processing decision so one tenant can never receive platform or another tenant's
operational data.

## 4. Define one trace across the complete AI request

Each AI request has `TraceId`, `SpanId`, `CorrelationId`, and `AiRequestId`. The trace
contains bounded spans for:

1. `ai.request`
2. `ai.policy.evaluate`
3. `ai.memory.load`
4. `ai.cache.lookup`
5. `ai.retrieval.query`
6. `ai.vector.search`
7. `ai.rerank`
8. `ai.tool.call` for each allow-listed read tool
9. `ai.prompt.assemble`
10. `ai.model.generate`
11. `ai.guardrail.output`
12. `ai.citation.validate`
13. `ai.confidence.evaluate`
14. `ai.usage.record`

Skipped stages are marked as skipped with a bounded reason. Fallback attempts are child
spans linked to the original provider attempt. Retry attempts are visible but bounded to
prevent telemetry amplification.

Approved low-cardinality attributes include:

- Use case and request outcome.
- Environment, region, service version, and tenant service tier.
- Provider/model registry key, prompt version, index version, and retrieval profile.
- Cache status, fallback state, confidence band, refusal category, and error category.
- Tool key and guardrail/policy version.

Raw `TenantId`, user/employee IDs, email, document IDs, source text, query text, prompt,
response, vector, secret, access token, and tool payload are prohibited telemetry
attributes.

## 5. Adopt a bounded AI metric catalog

Metric names and labels are versioned. Labels use controlled enumerations; dynamic text and
identifiers are forbidden.

| Metric | Type | Required dimensions |
|---|---|---|
| `hrms_ai_requests_total` | Counter | use case, outcome, region |
| `hrms_ai_request_duration_seconds` | Histogram | use case, outcome |
| `hrms_ai_stage_duration_seconds` | Histogram | stage, outcome |
| `hrms_ai_provider_requests_total` | Counter | provider key, model class, outcome |
| `hrms_ai_provider_failures_total` | Counter | provider key, error category |
| `hrms_ai_fallback_activations_total` | Counter | source provider, target provider, reason |
| `hrms_ai_tokens_total` | Counter | provider key, model class, direction, cache state |
| `hrms_ai_estimated_cost` | Counter | provider key, model class, use case, currency |
| `hrms_ai_cache_operations_total` | Counter | cache type, hit/miss/stale/rejected |
| `hrms_ai_retrieval_requests_total` | Counter | outcome, retrieval profile |
| `hrms_ai_retrieval_documents` | Histogram | use case, outcome |
| `hrms_ai_citation_completeness` | Histogram | use case, confidence band |
| `hrms_ai_refusals_total` | Counter | use case, refusal category |
| `hrms_ai_quality_incidents_total` | Counter | incident category, severity |
| `hrms_ai_security_blocks_total` | Counter | detector category, severity |
| `hrms_ai_ingestion_jobs_total` | Counter | source type, outcome |
| `hrms_ai_ingestion_lag_seconds` | Gauge | source type, priority class |

Per-tenant token/cost/quota records belong in the durable tenant usage ledger governed by
ADR-033, not Prometheus labels. This prevents tenant identifiers from leaking into metrics
and prevents unbounded time-series cardinality.

## 6. Use structured logs for operational events only

Structured logs record event type, time, service/version, trace/correlation IDs, bounded
outcome/error category, provider/model registry keys, prompt/index versions, duration, and
retry/fallback state.

Logs must not contain:

- Prompt or response content.
- Retrieved source text or embeddings.
- Employee, payroll, health, disciplinary, attendance, or identity data.
- Raw tenant/user/document identifiers.
- API keys, tokens, connection strings, or provider request/response bodies.

Security audit, business audit, and AI interaction audit remain separate durable records.
Operational logs are not the legal audit system of record.

## 7. Protect tenant privacy and control cardinality

- Metrics never use `TenantId`, `UserId`, `EmployeeId`, `DocumentId`, conversation ID, or
  request text as labels.
- Restricted traces/logs may carry a rotating HMAC tenant reference solely for authorized
  platform support correlation. It cannot be reversed without the protected mapping.
- Tenant administrators receive tenant-scoped aggregates through authorized HRMS APIs and
  dashboards, not direct access to the shared observability backend.
- Platform operations may view cross-tenant service health under dedicated RBAC/ABAC and
  audit, but cannot view prompt/response content.
- Debug content capture is disabled by default in every environment. Any future break-glass
  capture requires a separate approved policy, explicit purpose, encryption, short expiry,
  restricted access, and full audit.
- Collector processors enforce redaction and reject prohibited attributes before export.
- CI tests fail when metric labels or log schemas introduce dynamic/high-cardinality or
  sensitive fields.

## 8. Establish initial SLOs and error budgets

The approved AI Strategy sets these initial configurable targets:

| SLO | Initial target | Measurement |
|---|---|---|
| AI API availability | >= 99.9% per calendar month | Successful eligible requests / total eligible requests |
| Retrieval latency | p95 <= 1.5 seconds | `ai.retrieval.query` plus `ai.vector.search` duration |
| Full knowledge-answer latency | p95 <= 10 seconds | Accepted `ai.request` duration |
| Citation completeness | >= 98% on approved policy benchmark | ADR-034 evaluation output |
| Cross-tenant retrieval incidents | 0 | Security incident and canary-test results |
| Critical alert detection | <= 5 minutes | Event occurrence to alert creation |

Targets are effective-dated service configuration and may vary by approved service tier.
No cost, availability, or latency target may weaken tenant isolation, permission checks,
grounding, citation validation, or output safety.

Availability excludes requests correctly rejected by authentication, authorization,
budget, quota, safety, or validation policy. Provider fallback that returns a valid answer
counts as available but is separately measured.

Use multi-window error-budget burn alerts rather than alerting on every isolated failure.
Error-budget exhaustion blocks risky model/prompt/index promotions until owner and
operations approval.

Contractual SLA reports are derived from the approved SLO measurements but remain separate
from internal engineering targets. A tenant can see only its own SLA results through an
authorized application report. SLA terms, exclusions, service credits, and reporting
periods are commercial configuration and are never hardcoded in telemetry logic.

## 9. Provide role-specific dashboards

### Platform operations dashboard

- Availability, latency percentiles, throughput, saturation, queue/ingestion lag.
- Qdrant, model, embedding, reranker, cache, collector, and exporter health.
- Provider errors, circuit state, retries, fallback rate, and degraded mode.

### AI quality dashboard

- Retrieval hit/no-result rate, citation completeness, confidence distribution.
- Refusal rate, false-refusal review, hallucination incidents, and feedback trend.
- Prompt/model/index versions and evaluation-regression status.

### Security dashboard

- Prompt-injection/jailbreak detections, output leakage blocks, tool denials.
- Anomalous extraction patterns, cross-tenant canary results, and security incidents.
- No raw prompts, answers, source content, or employee data.

### Executive/Product dashboard

- Adoption, successful grounded answers, quality trend, availability, and estimated cost.
- Aggregated by approved product/use-case dimensions, not individual employees.

### Tenant administrator dashboard

- Own tenant's usage, latency, quality, budget status, fallback, and service health.
- Delivered through tenant-scoped application APIs with RBAC/ABAC and audit.

## 10. Classify and route actionable alerts

| Severity | Examples | Required response |
|---|---|---|
| SEV-0 | Suspected cross-tenant disclosure, confirmed sensitive-data leakage | Immediately block affected path, page Security/Operations, preserve protected evidence, start breach runbook |
| SEV-1 | AI service unavailable, Qdrant unavailable, fallback storm, widespread provider failure | Page on-call, activate degraded mode/failover runbook, publish service status |
| SEV-2 | SLO burn, sustained latency, quality/citation regression, ingestion backlog, abnormal refusal rise | Notify owning team, create tracked incident, investigate within service target |
| SEV-3 | Capacity forecast, low-risk dashboard/config drift, non-urgent optimization | Work queue and planned remediation |

Alert routing uses the approved notification abstraction. Alerts are grouped, deduplicated,
inhibited during a parent outage, and linked to a runbook and dashboard. Alert thresholds
are configuration, not hardcoded application rules.

## 11. Require operational runbooks

ADR-031 requires these runbooks, which are expanded in the Phase 6C AI Operations
Handbook:

- `AI-RUN-001` Model/provider outage and fallback storm.
- `AI-RUN-002` Qdrant outage, corruption, restore, and re-index.
- `AI-RUN-003` Latency/SLO degradation and capacity saturation.
- `AI-RUN-004` Citation, groundedness, refusal, or hallucination regression.
- `AI-RUN-005` Prompt injection, data leakage, and cross-tenant incident.
- `AI-RUN-006` Token/cost spike, credential abuse, and quota exhaustion.
- `AI-RUN-007` Telemetry collector/exporter/backend outage.
- `AI-RUN-008` Ingestion backlog and index-promotion failure.
- `AI-RUN-009` Cache poisoning, staleness, and invalidation failure.

Each runbook defines detection, owner, severity, containment, diagnosis, recovery,
validation, communication, rollback, and post-incident review.

## 12. Make observability failure non-blocking but visible

- Telemetry export is asynchronous with bounded buffers, batching, backpressure, and
  circuit breakers.
- A monitoring-backend outage must not block a valid AI response.
- Collector/export failure emits a local health signal and follows `AI-RUN-007`.
- When buffers fill, normal successful traces/logs may be sampled or dropped according to
  policy; security events, business audit, and durable usage/cost records use their own
  reliable event/outbox paths and are never treated as optional telemetry.
- Telemetry components must not recursively flood themselves during an outage.

## 13. Apply environment-aware sampling and retention

- Metrics are aggregated continuously and remain low-cardinality.
- Local development/test may retain 100% traces for a short window.
- Production uses tail-based sampling: retain all errors, security blocks, fallback,
  degraded-mode, slow, and anomalous traces; sample routine successful requests at a
  configurable rate.
- Debug logging is disabled in production by default.
- Initial cost-conscious defaults: local raw telemetry <= 7 days; production detailed
  traces/logs <= 7 days; detailed operational metrics <= 30 days. Longer trends use
  low-cardinality aggregates outside the raw telemetry backend.
- Final retention, deletion, legal hold, and backup rules are governed by ADR-022. A tenant
  offboarding/deletion workflow removes eligible tenant-correlated telemetry and mappings.

## 14. Separate monitoring from durable AI governance records

Observability signals are optimized for operations. The following require durable,
tenant-scoped records outside Prometheus/Loki/Tempo:

- Per-tenant token, request, provider cost, budget, and quota decisions - ADR-033.
- Prompt/model/index promotion and evaluation evidence - ADR-034.
- Security and business audit events - Audit architecture and security specification.
- Conversation and memory lifecycle - ADR-032.

Durable records may emit aggregate telemetry, but telemetry cannot replace their source of
truth.

---

# Alternatives Considered

## Use Azure Monitor/Application Insights first

Strong managed integration, but introduces a paid dependency during initial development
and increases early vendor coupling. Rejected as the first backend; retained as a later
OpenTelemetry exporter option.

## Instrument directly with each monitoring vendor's SDK

May expose vendor-specific features quickly, but requires application changes to switch
backends and fragments telemetry semantics. Rejected.

## Use logs only

Logs cannot efficiently provide latency distributions, SLO/error-budget calculations,
stage traces, or reliable alerting. Rejected.

## Build a custom telemetry platform

Creates unnecessary platform and operational burden. Rejected in favor of established
OpenTelemetry and open-source observability components.

## Store full prompts, answers, and retrieved context for debugging

Improves debugging but creates an unacceptable secondary store of sensitive tenant and HR
data. Rejected as the default. Any exceptional capture requires a separate approved
break-glass policy.

## Delay observability until after AI features are built

Would make quality, cost, security, and failure behavior impossible to validate and would
create expensive rework. Rejected.

---

# Consequences

## Positive

- Initial development requires no paid monitoring subscription.
- Application code remains independent of the observability backend.
- One trace explains latency and failures across the complete AI request.
- SLOs, quality, cost, fallback, Qdrant, and security behavior become measurable.
- Sensitive HR content is excluded from normal telemetry by design.
- Managed monitoring can be adopted later through exporter configuration.

## Negative

- The self-hosted development stack adds containers, storage, dashboards, and configuration.
- Production self-hosting requires upgrades, backup, scaling, and on-call ownership.
- Privacy and cardinality controls limit some ad-hoc debugging.
- Quality metrics depend on ADR-034 evaluation and human incident labeling.
- Additional durable stores are still required for audit and per-tenant cost governance.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Sensitive content enters telemetry | Prohibited-field schema, collector redaction/drop, CI scanning, no content capture by default |
| High-cardinality metrics overload Prometheus | Bounded dimensions, no tenant/user/request IDs as labels, cardinality tests and budgets |
| Monitoring outage affects AI | Asynchronous bounded export; separate durable audit/usage paths; backend outage runbook |
| Self-hosted stack becomes operational burden | Version-pinned deployment, retention limits, health checks, IaC, later OTLP managed exporter option |
| Alert fatigue | SLO burn alerts, grouping, deduplication, inhibition, severity/runbook requirements |
| Tenant admin sees another tenant | Tenant-scoped application API, RBAC/ABAC, no direct shared-backend access, isolation tests |
| Provider metric semantics differ | Versioned internal metric contract and adapter normalization |
| Sampling hides an incident | Retain all error/security/fallback/slow traces; metrics remain unsampled |

---

# Acceptance Criteria Before Approval/Implementation

| ID | Criterion |
|---|---|
| OT-AC-001 | Application instrumentation uses OpenTelemetry/OTLP and contains no monitoring-vendor SDK dependency. |
| OT-AC-002 | Local development can run metrics, dashboards, logs, traces, and alerts without a paid managed service. |
| OT-AC-003 | A single trace shows all applicable AI stages, retries, provider attempts, and fallback outcome. |
| OT-AC-004 | Automated tests prove prompts, answers, source text, vectors, secrets, employee IDs, and raw tenant/user IDs are absent from exported telemetry. |
| OT-AC-005 | Metrics pass cardinality budgets and contain no dynamic identifier labels. |
| OT-AC-006 | Platform, quality, security, executive, and tenant-admin dashboards enforce their approved scopes. |
| OT-AC-007 | SLO calculations reproduce availability, retrieval/full-answer latency, citation, isolation, and alert-detection targets. |
| OT-AC-008 | Simulated model and Qdrant failures produce traces, provider/fallback metrics, alerts, and linked runbooks. |
| OT-AC-009 | Suspected cross-tenant or sensitive-data leakage generates a SEV-0 alert within five minutes and blocks the affected path. |
| OT-AC-010 | An observability-backend outage does not block valid AI responses and does not lose durable security/audit/usage events. |
| OT-AC-011 | Tail sampling retains all errors, security blocks, fallback, degraded, and slow traces. |
| OT-AC-012 | Tenant administrators can access only their tenant's aggregates through authorized APIs; cross-tenant tests return no data. |
| OT-AC-013 | Switching from the self-hosted backend to a test managed exporter requires collector/deployment configuration only, with no AI feature-code change. |
| OT-AC-014 | Retention/deletion tests enforce environment policy and approved ADR-022 rules when available. |
| OT-AC-015 | Dashboards, alerts, runbooks, metric catalog, and telemetry schema are version-controlled and reviewed with the release. |
| OT-AC-016 | Tenant SLA reporting is derived from SLO evidence, tenant-isolated, and configurable without telemetry-code changes. |

---

# Impact

## Architecture

Adds OpenTelemetry instrumentation, Collector, self-hosted Prometheus/Grafana/Loki/Tempo/
Alertmanager for initial development, a versioned AI telemetry contract, SLO/error-budget
management, role-specific dashboards, and runbook-linked alerting.

## Database

No operational metrics are stored in SQL Server. ADR-033 defines the durable tenant usage
and cost ledger. Restricted tenant-correlation mappings, if required, must be encrypted,
access-controlled, auditable, and designed in the AI database document.

## Security

Introduces strict telemetry data classification, redaction, cardinality controls,
tenant-scoped dashboard access, restricted platform-operations access, and AI-specific
security alerts. Telemetry is not a bypass around audit retention or authorization.

## Performance

Instrumentation must be asynchronous and bounded. Load tests measure instrumentation
overhead and exporter backpressure. Sampling reduces trace/log volume without sampling
away metrics or durable security/audit/usage records.

## Development

Technical design and test documents must define instrumentation helpers, metric schemas,
collector configuration, dashboards, alerts, and runbook ownership. No implementation
starts until the constitutional five-document set and OpenAPI are Approved.

## Operations

Operations owns the collector/backend lifecycle, retention, capacity, alerts, on-call
routing, and runbooks. Product/AI owners own quality thresholds and incident classification;
Security owns sensitive-data and cross-tenant alerts.

---

# Official References

- OpenTelemetry documentation: `https://opentelemetry.io/docs/`
- OpenTelemetry .NET: `https://opentelemetry.io/docs/languages/net/`
- OpenTelemetry generative AI conventions:
  `https://opentelemetry.io/docs/specs/semconv/gen-ai/`
- Prometheus overview: `https://prometheus.io/docs/introduction/overview/`
- Grafana open-source projects: `https://grafana.com/oss/`
- Qdrant monitoring: `https://qdrant.tech/documentation/guides/monitoring/`

References last validated: 2026-06-23.

---

# Approval

Solution Architect: Approved (Agent 6 / Codex)  
Security Architect: ____  
Platform/Operations Architect: ____  
.NET Architect: ____  
Prompt/Context Engineer: ____  
Product Owner: Bhajan Lal - Approved 2026-06-23

(Status: Approved)
