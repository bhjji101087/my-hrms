# ADR-019 - Enterprise AI / RAG Platform Architecture

Architecture Decision Record

Date: 2026-06-14
Last Updated: 2026-06-23
Status: Approved
Approved By: Bhajan Lal (Product Owner)
Approved Date: 2026-06-23

Related documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md` - Approved v2.1
- ADR-004 Modular Monolith
- ADR-005 Multi-Tenancy Model
- ADR-006 Tenant Context and Data Access
- ADR-008 Identity and Access Management
- ADR-009 Event-Driven Backbone
- ADR-027 Provider-Abstraction Framework
- ADR-030 Vector Store Strategy - Approved companion decision

---

# Context

The HRMS requires an enterprise AI layer for policy and payroll questions, employee
lookup, report and workflow drafting, proactive insights, and anomaly explanation. These
capabilities process sensitive tenant knowledge and may read live HR data, so a normal
chatbot architecture is insufficient.

The architecture must provide:

- Grounded answers with citations and explicit low-confidence behavior.
- Absolute tenant isolation and current RBAC plus ABAC enforcement.
- Pluggable LLM, embedding, and vector-store providers.
- Versioned prompts, models, indexes, policies, and evaluation evidence.
- Conversation continuity without creating unauthorized long-term profiles.
- Cost, quality, security, availability, and operational controls.
- Human-controlled actions through existing domain workflows only.
- A modular-monolith implementation that can be extracted later without redesign.

The earlier version of this ADR selected basic RAG, a multi-provider LLM abstraction, and
per-tenant vector storage. The approved AI Strategy v2.1 adds the enterprise controls and
clear service boundaries needed before implementation.

---

# Decision

## 1. AI is a governed platform module

Create a bounded `AI` platform module inside the modular monolith. It owns orchestration,
prompt/context policy, knowledge ingestion coordination, confidence evaluation, usage and
cost accounting, AI audit metadata, and provider resolution.

Business modules expose permission-scoped contracts and domain events. They do not call
vendor models directly and do not place provider SDK types in domain or application code.
The AI module can be extracted into a separate service later if independent scaling,
residency, or deployment needs justify it.

## 2. Use two controlled answer paths

1. **Knowledge answer path:** approved tenant documents are retrieved through RAG. Every
   material claim requires a valid citation. Missing, expired, conflicting, or weak
   evidence produces a refusal, caution, or human escalation.
2. **Structured-data answer path:** live employee, payroll, leave, attendance, and workflow
   data is accessed only through allow-listed, permission-scoped read APIs. Live HR records
   are not embedded in the vector store.

The context orchestrator may combine both paths only after each source has independently
passed tenant, permission, sensitivity, effective-date, and purpose checks.

## 3. Apply provider abstraction to every AI dependency

Core AI code depends on these provider-neutral categories:

- `ILlmProvider` for generation and supported model capabilities.
- `IEmbeddingProvider` for document/query embeddings.
- `IVectorStore` for versioned indexing and authorized retrieval.
- `IProviderResolver<T>` from ADR-027 for tenant-specific selection, health, and fallback.

Vendor SDKs live only in adapter projects. Exact model identifiers, embedding dimensions,
prices, regions, capabilities, and deprecation dates are effective-dated registry data,
not feature-code constants.

The first adapters are selected by approved deployment needs. Anthropic, OpenAI, and
Google model providers may be supported, but no single vendor is a core dependency. Vector
store selection is delegated to ADR-030.

## 4. Enforce tenant and permission isolation before every AI operation

- Trusted tenant context comes from ADR-006. Request content never supplies a trusted
  `TenantId`.
- The caller's current identity, roles, and server-resolved ABAC attributes are evaluated
  before retrieval, memory access, cache access, read-tool calls, and output release.
- Vector data uses a hard provider-native tenant partition or a dedicated tenant index as
  defined in ADR-030. Shared metadata filtering alone is not an isolation boundary.
- Retrieved chunks are revalidated for tenant and permissions before prompt assembly.
- Conversation memory, caches, evaluation data, usage/cost records, and AI audit records
  are tenant-scoped and permission-partitioned.
- Background work executes under an explicit, audited tenant system context.
- Cross-tenant negative tests are mandatory in CI and release validation.

## 5. AI cannot directly change business state

The AI service cannot invoke state-changing domain operations. It may return a
non-executable recommendation or navigation suggestion. The user must initiate any change
through the normal domain UI/API, where authorization, validation, workflow, maker-checker,
idempotency, and audit are applied independently of AI.

Workflow and report generation produce drafts only. AI cannot publish workflows, approve
requests, modify payroll, change employee data, or activate configuration.

## 6. Grounding, confidence, and explainability are response requirements

Knowledge responses include:

- Answer and material-claim citations.
- Overall confidence score and band.
- Retrieval, source-quality, and citation-completeness components.
- A short explanation of missing, stale, or conflicting evidence.
- Prompt, model-registry, and index versions for traceability.

Scores are calibrated against approved benchmark data and are not presented as legal or
mathematical certainty. Configurable thresholds determine normal, cautious, refusal, and
human-escalation behavior. A critical conflict or unsupported policy/payroll claim must be
refused regardless of aggregate score.

## 7. Treat prompts and AI configuration as immutable versioned data

Prompts, tool schemas, model assignments, fallback policy, safety policy, confidence
thresholds, budgets, memory policy, cache policy, and evaluation gates follow:

`Draft -> Validate -> Security/Evaluation Review -> Publish -> Supersede`

Published versions are immutable. Each request remains pinned to the versions resolved at
its start. Promotion uses sandbox-to-production controls, audit reason, effective date,
and rollback version.

## 8. Apply layered AI security controls

- Input validation, abuse limits, jailbreak and prompt-injection detection.
- Approved-source, tenant, permission, sensitivity, and effective-date retrieval filters.
- Separation of system instructions from untrusted document text.
- Allow-listed read tools with independent authorization, schema limits, and timeouts.
- Citation verification, sensitive-data leakage detection, and output blocking/redaction.
- Anomalous usage, extraction attempts, provider misuse, and cache probing detection.
- Immediate fail-closed incident handling for suspected cross-tenant disclosure.

Detailed controls and tests belong in `SEC-AI-001-ai-security-extension.md`.

## 9. Make observability, cost, evaluation, memory, and cache first-class controls

No AI capability reaches production without:

- End-to-end and component latency, errors, provider/fallback, token, cost, cache,
  retrieval, quality, refusal, and security telemetry.
- Per-tenant budgets, quotas, forecasts, alerts, soft limits, and hard limits.
- Offline regression and adversarial evaluation with approved promotion thresholds.
- Tenant- and permission-partitioned conversation memory with retention/deletion controls.
- Tenant- and permission-partitioned semantic/retrieval caches with event-driven
  invalidation and no default caching of personalized HR/payroll answers.
- Operational runbooks for outage, failover, degraded mode, rollback, cost spike, data
  leakage, vector restore/rebuild, and evaluation regression.

Binding decisions are delegated to ADR-031 through ADR-035 and the approved Phase 6
companion documents.

## 10. Keep canonical data outside models and vector indexes

- Tenant source documents and SQL metadata remain the systems of record.
- Embeddings, vector indexes, caches, and generated summaries are reproducible derived
  data.
- Tenant data is used for inference only and is never used to train a shared base model.
- Source, vector, memory, cache, interaction, and backup deletion follows the approved
  retention, legal-hold, offboarding, and DPDP rules.
- Secrets are stored only through tenant-scoped secret references and are never returned
  by APIs or written to telemetry.

## 11. Use events without leaking sensitive content

AI lifecycle changes publish versioned events through ADR-009, including knowledge
publication, index promotion, prompt/model assignment changes, permission changes, cache
invalidation, and security incidents.

Events carry `TenantId`, identifiers, versions, and minimum operational metadata. Raw
prompts, answers, source chunks, credentials, and unnecessary PII are excluded.

---

# Core Architectural Contracts

The technical design may refine names, but it must preserve these boundaries:

| Contract | Responsibility |
|---|---|
| `IAiOrchestrator` | Executes the approved policy-controlled answer pipeline |
| `ILlmProvider` | Provider-neutral generation and capability contract |
| `IEmbeddingProvider` | Provider-neutral embedding contract |
| `IVectorStore` | Tenant-partitioned indexing, retrieval, health, and lifecycle contract |
| `IPromptRegistry` | Resolves immutable effective prompt versions |
| `IAiPolicyEvaluator` | Applies tenant, permission, safety, residency, budget, and use-case policy |
| `IReadToolRegistry` | Exposes allow-listed permission-scoped read tools |
| `IConfidenceEvaluator` | Produces calibrated confidence components and behavior band |
| `IAiUsageLedger` | Records tenant usage, tokens, provider cost, and quota decisions |

No contract exposes vendor request/response types.

---

# Alternatives Considered

## Direct vendor SDK calls from features

Fast initially, but creates vendor lock-in, inconsistent safety, duplicate cost controls,
and untestable tenant policy. Rejected.

## Ungrounded general-purpose chat

Cannot provide reliable policy/payroll answers and conflicts with the platform requirement
for citations and context engineering. Rejected.

## Fine-tuning per tenant as the primary knowledge mechanism

Slow to update, difficult to delete, expensive to govern, and poor for effective-dated
policy knowledge. Rejected as the default. A future narrowly scoped fine-tuning proposal
requires a separate ADR and privacy review.

## Embed all live HR data

Creates stale copies and increases permission, deletion, and disclosure risk. Rejected in
favor of permission-scoped read APIs for structured data.

## Autonomous AI actions

Would bypass deterministic authorization and workflow controls and create unacceptable HR
and payroll risk. Rejected.

## Separate microservice from the first release

Adds deployment and distributed-system complexity before scaling evidence exists. Rejected
for the initial modular-monolith boundary; later extraction remains supported.

---

# Consequences

## Positive

- Grounded, cited, permission-aware AI suitable for sensitive HR workflows.
- Strong isolation and auditable behavior across tenants and providers.
- Provider and model choice without changes to feature code.
- Safe, reversible prompt/model/index evolution.
- Independent control of quality, cost, availability, privacy, and security.
- Future service extraction without changing domain contracts.

## Negative

- More platform work before user-facing AI can be released.
- Additional provider, evaluation, telemetry, cost-ledger, and runbook surfaces.
- Higher latency than direct ungrounded model calls.
- Confidence and evaluation thresholds require ongoing domain calibration.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Hallucinated policy/payroll answer | RAG, citations, confidence gates, refusal, domain evaluation |
| Cross-tenant disclosure | Hard partition, trusted tenant context, revalidation, CI canary tests |
| Prompt injection or poisoned source | Untrusted-content boundary, approved sources, tool allow-list, output checks |
| Provider outage or lock-in | ADR-027 adapters, approved fallback, retrieval-only degraded mode, exit plan |
| Excessive or unpredictable cost | Tenant budgets, quotas, model routing, cache, usage ledger, forecasting |
| Stale answer after policy/permission change | Effective-dated retrieval, version pinning, event-driven invalidation |
| Sensitive data in telemetry | Metadata-only telemetry, redaction, restricted audit content |
| Unsafe recommendation interpreted as action | Non-executable recommendations and separate user-initiated domain command |

---

# Impact

## Architecture

Adds a bounded AI module, context orchestrator, provider adapters, prompt registry,
knowledge-ingestion pipeline, policy enforcement, confidence service, evaluation harness,
usage ledger, and AI operational controls. ADR-030 through ADR-035 define the subordinate
architecture decisions.

## Database

Requires a dedicated `AI` schema design for knowledge metadata, versions, ingestion jobs,
conversation memory, interaction audit, usage/cost ledger, evaluation data, and policies.
Every tenant-scoped table follows ADR-005/006 and database standards. Actual vectors remain
in the configured vector provider.

## Security

Extends the platform threat model with prompt injection, jailbreak, knowledge poisoning,
model abuse, output leakage, tool abuse, and AI-specific incident handling. RBAC, ABAC,
tenant isolation, audit, secret management, and DPDP remain mandatory.

## Performance

Adds retrieval, reranking, model, and guardrail latency. Streaming may improve perceived
latency but cannot release content before required safety checks. Per-tenant quotas,
bulkheads, timeouts, caching, and asynchronous ingestion protect shared capacity.

## Development

No AI implementation may begin until the constitutional Business, Technical, Database, UI,
and Test documents plus required OpenAPI are Approved. Architecture tests must prevent
vendor SDK references outside adapters and state-changing tool exposure.

---

# Approval

Solution Architect: Approved (Agent 6 / Codex)  
Security Architect: ____  
Prompt Engineer: ____  
Context Engineer: ____  
Database Architect: ____  
Product Owner: Bhajan Lal - Approved 2026-06-23

(Status: Approved)
