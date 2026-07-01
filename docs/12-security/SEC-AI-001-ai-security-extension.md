# SEC-AI-001 - AI Security Extension

Document Owner: Security Architect
Created Date: 2026-06-27
Version: 1.0
Status: Approved
Reviewers: Solution Architecture, Platform/Operations, Data Governance/Privacy, Product/AI, Domain Owners

Related approved documents:

- `docs/12-security/SEC-DESIGN-001-threat-model.md`
- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md`
- `docs/15-ai/AI-OPS-001-enterprise-ai-operations.md`
- `docs/16-decisions/ADR-005-multi-tenancy-model.md`
- `docs/16-decisions/ADR-006-tenant-context-data-access.md`
- `docs/16-decisions/ADR-008-identity-access.md`
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

- ADR-022 Data Retention, Archival, Legal Hold, and Deletion
- AI disaster-recovery design and exercise plan
- `docs/08-api-specs/API-SPEC-002-ai-platform-v1.md`
- `docs/08-api-specs/OPENAPI-002-ai-platform-v1.yaml`
- AI Business, Technical, Database, UI, and Test documents

---

# 1. Purpose

This document extends the approved platform security threat model for the AI/RAG platform.
It defines mandatory controls for AI-specific risks including prompt injection, RAG
poisoning, vector leakage, provider misuse, model behavior drift, excessive agency,
sensitive-data disclosure, memory/cache exposure, cost abuse, and AI incident response.

This document is a security design extension. It does not approve implementation by itself.
Implementation remains blocked until the constitutional five-document set, API/OpenAPI,
database design, UI design, and test plan are approved.

---

# 2. Scope

Covered:

- AI gateway/orchestrator security.
- Prompt and context assembly security.
- Retrieval-augmented generation over tenant knowledge.
- Qdrant vector-store security.
- Redis memory and semantic/retrieval cache security.
- AI provider, model, embedding, reranking, and evaluator adapter security.
- Read-only AI tools and permission-scoped domain API access.
- Knowledge ingestion, document extraction, chunking, embedding, and index promotion.
- Output guardrails, citation verification, sensitive-data blocking, and refusal behavior.
- AI telemetry, audit, incident response, and red-team testing.

Not covered:

- General platform identity, RLS, and API security already approved in
  `SEC-DESIGN-001-threat-model.md`, except where AI adds new controls.
- State-changing HRMS business workflows. AI remains read-only and cannot publish,
  approve, modify, delete, or execute business actions.
- Autonomous AI agents. They remain reserved for future architecture and operations docs.

---

# 3. Security Objectives

1. Prevent cross-tenant AI data disclosure under every retrieval, memory, cache, provider,
   telemetry, and audit path.
2. Prevent prompt injection and retrieved-document instructions from overriding platform
   policy, tenant isolation, RBAC/ABAC, safety policy, or citation requirements.
3. Ensure AI can read only what the current user is authorized to read at the time of the
   request.
4. Ensure AI cannot directly mutate HRMS business state.
5. Keep source documents and SQL records authoritative; vectors, caches, and summaries are
   derived and rebuildable.
6. Protect prompts, model configuration, embeddings, retrieved chunks, source documents,
   memory, cache entries, and provider credentials from unauthorized disclosure or tampering.
7. Detect and contain poisoning, leakage, excessive use, model/provider drift, and unsafe
   output quickly.
8. Preserve audit evidence without storing unnecessary sensitive prompt/response content.
9. Make every security control configurable, versioned, effective-dated, and auditable.
10. Keep future AI providers, vector stores, and modules open for extension without weakening
    the existing security boundary.

---

# 4. Research Basis

This document was drafted using the approved HRMS architecture plus current official and
primary sources validated on 2026-06-27:

- OWASP Top 10 for LLM and Generative AI Applications 2025.
- OWASP LLM01 Prompt Injection.
- OWASP LLM04 Data and Model Poisoning.
- OWASP LLM06 Excessive Agency.
- OWASP LLM08 Vector and Embedding Weaknesses.
- OWASP LLM10 Unbounded Consumption.
- NIST AI Risk Management Framework and NIST AI 100-2 Adversarial Machine Learning.
- NIST SP 800-218 Secure Software Development Framework.
- NIST SP 800-61 Rev. 3 Incident Response.
- NCSC Guidelines for Secure AI System Development.
- Qdrant security and access-control guidance.
- Redis security and ACL guidance.
- EU AI Act official text for employment and worker-management high-risk context.

External guidance is used as security input, not as a substitute for HRMS tenant isolation,
RBAC/ABAC, legal review, or owner approval.

---

# 5. Non-Negotiable AI Security Rules

1. Tenant context is server-resolved only. AI must never trust `TenantId` from prompt,
   request body, retrieved document, model output, cache key, or tool argument.
2. Every retrieval, memory lookup, cache hit, tool call, and output release must re-check
   RBAC and ABAC.
3. Retrieved documents are untrusted input. They may contain facts, but never instructions.
4. AI cannot directly perform create, update, delete, approve, publish, payroll, workflow,
   entitlement, user-management, provider-management, or configuration-changing actions.
5. The model is not an authorization engine. Deterministic application code makes all
   authorization, data-scope, safety, and release decisions.
6. Source data is authoritative. Embeddings, Qdrant indexes, Redis caches, and summaries are
   derived stores.
7. No shared vector, cache, memory, or telemetry scope may rely on filtering alone where a
   hard tenant partition is available.
8. AI must fail closed when tenant, identity, permission, safety, model, retrieval, memory,
   budget, or policy state cannot be verified.
9. Prompts, system instructions, provider credentials, source chunks, employee data, and raw
   responses are excluded from general telemetry.
10. Security tests and adversarial evaluations are release gates, not optional hardening.

---

# 6. AI Trust Boundaries

```text
User/UI
  -> API Gateway / WAF
  -> AuthN + tenant resolution
  -> AI Policy Enforcement
       - tenant, RBAC, ABAC, purpose, residency, quota, budget, safety
  -> Context Orchestrator
       - Redis memory reauthorization
       - cache eligibility and per-hit reauthorization
       - Qdrant tenant partition and retrieval filters
       - read-only domain tools
  -> Prompt Assembly
       - immutable prompt version
       - separated untrusted context
       - citations and source IDs
  -> Provider Adapter
       - least-privilege credential
       - provider request minimization
       - timeout and budget limits
  -> Output Guardrails
       - citation support
       - sensitive-data checks
       - policy and purpose boundary
       - refusal/escalation decision
  -> Response + audit + telemetry + usage ledger
```

Main trust boundaries:

- Browser/user prompt boundary.
- Uploaded document and extracted text boundary.
- AI policy engine boundary.
- Vector store and cache boundary.
- Provider adapter boundary.
- Read-only domain API/tool boundary.
- Telemetry/audit boundary.
- Tenant administrator configuration boundary.

Each boundary requires explicit validation, authorization, rate limiting, audit, and failure
behavior.

---

# 7. AI Asset and Data Classification

| Asset | Classification | Security requirement |
|---|---|---|
| System prompts and policy prompts | Restricted platform configuration | Immutable versioning, admin-only access, no telemetry exposure |
| User prompts | Tenant confidential, may contain PII | Minimize storage, redact telemetry, retention controlled by ADR-022 |
| Retrieved chunks | Same as source document | Reauthorize before prompt assembly and output release |
| Embeddings and vectors | Derived sensitive tenant data | Tenant partitioning, encryption, no external exposure, deletion/rebuild |
| Conversation memory | Sensitive derived context | Redis TTL, SQL summaries only when enabled, per-turn reauthorization |
| Semantic/retrieval cache | Sensitive derived answer/context | Deny-by-default eligibility, purpose/permission partitioning |
| Provider credentials | Secret | Vault only, least privilege, rotation, no logs |
| Model/provider registry | Restricted configuration | Effective-dated approvals, signed/change-controlled updates |
| Evaluation datasets | Controlled test evidence, may include synthetic sensitive data | Sealed, versioned, access-controlled, not reused as training data |
| AI audit records | Restricted compliance evidence | Durable, tenant-scoped, tamper-evident, minimal sensitive content |
| Telemetry | Operational data | Redacted, bounded cardinality, no raw prompts/responses/employee data |

---

# 8. Threat Model Summary

| Threat | AI example | Mandatory control |
|---|---|---|
| Spoofing | Forged tenant/user context in prompt or tool argument | Server-resolved tenant and identity, signed JWT, service identity, correlation ID |
| Tampering | Poisoned policy document changes payroll guidance | Source approval workflow, content hash, malware/hidden-text scan, shadow-index validation |
| Repudiation | User denies generating or approving an AI action | AI cannot approve; immutable request metadata and UI action audit |
| Information disclosure | AI retrieves another tenant's policy or salary data | Hard tenant partition, RBAC/ABAC, post-retrieval validation, output redaction |
| Denial of service | Long prompts or repeated costly queries exhaust provider budget | Token limits, rate limits, quotas, circuit breakers, ADR-033 budgets |
| Elevation of privilege | Prompt tells AI to use admin tool or reveal hidden fields | No state-changing tools, allow-listed read tools, complete mediation in code |
| Poisoning | Hidden instructions embedded in uploaded handbook or resume | Treat source text as untrusted, source validation, prompt separation, adversarial tests |
| Model/provider drift | Provider changes behavior behind same model name | ADR-034 drift monitoring, lifecycle re-evaluation, rollback bundle |
| Supply chain compromise | Malicious model/library/container in AI pipeline | SBOM/AIBOM, signed artifacts, dependency scanning, sandboxed extraction |
| Cost abuse | Denial-of-wallet attack through high-volume prompts | Tenant/user/use-case budgets, alerts, throttling, emergency disablement |

---

# 9. OWASP GenAI Risk Mapping

| OWASP 2025 risk | HRMS exposure | Required HRMS control |
|---|---|---|
| LLM01 Prompt Injection | User prompt or retrieved document tries to override platform rules | Instruction hierarchy, untrusted-context separation, prompt-injection detection, output policy gate |
| LLM02 Sensitive Information Disclosure | Model returns PII, payroll, salary, disciplinary, or medical information | RBAC/ABAC, field masking, DLP checks, citation support, refusal/escalation |
| LLM03 Supply Chain | Provider SDK, model artifact, parser, OCR, or embedding library compromised | SBOM/AIBOM, dependency scanning, signed artifacts, provider due diligence |
| LLM04 Data and Model Poisoning | Uploaded policy, FAQ, public source, or feedback contaminates RAG | Approved sources only, hashing, malware/hidden-text checks, shadow-index tests |
| LLM05 Improper Output Handling | AI output is inserted into UI/API without validation | Output schema validation, encoding, UI sanitization, no executable responses |
| LLM06 Excessive Agency | AI tool can update HR data or perform high-impact actions | Read-only tools only, no direct mutations, human workflow path for actions |
| LLM07 System Prompt Leakage | User asks for system prompt or hidden policy | Refusal, prompt confidentiality, no prompt in telemetry, access-controlled registry |
| LLM08 Vector and Embedding Weaknesses | Cross-tenant vector leak or embedding inversion | Hard partitioning, metadata filters, post-retrieval validation, encryption, deletion |
| LLM09 Misinformation | AI gives unsupported payroll/legal/HR policy answer | Grounding, citations, confidence gates, refusal, human escalation |
| LLM10 Unbounded Consumption | Cost, token, context, or provider capacity abuse | Quotas, budgets, token limits, rate limits, cache policy, circuit breakers |

---

# 10. Prompt Injection and Jailbreak Controls

Prompt injection is expected, not exceptional. The system must assume that users, uploaded
documents, emails, PDFs, webpages, images, and extracted text may contain hostile
instructions.

Mandatory controls:

- Maintain a strict instruction hierarchy: platform policy, tenant policy, system prompt,
  tool schema, authorized context, then user question.
- Mark retrieved context as untrusted evidence. Retrieved text cannot define rules, tool
  permissions, tenant scope, safety policy, or output format.
- Use explicit prompt delimiters and source metadata around every retrieved chunk.
- Detect direct and indirect injection patterns, including hidden text, base64/encoding,
  multilingual evasion, role-play, "ignore previous instructions", data-exfiltration
  requests, system-prompt requests, and tool-abuse attempts.
- Apply deterministic output checks after model response; do not rely only on the prompt to
  prevent unsafe behavior.
- Refuse or reduce context when the prompt contains instructions to reveal secrets, cross
  tenant data, system prompts, provider keys, hidden fields, or unauthorized HR data.
- Add adversarial prompt suites to ADR-034 evaluation before each model/prompt/index
  promotion.
- Log security metadata for injection attempts without storing unnecessary raw content.

---

# 11. RAG and Vector Security

RAG increases accuracy but creates new attack surfaces. Qdrant indexes must be treated as
sensitive derived stores, not neutral search infrastructure.

Mandatory controls:

- Use the ADR-030 tenant placement model: Qdrant tenant shard key/dedicated collection and
  mandatory `TenantId` payload validation.
- A future Azure AI Search adapter must use dedicated tenant indexes unless an approved ADR
  accepts an equivalent hard partition.
- Every vector point contains `TenantId`, `DocumentId`, `ChunkId`, `DocumentVersion`,
  `PermissionTags`, `Sensitivity`, `EffectiveFrom`, `EffectiveTo`, `Locale`,
  `Jurisdiction`, `ApprovalStatus`, `EmbeddingModelVersion`, and `ContentHash`.
- Retrieval applies hard tenant placement first, then permission/sensitivity/effective-date
  filters, then post-retrieval validation.
- Shared metadata filtering alone is not an isolation boundary.
- Embeddings are never exposed through public APIs or admin UI by default.
- Vector export, snapshot, restore, rebuild, and collection inspection require privileged
  platform roles, reason, approval, and audit.
- Every index promotion uses a shadow index and must pass cross-tenant negative tests,
  poisoned-document tests, citation tests, freshness tests, and rollback tests.
- Deletion/offboarding events remove or make unreachable eligible vectors, caches, and
  summaries according to ADR-022.

---

# 12. Knowledge Ingestion Security

Knowledge ingestion is a high-risk path because it can introduce poisoned content into
future answers.

Mandatory controls:

- Ingestion accepts only approved source types, allowed MIME types, allowed extensions, and
  configured file size limits.
- Every upload is malware scanned and quarantined until approved.
- Extracted text is scanned for hidden text, invisible characters, suspicious instructions,
  external URL beacons, unusual encodings, and prompt-injection markers.
- Source documents require owner, classification, jurisdiction, language, effective dates,
  retention policy, approval status, and supersession metadata.
- Personal documents such as resumes, complaints, medical notes, disciplinary material, or
  payroll records are not embedded unless a dedicated approved use case permits it.
- Public internet content is not ingested automatically. It requires source authority,
  provenance, freshness, legal review where needed, and owner approval.
- Chunking, embedding, and metadata assignment are deterministic and versioned.
- Rejected source material is retained only as permitted by security and retention policy.
- Tenant administrators can manage only their tenant's sources and cannot override platform
  malware, privacy, isolation, or prohibited-use checks.

---

# 13. AI Read Tools and Excessive Agency Controls

The AI platform may use read-only domain tools to answer authorized questions. These tools
are security boundaries, not model conveniences.

Mandatory controls:

- Tools are allow-listed, versioned, schema-limited, and registered in `IReadToolRegistry`.
- Tools execute under the current user's tenant, identity, RBAC, ABAC, purpose, and field
  masking policy.
- Tools cannot expose SQL, file system, shell, network fetch, provider admin, tenant admin,
  payroll mutation, workflow publication, or configuration mutation functions.
- Tool arguments are generated by the orchestrator and validated by deterministic code.
- Tool results are minimized, classified, and rechecked before prompt assembly.
- Tool calls have timeouts, result limits, rate limits, and audit records.
- High-impact employment decisions, payroll decisions, promotion/termination decisions, and
  candidate decisions cannot be made by AI.
- Future autonomous agents remain prohibited until a dedicated approved package exists.

---

# 14. Sensitive Data and Privacy Controls

AI responses may touch salary, payroll, national identifiers, bank data, health-adjacent
data, leave, disciplinary, performance, grievance, and employee-relations data. These are
high-sensitivity HRMS categories.

Mandatory controls:

- Field-level masking rules from the domain API apply before AI sees structured data.
- The model receives minimum necessary context only.
- Provider requests exclude secrets, tokens, raw credentials, unnecessary identifiers, and
  unrelated employee records.
- Tenant data is used for inference only and is never used to train shared base models.
- Provider data-processing terms must confirm data use, retention, residency, subprocessors,
  deletion, breach notification, and audit support before activation.
- Raw prompts/responses are not stored by default. Any exception requires purpose, retention,
  encryption, access control, and owner approval.
- Conversation summaries are governed by ADR-032 and must remain purpose-scoped.
- AI cannot infer or reveal sensitive attributes unless explicitly authorized and necessary
  for the use case.
- Data-subject requests, deletion, legal hold, backup erasure, and tenant offboarding follow
  ADR-022 when approved.

---

# 15. Memory and Cache Security

Conversation memory and semantic cache improve usability and cost, but they can leak stale
or unauthorized context if not controlled.

Mandatory controls:

- Session memory is `SessionOnly` by default.
- Redis memory keys include tenant, user/session, purpose, policy, prompt/model, and version
  partitioning as defined by ADR-032.
- SQL summaries are opt-in, encrypted, effective-dated, and reauthorized every turn.
- Semantic/retrieval cache is deny-by-default for personalized HR/payroll answers.
- Every cache hit is reauthorized before reuse.
- Cache keys use HMAC or equivalent construction to avoid leaking prompt/content patterns.
- Cache values store no provider credentials, system prompts, or unrestricted source text.
- TenantRoleMatrixChanged, permission changes, source changes, deletion, policy changes,
  model/prompt changes, and security incidents invalidate affected memory/cache entries.
- Redis uses private network placement, ACL users, TLS where required, restricted commands,
  separate workloads/namespaces, and emergency disablement.

---

# 16. Provider and Model Security

Provider abstraction must not become provider blindness. Each provider/model adapter must
have an approved security profile before production use.

Mandatory controls:

- Provider selection is registry-driven and effective-dated.
- Provider credentials are stored only as secret references and scoped by environment,
  tenant/service tier, capability, and region.
- Provider calls use request minimization, timeouts, retries with caps, and budget checks.
- No provider is activated automatically during outage, cost pressure, or capacity pressure.
- External provider terms must be reviewed for data retention, training use, jurisdiction,
  security posture, incident notice, logging, subcontractors, and deletion support.
- Model version, provider version, prompt version, safety policy, retrieval index, cache
  policy, memory policy, and evaluation bundle are pinned per request.
- Provider behavior drift triggers ADR-034 re-evaluation and may require rollback or
  disablement.
- Self-hosted/local models, model files, and serialized artifacts are treated as untrusted
  third-party code and require scanning, sandboxing, provenance, and signed artifact checks.

---

# 17. Output Handling and Misinformation Controls

AI output is untrusted until validated. It cannot be inserted into UI, copied to reports, or
used by downstream systems without release checks.

Mandatory controls:

- Knowledge answers require citations for every material claim.
- Unsupported, stale, conflicting, or low-confidence claims trigger refusal, caution, or
  human escalation.
- Payroll, legal, compliance, disciplinary, performance, and employment-decision answers
  require stricter thresholds and domain-specific escalation rules.
- Output schemas are validated before release.
- UI rendering must encode AI output and block HTML/script injection.
- AI-generated reports, workflows, policies, or forms are drafts only until normal review
  and approval workflows complete.
- Responses are scanned for sensitive-data leakage, system-prompt leakage, provider-secret
  leakage, cross-tenant identifiers, and prohibited employment behavior.
- Response metadata includes prompt/model/index/policy versions, citations, confidence band,
  refusal reason, and escalation marker where applicable.

---

# 18. Cost Abuse and Unbounded Consumption Controls

AI security includes economic abuse. A tenant, user, bot, or attacker must not be able to
create uncontrolled provider spend or deny service to other tenants.

Mandatory controls:

- Apply tenant, user, use-case, provider, model, and operation-level rate limits.
- Enforce maximum prompt size, retrieved-context size, tool result size, output tokens, and
  request duration.
- Use ADR-033 atomic budget reservation before paid provider calls.
- Detect denial-of-wallet patterns, retry storms, cache bypass storms, embedding floods, and
  repeated adversarial probing.
- Apply circuit breakers and emergency disablement at global, tenant, use-case, provider,
  model, cache, and ingestion levels.
- Quota failures must return safe user-facing messages and must not degrade tenant isolation
  or safety controls.

---

# 19. AI Audit and Evidence

Audit records must prove what happened without becoming a new data-leak source.

Durable AI audit records include:

- Tenant, user, purpose, use case, request ID, correlation ID, and timestamp.
- Prompt/model/provider/index/cache/memory/evaluation policy versions.
- Authorization decision, denial/refusal/escalation reason, and policy decision IDs.
- Source document IDs, section IDs, and citation IDs used in the response.
- Tool call metadata, not unrestricted tool output.
- Provider call metadata, token/cost metadata, and fallback path.
- Security signal IDs for injection, leakage, poisoning, cost abuse, or drift.
- Response release decision and confidence band.

Audit records must not store provider keys, system prompts, full source chunks, raw employee
records, or raw prompt/response content unless an approved retention exception exists.

---

# 20. Telemetry and Monitoring Security

Operational telemetry follows ADR-031 and AI-OPS-001.

Mandatory security signals:

- PromptInjectionDetected
- SystemPromptDisclosureAttempted
- SensitiveOutputBlocked
- CrossTenantRetrievalAttempted
- UnauthorizedToolCallBlocked
- RAGPoisoningSuspected
- VectorPartitionViolation
- CachePolicyViolation
- MemoryAuthorizationDrift
- ProviderBehaviorDrift
- ModelSafetyRegression
- UnboundedConsumptionSuspected
- DenialOfWalletSuspected
- AiSecurityIncidentOpened
- AiEmergencyDisablementActivated

Signals must be tenant-safe, cardinality-bounded, redacted, and linked to durable audit
where evidence is required.

---

# 21. Deployment and Infrastructure Controls

Mandatory controls:

- Separate production and non-production provider keys, Qdrant collections, Redis
  namespaces, object storage, SQL databases, telemetry, and tenant catalogs.
- No production tenant data is copied to non-production by default.
- AI containers, parsers, OCR tools, embedding workers, and provider adapters are scanned
  before deployment.
- Secrets are delivered through approved secret-management paths only.
- Egress from AI services is allow-listed. Open internet fetch by AI is prohibited unless a
  dedicated approved connector exists.
- Qdrant self-hosted deployments require authentication, private network binding, TLS,
  audit logging, least-privilege keys, internal-port protection, and rotation.
- Redis deployments require private network access, ACLs, TLS where required, restricted
  dangerous commands, and no direct untrusted client access.
- Provider endpoints require certificate validation and approved network path.
- Emergency changes are time-bound, monitored, audited, and reviewed after use.

---

# 22. Secure Development and Supply Chain Controls

AI development follows `SECURITY_STANDARDS.md`, NIST SSDF, and NCSC secure AI lifecycle
guidance.

Mandatory controls:

- Threat model every AI feature, provider adapter, ingestion path, tool, memory/cache path,
  and operational API.
- Maintain SBOM for application dependencies and AIBOM/model bill of materials for model,
  prompt, dataset, embedding, and evaluation dependencies where applicable.
- Use SAST, dependency scanning, secret scanning, container scanning, IaC scanning, and
  license checks in CI.
- Treat model files, serialized artifacts, third-party datasets, parsers, and extraction
  libraries as untrusted supply chain inputs.
- Keep prompt, model, index, policy, and evaluation changes under version control or
  governed configuration with audit.
- Require code review plus security review for changes that affect tenant isolation,
  prompt assembly, provider adapters, vector retrieval, memory, cache, tools, or output
  release.

---

# 23. Incident Response

AI security incidents follow NIST SP 800-61 Rev. 3 concepts and AI-OPS-001 runbooks.

| Incident condition | Initial action | Primary runbook |
|---|---|---|
| Cross-tenant retrieval or output | Fail closed, disable affected AI path, preserve evidence | AI-RUN-005 |
| Prompt injection causing unsafe output | Disable prompt/model/index bundle if needed, preserve samples | AI-RUN-005 |
| RAG poisoning suspected | Freeze index promotion, quarantine source, rebuild shadow index | AI-RUN-008 |
| Vector partition or Qdrant credential issue | Disable affected placement/key, validate partitions | AI-RUN-002 |
| Cache poisoning or stale unauthorized hit | Disable cache namespace, rotate namespace, invalidate entries | AI-RUN-009 |
| Memory authorization drift | Reset affected memory, invalidate summaries, reauthorize | AI-RUN-010 |
| Provider behavior drift | Switch/disable provider by approved policy, re-evaluate bundle | AI-RUN-001 |
| Cost abuse or denial-of-wallet | Apply emergency quotas/disablement, preserve usage evidence | AI-RUN-006 |
| Secret compromise | Revoke, rotate, invalidate dependent sessions/caches | AI-RUN-017 |
| Deletion/legal-hold failure | Block affected reuse/export/restore, reconcile state | AI-RUN-018 |

SEV-0 is mandatory for confirmed or plausible cross-tenant disclosure, provider credential
exposure, unauthorized HR/payroll data disclosure, or AI-caused prohibited employment
behavior.

---

# 24. Regulatory and Employment-Risk Controls

The HRMS AI platform must treat employment and worker-management use cases as high impact
even when a local law does not use the same label.

Mandatory controls:

- AI cannot make final employment, payroll, promotion, termination, disciplinary, candidate,
  or performance decisions.
- AI cannot rank candidates, score employees, recommend termination, or classify protected
  attributes without a dedicated approved high-risk use case and legal review.
- Users must understand when content is AI-generated and when human review is required.
- Human review must be meaningful for high-impact decisions; rubber-stamp review is not
  accepted.
- Fairness and bias evaluation from ADR-034 is mandatory for any use case that could affect
  employees, candidates, pay, access to benefits, or work allocation.
- Regional privacy, labor, data residency, retention, and employee monitoring requirements
  must be validated before tenant activation.

---

# 25. API and OpenAPI Security Requirements

Phase 6D API/OpenAPI must include AI security behavior, not only happy-path operations.

Mandatory API controls:

- All AI APIs are versioned and documented in OpenAPI.
- Tenant context is resolved by server-side identity/host policy.
- Request schemas include purpose, use case, idempotency/correlation ID, and allowed
  operation type where applicable.
- Security responses document refusal, insufficient permission, budget/quota denial, policy
  denial, safety denial, degraded mode, and incident disablement.
- Administrative APIs require elevated RBAC/ABAC, reason, approval reference, optimistic
  concurrency, idempotency, and audit.
- APIs never expose raw vectors, raw cache entries, unrestricted memory, provider secrets,
  system prompts, or cross-tenant diagnostics.
- Operational APIs support preview/dry-run for destructive or recovery actions where useful.

---

# 26. Security Test and Red-Team Requirements

Security testing is mandatory before approval and release.

Required test categories:

- Cross-tenant negative retrieval tests.
- RBAC/ABAC and field-masking tests.
- Prompt injection and jailbreak tests.
- Indirect injection through uploaded documents and extracted text.
- Hidden text, encoded text, multilingual, and obfuscated prompt tests.
- RAG poisoning tests and source-integrity tests.
- Vector partition, snapshot, restore, and rebuild tests.
- Embedding/version mismatch tests.
- Cache poisoning, stale hit, and cache reauthorization tests.
- Conversation memory reset, invalidation, and purpose-boundary tests.
- Provider fallback, timeout, and behavior-drift tests.
- Sensitive output blocking and system-prompt leakage tests.
- Cost abuse, token flooding, retry storm, and denial-of-wallet tests.
- Tool-call argument manipulation and unauthorized tool tests.
- Security telemetry, audit, incident, and emergency disablement tests.
- End-to-end tests proving AI cannot mutate HRMS business state.

Unit coverage remains at least 85%, with integration, security, performance, adversarial,
chaos/failover, restore, deletion, and end-to-end coverage for AI paths.

---

# 27. Residual Risks

| Risk | Status | Required mitigation |
|---|---|---|
| Prompt injection cannot be fully eliminated | Accepted as inherent | Layered detection, least privilege, no state mutation, output gates, red-team cadence |
| Provider model behavior may change | Open | Registry pinning where possible, drift detection, re-evaluation, rollback |
| Embeddings may leak information by inference | Open | Hard partitioning, no public vector APIs, encryption, minimization, deletion |
| Tenant admin may upload poisoned content | Open | Approval workflow, scanning, shadow-index tests, source ownership, audit |
| Overly broad future AI tools could create agency risk | Blocked | Read-only tools only; future agents require separate approved package |
| Regulatory treatment of HR AI evolves | Open | Legal review before high-impact use cases, effective-dated policy updates |
| Self-hosted Qdrant/Redis may be misconfigured | Open | Security baseline, ORR validation, monitoring, periodic configuration audit |

---

# 28. Approval Gates

Before any AI capability enters implementation or production design, the following must be
complete:

- This document is `Approved`.
- ADR-022 retention/deletion/legal-hold decision is approved.
- AI disaster-recovery design and exercise plan are approved.
- AI API specification and OpenAPI YAML are approved.
- AI Business, Technical, Database, UI, and Test documents are approved for the feature.
- Security test plan includes the test categories in this document.
- AI Governance Board review is required for significant provider/model/prompt/RAG/security
  policy changes.

---

# 29. Acceptance Criteria

| ID | Criterion |
|---|---|
| SEC-AI-AC-001 | Tenant context for every AI operation is server-resolved and never trusted from prompt, request body, model output, cache, memory, or tool arguments. |
| SEC-AI-AC-002 | Every retrieval, memory lookup, cache hit, tool call, and output release re-checks current RBAC and ABAC. |
| SEC-AI-AC-003 | Retrieved documents are treated as untrusted evidence and cannot override platform, tenant, system, safety, or tool policy. |
| SEC-AI-AC-004 | AI cannot directly create, update, delete, approve, publish, payroll, workflow, identity, provider, or configuration state. |
| SEC-AI-AC-005 | Prompt injection detection covers direct, indirect, hidden, encoded, multilingual, and system-prompt disclosure attempts. |
| SEC-AI-AC-006 | Output guardrails validate citations, sensitive-data policy, system-prompt leakage, tenant scope, schema, and refusal/escalation behavior. |
| SEC-AI-AC-007 | Qdrant uses hard tenant placement plus mandatory metadata filters and post-retrieval tenant/permission validation. |
| SEC-AI-AC-008 | Embeddings and vectors are never exposed through public APIs or general admin UI. |
| SEC-AI-AC-009 | Knowledge ingestion validates source authority, malware status, hidden text, prompt-injection markers, classification, effective dates, and approval state. |
| SEC-AI-AC-010 | Index promotion uses shadow indexes and passes isolation, poisoning, citation, freshness, performance, and rollback tests. |
| SEC-AI-AC-011 | Redis memory and cache use ACLs, private network placement, TTL, namespace partitioning, and per-hit reauthorization. |
| SEC-AI-AC-012 | Semantic/retrieval caching is deny-by-default for personalized HR/payroll answers. |
| SEC-AI-AC-013 | Provider credentials are vault-backed, least privilege, rotated, scoped by environment and capability, and never logged. |
| SEC-AI-AC-014 | Provider activation requires approved data-processing, retention, residency, incident, deletion, and security review. |
| SEC-AI-AC-015 | Model/provider/prompt/index/cache/memory/evaluation bundle versions are pinned and auditable per request. |
| SEC-AI-AC-016 | Provider behavior drift triggers evaluation review and can trigger disablement or rollback. |
| SEC-AI-AC-017 | AI telemetry excludes raw prompts, raw responses, unrestricted source chunks, employee records, provider keys, and system prompts by default. |
| SEC-AI-AC-018 | Durable AI audit records capture enough metadata to reconstruct policy, source, tool, provider, cost, and release decisions. |
| SEC-AI-AC-019 | Cost abuse controls enforce rate limits, token limits, budget reservation, circuit breakers, and emergency disablement. |
| SEC-AI-AC-020 | AI APIs are versioned, OpenAPI-documented, tenant-isolated, RBAC/ABAC-protected, audited, idempotent where needed, and rate-limited. |
| SEC-AI-AC-021 | Administrative AI security APIs require reason, approval reference, optimistic concurrency, idempotency, and immutable audit. |
| SEC-AI-AC-022 | Security signals exist for injection, leakage, poisoning, vector partition violation, cache violation, memory drift, provider drift, and cost abuse. |
| SEC-AI-AC-023 | Confirmed or plausible cross-tenant disclosure is SEV-0 and fails closed immediately. |
| SEC-AI-AC-024 | AI-generated workflows, reports, policies, and forms remain drafts until normal human approval workflows complete. |
| SEC-AI-AC-025 | High-impact employment, payroll, candidate, performance, disciplinary, and termination use cases require legal/domain/fairness review and human oversight. |
| SEC-AI-AC-026 | AI cannot rank candidates, score employees, or recommend termination without a separately approved high-risk use case. |
| SEC-AI-AC-027 | Security testing includes prompt injection, RAG poisoning, vector leakage, memory/cache, provider drift, tool misuse, cost abuse, and cross-tenant tests. |
| SEC-AI-AC-028 | Unit coverage is at least 85% and includes AI security policy units plus integration and end-to-end security tests. |
| SEC-AI-AC-029 | Self-hosted Qdrant production deployment proves authentication, TLS, private binding, least-privilege keys, audit logging, and internal-port protection. |
| SEC-AI-AC-030 | Redis production deployment proves private access, ACL users, TLS where required, restricted commands, and no direct untrusted access. |
| SEC-AI-AC-031 | Source deletion, tenant offboarding, and legal hold reconcile source, vector, memory, cache, provider residual state, audit, and backup state after ADR-022 approval. |
| SEC-AI-AC-032 | AI emergency disablement can be applied by tenant, use case, provider, model, prompt bundle, index, memory, cache, or global scope without code deployment. |
| SEC-AI-AC-033 | Security reviews are mandatory for prompt assembly, provider adapters, vector retrieval, ingestion, memory, cache, tools, and output-release changes. |
| SEC-AI-AC-034 | SBOM/AIBOM, dependency scanning, secret scanning, container scanning, and signed artifact checks are required for AI release candidates. |
| SEC-AI-AC-035 | Future autonomous agents remain prohibited until a dedicated approved architecture, security, database, operations, API/OpenAPI, UI, and test package exists. |

---

# 30. Official and Primary References

- OWASP Top 10 for LLM and Generative AI Applications 2025:
  `https://genai.owasp.org/llm-top-10/`
- OWASP LLM01 Prompt Injection:
  `https://genai.owasp.org/llmrisk/llm01-prompt-injection/`
- OWASP LLM04 Data and Model Poisoning:
  `https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/`
- OWASP LLM06 Excessive Agency:
  `https://genai.owasp.org/llmrisk/llm062025-excessive-agency/`
- OWASP LLM08 Vector and Embedding Weaknesses:
  `https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/`
- OWASP LLM10 Unbounded Consumption:
  `https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/`
- NIST AI Risk Management Framework:
  `https://www.nist.gov/itl/ai-risk-management-framework`
- NIST AI 100-2 E2023, Adversarial Machine Learning:
  `https://csrc.nist.gov/pubs/ai/100/2/e2023/final`
- NIST SP 800-218 Secure Software Development Framework:
  `https://csrc.nist.gov/pubs/sp/800/218/final`
- NIST SP 800-61 Rev. 3 Incident Response:
  `https://csrc.nist.gov/pubs/sp/800/61/r3/final`
- NCSC Guidelines for Secure AI System Development:
  `https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development`
- Qdrant Security and Access Control:
  `https://qdrant.tech/documentation/operations/security/`
- Redis Security:
  `https://redis.io/docs/latest/operate/oss_and_stack/management/security/`
- Redis ACL:
  `https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/`
- EU AI Act Regulation 2024/1689:
  `https://eur-lex.europa.eu/eli/reg/2024/1689/oj`

References last validated: 2026-06-27.

---

# Approval

Security Architect: Drafted by Codex 2026-06-27  
Solution Architect: ____  
Platform/Operations Architect: ____  
Data Governance/Privacy: ____  
Product/AI Owner: ____  
HR/Payroll Domain Owner: ____  
Product Owner: Approved by Bhajan Lal 2026-06-27

(Status: Approved - owner approved 2026-06-27)
