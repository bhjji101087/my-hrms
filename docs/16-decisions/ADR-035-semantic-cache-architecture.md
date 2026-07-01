# ADR-035 - Enterprise Semantic and Retrieval Cache Architecture

Architecture Decision Record

Date: 2026-06-25
Last Updated: 2026-06-25
Status: Approved
Approved By: Bhajan Lal (Product Owner)
Approved Date: 2026-06-25

Related documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md` - Approved v2.1
- ADR-005 Multi-Tenancy Model - Approved
- ADR-006 Tenant Context and Data Access - Approved
- ADR-007 Effective-Dated and Bitemporal Data - Approved
- ADR-008 Identity and Access Management - Approved
- ADR-009 Event-Driven Backbone - Approved
- ADR-019 Enterprise AI/RAG Platform Architecture - Approved
- ADR-027 Provider-Abstraction Framework - Approved
- ADR-030 Enterprise Vector Store Strategy - Approved
- ADR-031 AI Observability and Telemetry - Approved
- ADR-032 Conversation Memory Strategy - Approved
- ADR-033 AI Cost Governance - Approved
- ADR-034 Enterprise AI and RAG Evaluation Framework - Approved

---

# Context

AI and RAG requests repeatedly embed similar questions, retrieve the same sources, assemble
the same prompt prefix, and generate substantially equivalent grounded answers. Controlled
caching can reduce latency, model tokens, provider cost, embedding work, and load on Qdrant,
Redis, SQL Server, and source systems.

Semantic caching is also a high-risk reuse mechanism. Unlike an exact key/value cache, it may
return an answer created for a different wording or context. A false semantic hit, stale
permission fingerprint, outdated policy, poisoned entry, cross-tenant nearest neighbor, or
provider-side cache assumption can expose data or produce an authoritative-looking but wrong
HR response.

Enterprise HRMS risk is especially high because apparently similar questions may differ by:

- Tenant, role, ABAC scope, delegation, employment status, or purpose.
- Country, state, legal entity, business unit, grade, worker type, union/contract, language,
  or policy effective date.
- Source approval, supersession, permission, confidentiality, or legal-hold state.
- Prompt, model, embedding, reranker, index, tool, confidence, safety, memory, or cache-policy
  version.
- Personal employee facts, live payroll/attendance/leave balances, workflow state, or other
  data that must never be reused as a generic answer.

Redis documentation demonstrates semantic response caching with configurable similarity
thresholds, TTLs, tags, and filters, and Redis supports vector search with metadata filters.
Provider prompt/context caches from Anthropic, OpenAI, and Google have different prefix,
token, TTL, routing, and usage-reporting behavior. These capabilities are useful
optimizations, not portable security or correctness controls.

The platform therefore needs a tenant-safe, permission-aware, versioned cache architecture
that can operate locally/self-hosted without a paid managed cache and can be replaced through
adapters without changing AI feature code.

---

# Decision

## 1. Treat every AI cache as disposable derived data

The cache is never:

- A system of record.
- A source of authorization or tenant identity.
- A substitute for current source documents, rules, or effective dates.
- Conversation memory, an employee profile, an audit ledger, or evaluation evidence.
- Proof that a response is still safe, correct, current, or permitted.

A cache hit is a candidate optimization. The platform independently resolves tenant/user,
revalidates current RBAC plus ABAC, verifies dependencies and policy versions, and applies
current output controls before release.

Loss, eviction, corruption, or disablement of cache entries must degrade to a miss. Core HRMS
and approved AI paths remain correct without a cache.

## 2. Support five explicitly separated cache classes

| Cache class | Permitted content | Initial state | Authoritative validation |
|---|---|---|---|
| Exact response cache | Evaluated grounded answer for an identical canonical request/security/version bundle | Disabled until use-case policy enables | Full hit revalidation |
| Semantic response cache | Evaluated grounded non-personal knowledge answer plus dependency manifest | Disabled by default; opt-in per use case | Hard partition, similarity gate, full hit revalidation |
| Retrieval cache | Authorized source IDs, versions, ranking/scores, and filter manifest; no source body by default | Policy controlled | Reauthorize and re-fetch current source content |
| Embedding cache | Normalized eligible query embedding and model/version metadata | Policy controlled | Tenant/version scope and classification check |
| Provider prompt/context cache | Provider-side reusable static prefix/context where contract and policy allow | Disabled by default per provider/use case | Provider policy plus full normal response processing |

Negative/no-result retrieval caching may be enabled only with a short absolute TTL, current
index/source namespace, and event invalidation. It cannot turn temporary authorization,
ingestion, or provider failures into a durable no-answer response.

Security rate-limit, idempotency, circuit-breaker, and session-memory stores are separate
capabilities even when they use Redis. They do not share semantic entries or eligibility
rules.

## 3. Use self-hosted Redis as the first cache and semantic-index adapter

Initial development and deployment use a version-pinned, self-hosted Redis capability behind
`ICacheProvider` and `ISemanticCacheStore`. Redis stores cache entries in hashes/JSON and uses
its supported vector-search capability for semantic lookup with metadata filters.

This decision does not replace ADR-030:

- Qdrant remains the first `IVectorStore` adapter for approved canonical knowledge vectors.
- Redis is the first ephemeral cache store and semantic cache index.
- Semantic response, conversation, and user-preference vectors are not written into Qdrant.
- A future Qdrant semantic-cache adapter requires an ADR amendment, separate placement,
  TTL/deletion proof, poisoning/isolation evaluation, and must not mix cache entries with
  canonical knowledge collections.

Development can run Redis locally/self-hosted without a managed-service subscription.
Production still accounts for compute, storage, backup where enabled, operations, support,
security, and availability under ADR-033.

Redis search/vector capability, client, module/build, and license compatibility are pinned
and reviewed before each production promotion. Core AI code depends only on interfaces.

## 4. Keep cache providers replaceable and capabilities explicit

Provider-independent contracts include:

- `ICacheProvider` - exact key/value operations and atomic TTL behavior.
- `ISemanticCacheStore` - scoped vector put/search/delete and metadata filters.
- `ICacheEligibilityEvaluator` - decides whether request and response may be cached.
- `ICacheKeyBuilder` - creates trusted canonical HMAC keys and scope fingerprints.
- `ICacheHitValidator` - reauthorizes and validates every candidate hit.
- `ICacheDependencyRegistry` - source/version dependencies and targeted invalidation.
- `ICacheInvalidationService` - namespace rotation, event consumption, purge, reconciliation.
- `IPromptCacheAdapter` - optional provider prompt/context cache configuration and usage.
- `ICacheTelemetry` - normalized metrics without sensitive payloads.

Capability flags record vector search, metadata filters, atomic operations, absolute TTL,
conditional write, compare-and-set, bulk delete, ACL/key-prefix controls, encryption,
replication, and provider prompt-cache semantics.

No use case may rely on an optional adapter capability without an approved fallback. Adding
or replacing Redis/provider cache adapters does not change feature logic or public contracts.

## 5. Make cache eligibility an effective-dated policy decision

Every use case has an effective-dated `AiCachePolicy` defining eligible cache classes,
content/data classifications, sources, languages, jurisdictions, maximum sensitivity,
required confidence/evaluation status, TTL, similarity policy, dependency rules, and
prohibited contexts.

Semantic/exact response caching is limited initially to evaluated, grounded, read-only,
non-personal knowledge answers such as approved tenant policies, handbooks, and SOPs when the
answer is identical for the entire security/context equivalence class.

Response caching is prohibited by default for:

- Employee-specific or applicant-specific data.
- Payroll amounts, payslips, compensation, tax, bank, benefits, loans, or deductions.
- Attendance, leave balance, schedules, location, health, disability, disciplinary,
  grievance, performance, recruitment, background-check, or termination information.
- Live workflow, approval, case, ticket, integration, or transactional state.
- Conversation turns, summaries, inferred preferences, hidden reasoning, or tool payloads.
- Secrets, credentials, authentication data, protected attributes, or restricted legal data.
- State-changing operations or recommendations that could be executed as decisions.
- Low-confidence, conflicting, unsupported, injection-flagged, redacted, error, fallback,
  incident, or human-escalation responses unless a separately approved safe negative policy
  explicitly permits a short-lived non-content marker.

If personalization, rules, effective dating, or jurisdiction changes the answer, all relevant
attributes/versions must be in the security/context fingerprint or the response is ineligible.
Unknown classification is ineligible.

Every policy has `PolicyReviewDate` and `PolicyExpiryDate`. Review revalidates TTLs,
eligibility/prohibition rules, similarity thresholds/margins, sensitivity classifications,
source dependencies, warm-up rules, provider-cache behavior, incidents, cost/value, and
ADR-034 evidence. Configurable notifications occur before review and expiry. An expired or
overdue policy disables new cache reads/writes for its scope and safely falls back to normal
authorized processing; it cannot renew silently or continue because entries remain in Redis.
Renewal creates a new effective-dated version and preserves prior approval history.

## 6. Resolve trusted tenant and authorization scope before cache access

Cache lookup never occurs before trusted server-side resolution of:

- `TenantId`, `UserId`, account/employment status, and request purpose.
- Current RBAC permissions, ABAC attributes/scope, delegations, and role-matrix version.
- Data-classification and tenant cache/AI entitlement policy.
- Use case, locale, jurisdiction, source scope, and applicable effective-date context.

Request-supplied tenant IDs, role names, permission fingerprints, cache keys, namespaces,
entry IDs, or hashes are ignored as authority.

The `SecurityContextFingerprint` is generated by a centralized server component from trusted
versioned authorization/context inputs. It contains hashes/versions, not raw roles, employee
attributes, or sensitive values. Any authorization change produces a new fingerprint so old
entries become unreachable even before asynchronous deletion.

## 7. Hard-partition before any exact or semantic comparison

The cache partition is selected before vector search and includes at minimum:

- Trusted tenant partition/shard.
- Use case and declared purpose.
- Security-context/permission equivalence fingerprint.
- Data classification and approved source scope.
- Locale and jurisdiction/effective-date policy.
- Cache namespace generation.

Similarity search is executed only inside that exact partition with server-generated metadata
filters. A global nearest-neighbor search followed by tenant filtering is prohibited.

High-risk, regulated, or high-volume tenants may use a dedicated Redis database, cluster,
index, keyspace, or deployment according to policy. Shared infrastructure still uses tenant
partitioning, quotas, ACL key patterns, encryption, and negative isolation tests.

## 8. Build non-enumerable, version-complete keys

Exact and semantic entries bind these dimensions where applicable:

- Tenant/security/purpose/context fingerprint.
- Canonical query hash and embedding model/version.
- Prompt/context template, output schema, model assignment, and provider-adapter version.
- Chunking, reranker, vector-index, source snapshot, and filter-policy versions.
- Rule/configuration, tool schema, safety, confidence, memory, evaluation, and cache-policy
  versions.
- Language, locale, jurisdiction, data classification, and sensitivity.
- Namespace generation and entry schema version.

Keys are generated with a platform-secret keyed hash/HMAC over canonical structured data.
They never expose raw queries, employee/user IDs, source names, roles, or policy text. Key
building uses a structured canonical serializer, not string concatenation.

Model, embedding, prompt, index, policy, or schema change creates a new key space or namespace;
the new configuration cannot accidentally read an entry evaluated under an old bundle.

## 9. Canonicalize queries without changing meaning

Canonicalization may normalize encoding, whitespace, case where language-safe, and approved
punctuation. It must preserve negation, numbers, dates, units, entity references, jurisdiction,
language, quoted text, and security-relevant terms.

LLM-based query rewriting is not used to build an exact key. A semantic lookup may use an
approved normalized representation, but the original query and transformation version remain
bound to the request evidence. Transformations are evaluated through ADR-034 for meaning
preservation and multilingual behavior.

Queries containing detected PII/sensitive data are ineligible for embedding or response
caching unless a separately approved use case proves minimization, lawful purpose, isolation,
deletion, and no unsafe semantic reuse. Embeddings are treated as potentially sensitive
derived data, not anonymous text.

## 10. Use evaluated similarity threshold, margin, and policy gates

Semantic candidate selection requires all of:

1. Exact hard-partition and metadata-filter match.
2. Same approved embedding model/version and normalization policy.
3. Similarity/distance meeting the effective use-case/language threshold.
4. Sufficient margin from ambiguous competing candidates where the policy requires it.
5. Same version bundle or an explicitly evaluated compatibility rule.
6. Current TTL, source/dependency state, authorization, and safety validation.

No universal vector threshold is permitted. Redis cosine/distance values are adapter
diagnostics, not probabilities. Threshold and margin are calibrated with positive, near-miss,
negation, numeric/date, multilingual, jurisdiction, and adversarial cases under ADR-034.

False semantic hits are more harmful than misses. Initial policy favors strict precision and
falls back to normal retrieval/generation when similarity is uncertain or multiple candidates
are semantically close.

## 11. Revalidate every candidate hit before response release

The hit validator performs this sequence:

1. Confirm current tenant, user, entitlement, purpose, RBAC/ABAC, and security fingerprint.
2. Confirm cache policy, namespace, release-candidate bundle, entry schema, and TTL.
3. Reauthorize every cited source/dependency under the current request.
4. Confirm source approval, version/content hash, effective date, jurisdiction, classification,
   and supersession/deletion state.
5. Confirm current prompt/model/index/safety/confidence/tool/configuration compatibility.
6. Re-run required output leakage, policy, citation, and safety checks.
7. Recompute/validate confidence or refuse cache reuse when the current policy requires it.
8. Record hit/miss/rejection reason and correlation metadata without content.

If any check is unavailable, ambiguous, or fails, the entry is rejected as a miss and queued
for targeted invalidation when appropriate. A cache hit never grants access to a source.

Retrieval-cache hits contain only candidate source IDs/versions/scores by default. Source
content is re-fetched from the authorized canonical store and current filters/reranking may be
reapplied before prompt assembly.

## 12. Write only evaluated and fully validated outputs

An entry may be written only after:

- Normal request authorization and retrieval complete successfully.
- Every material claim is grounded/cited according to the use-case policy.
- Confidence, refusal, safety, privacy, output-schema, and injection controls pass.
- The active release candidate and cache policy passed ADR-034 cache evaluation gates.
- Eligibility confirms no prohibited personal, transactional, live, or sensitive context.
- The response dependency/version manifest is complete.

Cache writes are internal only. A user prompt cannot force `cache=true`, choose a cache key,
modify another entry, lower a threshold, or mark its own response eligible.

Entries are immutable. A new answer/version creates a new entry; compare-and-set prevents
late or lower-quality generation from replacing an approved candidate. Cache-write failure
does not fail a successfully generated response.

## 13. Store minimum encrypted content and complete dependency metadata

Conceptual Redis entry:

```text
AiSemanticCacheEntry
  EntryId, EntrySchemaVersion,
  TenantPartitionHash, SecurityContextFingerprint,
  UseCaseKey, PurposeKey, LocaleKey, JurisdictionKey,
  QueryHash, QueryEmbedding, EmbeddingModelVersion,
  EncryptedResponse, CitationManifestJson,
  SourceDependencyManifestJson, SourceSnapshotVersion,
  ReleaseCandidateId, SystemBundleHash,
  PromptVersion, ModelAssignmentVersion, VectorIndexVersion,
  SafetyPolicyVersion, ConfidencePolicyVersion, CachePolicyVersion,
  NamespaceGeneration, Classification, Sensitivity,
  CreatedDate, AbsoluteExpiresDate, ContentIntegrityHash
```

Raw user/employee identifiers, roles, ABAC attributes, secrets, credentials, hidden reasoning,
full tool payloads, and unnecessary source text are prohibited. Query text is not retained in
semantic cache by default; a keyed query hash and eligible embedding are sufficient for
lookup. Response/citation content is encrypted using approved tenant/platform key policy.

SQL Server stores effective-dated control and audit state:

```text
AI.AiCachePolicy
  AiCachePolicyId, TenantId, UseCaseKey, PolicyVersion,
  EnabledCacheClassesJson, EligibleClassificationJson,
  ProhibitedContextJson, SimilarityPolicyJson, TtlPolicyJson,
  RequiredEvaluationVersion, RequiredConfidencePolicyVersion,
  DependencyPolicyJson, ProviderPromptCachePolicyId,
  PolicyReviewDate, PolicyExpiryDate,
  WarmUpPolicyVersion, WarmUpSourceType, WarmUpApprovalReference,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCacheNamespace
  AiCacheNamespaceId, TenantId, UseCaseKey,
  NamespaceGeneration, SecurityContextVersion,
  SourceSnapshotVersion, SystemBundleHash,
  EffectiveFrom, EffectiveTo, Status,
  NamespaceRotationReason, NamespaceRotationApprovedBy,
  NamespaceRotationEvidenceReference,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCacheWarmUpRun
  AiCacheWarmUpRunId, TenantId, UseCaseKey,
  WarmUpPolicyVersion, WarmUpSourceType,
  WarmUpApprovalReference, SourceManifestHash,
  ReleaseCandidateId, RequestedBy, ApprovedBy,
  StartedDate, CompletedDate, EligibleQueryCount,
  WrittenEntryCount, RejectedEntryCount, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCacheEmergencyControl
  AiCacheEmergencyControlId, TenantId, ScopeType, ScopeKey,
  DisableReads, DisableWrites, IncidentReference,
  DisablementReason, RequestedBy, ApprovedBy,
  EffectiveFrom, EffectiveTo, Status,
  NamespaceRotationReference, ReactivationEvidenceReference,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCacheInvalidationRequest
  AiCacheInvalidationRequestId, TenantId, ScopeType, ScopeKey,
  SourceEventId, Reason, TargetNamespaceGeneration,
  RequestedDate, StartedDate, CompletedDate, Status,
  MatchedEntryCount, DeletedEntryCount, ReconciliationStatus,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiProviderPromptCachePolicy
  AiProviderPromptCachePolicyId, TenantId, ProviderKey,
  UseCaseKey, PermittedPrefixClassesJson,
  ProhibitedContentJson, ProviderCacheKeyPolicyJson,
  TtlPolicyJson, ResidencyPolicyVersion,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCacheIncident
  AiCacheIncidentId, TenantId, UseCaseKey,
  IncidentCategory, Severity, AffectedNamespace,
  EvidenceReference, ContainmentAction, Status,
  OpenedDate, ResolvedDate, RegressionCaseReference,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber
```

Every SQL table has `TenantId`, RLS, tenant-leading indexes, mandatory audit/version columns,
and server-resolved tenant context. High-volume per-hit telemetry is not written as a SQL row;
security incidents, invalidation/administrative actions, and required audit evidence are.

## 14. Use absolute TTL and bounded freshness

TTL is effective-dated by cache class, use case, source volatility, sensitivity, tenant,
jurisdiction, and service tier. It is never a feature-code constant.

- Semantic/exact response entries use absolute expiry; a read does not indefinitely extend
  policy knowledge.
- Embedding/retrieval entries may use separately approved TTL refresh behavior.
- TTL cannot exceed the earliest source expiry, policy review, model/index retirement,
  entitlement, retention, or compliance limit.
- Redis expiry is an optimization and cleanup control, not the only invalidation mechanism.
- Expired entries are not served even if physical deletion is delayed.

Policy/payroll/compliance knowledge does not use stale-while-revalidate. If current source,
permission, effective-date, or policy validation is unavailable, the entry is a miss. A
separate low-risk product-guidance policy may allow clearly bounded stale behavior only after
evaluation and approval.

## 15. Combine versioned namespaces with event-driven invalidation

Correctness does not depend on deleting every entry synchronously. A namespace generation or
bound version change makes old entries unreachable immediately; background deletion reclaims
capacity.

ADR-009 events include or trigger invalidation for:

- `KnowledgeDocumentPublished`, `KnowledgeDocumentSuperseded`, and
  `KnowledgeDocumentDeleted`.
- Source permission, classification, legal hold, or effective-date change.
- `UserPermissionsChanged`, `UserRoleChanged`, `TenantRoleMatrixChanged`, delegation,
  assignment, or employment-status change.
- Prompt/model/embedding/reranker/vector-index/tool/safety/confidence/evaluation/cache-policy
  promotion or retirement.
- Tenant configuration, rule, locale, jurisdiction, purpose, or entitlement change.
- Security incident, poisoning detection, tenant suspension, offboarding, or deletion.

Entries carry source dependencies, and a reverse dependency index supports targeted removal.
Bulk safety invalidation increments the tenant/use-case namespace first, then purges old keys.

Consumers use the transactional outbox, event version/sequence, idempotency, retry, dead-letter
handling, and reconciliation. Per-hit source/authorization/version checks remain mandatory so
a delayed or missed event cannot become a security bypass.

## 16. Defend against poisoning, collision, probing, and semantic confusion

Controls include:

- Only internal post-guardrail writes; no user-controlled keys, metadata, thresholds, or
  eligibility.
- HMAC keys, integrity hashes, immutable entries, and compare-and-set writes.
- Hard tenant/security partition before similarity search.
- Strict evaluated threshold/margin and version compatibility.
- Injection/poisoning detection on query, retrieved source, generated output, and hit output.
- No caching of injection-flagged, unsupported, conflicted, low-confidence, redacted, or
  anomalous responses.
- Per-tenant/user/use-case lookup/write quotas and abuse-rate limits.
- No user-facing disclosure of raw cache status, keys, candidate count, similarity score,
  entry age, or another user's activity.
- Timing/probing anomaly monitoring and uniform authorization before hit/miss behavior.
- Periodic integrity/revalidation sampling and ADR-034 adversarial regression cases.

Cache poisoning or suspected cross-tenant hit is a security incident. The affected namespace
is rotated/disabled immediately, evidence is protected, and reactivation requires approved
root-cause correction and evaluation.

## 17. Prevent stampede and retry amplification

The platform uses scoped request coalescing/single-flight after authorization and exact key
construction:

- Lock scope includes tenant, security/context fingerprint, use case, and canonical key.
- Locks have short leases, owner tokens, bounded wait, and safe expiry.
- A waiter revalidates the completed entry rather than trusting the lock owner.
- No lock or result is shared across tenant/security partitions.
- Failed/unsafe generation is not published to waiters as a cacheable result.
- Provider/retrieval failures use circuit breakers and ADR-033 budgets to prevent retry/cost
  storms.

A cold-cache or mass-invalidation event activates quotas, backpressure, prioritized warm-up,
and provider capacity controls. Warm-up uses approved synthetic or authorized canonical
queries, never harvested employee conversations.

### 17.1 Govern cache warm-up as an approved operation

Warm-up is disabled unless an effective policy records `WarmUpPolicyVersion`,
`WarmUpSourceType`, and `WarmUpApprovalReference`. Permitted source types are versioned
configuration and initially limited to approved synthetic benchmark queries, approved
canonical product/policy questions, or a separately approved tenant-curated set.

- Employee/applicant conversations, prompts, memory, support transcripts, and usage logs are
  prohibited warm-up sources.
- Every query passes the same tenant resolution, eligibility, authorization, retrieval,
  grounding, safety, confidence, write, TTL, quota, and budget controls as normal traffic.
- Warm-up cannot write directly to Redis, bypass ADR-034 gates, reuse another tenant's set,
  lower thresholds, or create personal/live-state entries.
- Execution is scoped, rate-limited, idempotent, auditable, cancellable, and records the
  approved source-manifest hash plus accepted/rejected counts.
- Cold start, disaster recovery, failover, and namespace rotation do not automatically
  authorize warm-up. The active policy/approval and release bundle must still match.

Failed, partially approved, expired, or cancelled warm-up runs do not become promotion
evidence and cannot make ineligible entries reachable.

## 18. Separate provider prompt caching from platform response caching

Provider prompt/context caching can reduce repeated prefix-token processing, but the provider
controls exact semantics, eligible models, token minimums, routing, TTL, retention, and usage
reporting. It does not return a platform-approved cached answer and does not replace local
authorization, retrieval, output validation, or audit.

Initial provider-cache eligibility is limited to approved static content such as:

- Base system/safety instructions.
- Stable tool schemas with no secrets.
- Approved static prompt templates.
- Other prefix content explicitly permitted by tenant/provider processing policy.

Conversation history, employee/applicant data, retrieved confidential documents, live tool
results, secrets, and dynamic authorization context are excluded by default. Any extension
requires provider-contract, residency, retention, deletion, security, privacy, and ADR-034
evaluation approval.

`IPromptCacheAdapter` normalizes provider configuration and usage metadata but does not
pretend provider TTL/cache-sharing semantics are identical. Provider-cache identifiers and
keys are adapter details, never authorization or system-of-record data. If the provider
automatically caches prefixes, provider activation review must document the behavior and
prohibit ineligible content or disable the route.

## 19. Keep conversation memory and personal context out of semantic response cache

ADR-032 remains authoritative:

- Conversation turns, summaries, inferred preferences, and user profiles are not semantic
  response-cache entries.
- A conversation follow-up is not treated as equivalent to a standalone knowledge query
  unless the approved context assembler produces an independently eligible request with no
  personal/session dependency.
- Memory reset/deletion and purpose change cannot be bypassed through a cache hit.
- Qdrant contains no conversation/cache vectors under the initial architecture.

The semantic cache cannot provide long-term recall, personalize a generic answer, or recreate
deleted conversation context.

## 20. Enforce quotas, placement, eviction, and noisy-neighbor controls

Effective-dated controls include per-tenant/use-case/cache-class:

- Maximum entries, bytes, embedding dimensions, candidate count, and response size.
- Lookup/write rate, concurrency, and background invalidation/rebuild capacity.
- Absolute TTL, eviction priority, and minimum reserved capacity where offered.
- Shared versus dedicated Redis placement.
- Provider prompt-cache budget and eligible model/use-case scope.

Eviction policy is selected so cache loss produces a miss, not partial/corrupt output. Control,
lock, idempotency, and security keys are isolated from semantic response eviction domains or
use separate Redis deployments/keyspaces and memory policies.

Production may separate conversation/session Redis, AI semantic cache, and critical platform
cache by cluster or placement policy to avoid one workload evicting or saturating another.
Tenant quotas and bulkheads prevent one tenant from exhausting shared capacity.

## 21. Fail safely as a miss and never serve unverified stale content

- Redis or semantic index unavailable: bypass cache and use normal authorized AI/RAG flow.
- Cache hit validation unavailable: reject hit; continue only if the normal flow can authorize
  and operate.
- Authorization/tenant resolution unavailable: fail closed; do not perform cache lookup.
- Entry decryption/integrity/schema failure: reject, alert, and invalidate.
- Invalidation backlog above policy: rotate/disable affected namespace and treat as miss.
- Embedding mismatch/provider failure: skip semantic lookup; exact eligible cache may still be
  checked if independently valid.
- Provider prompt-cache failure: send a normal approved request without relying on provider
  cache, subject to budget/latency controls.
- Mass cache loss: rate-limit and prioritize regeneration to prevent model/provider cost or
  capacity incidents.

The platform never falls back to a broader tenant partition, older permission fingerprint,
stale source version, unapproved provider cache, or Qdrant response-cache collection.

### 21.1 Provide immediate emergency cache disablement

Authorized operators can disable cache reads and/or writes at global, tenant, or use-case
scope without code deployment. Scope precedence is global, then tenant, then use case; a
more-specific control cannot override a broader active disablement.

Every emergency control requires trusted scope, incident/reference, reason, requester,
approver under the configured severity workflow, effective time, and expiry where appropriate.
Activation is immediate, fully audited, evented, and propagated through a fail-closed control
path independent of semantic-cache availability. Global disablement is restricted to platform
security/operations roles; tenant/use-case disablement is ABAC-scoped.

Disablement causes safe cache bypass and, for poisoning/authorization/isolation incidents,
immediate namespace rotation before asynchronous purge. It does not disable core HRMS,
authorization, audit, deletion, incident response, or the normal AI path when that path is
otherwise safe and available. Reactivation requires containment, purge/reconciliation,
current policy/evaluation, evidence reference, and approval; expiry alone cannot reactivate a
scope after a critical incident.

## 22. Observe cache health without logging content

ADR-031 telemetry includes:

- Exact, semantic, retrieval, embedding, and provider prompt-cache hit/miss/bypass/rejection.
- Rejection reason category: policy, partition, threshold, margin, TTL, dependency, source,
  authorization, version, safety, integrity, or incident.
- Lookup/write/revalidation/invalidation duration and p50/p95/p99 latency.
- False-hit, false-miss, stale-hit, unauthorized-hit, and poisoning-attempt outcomes from
  ADR-034 evaluation/confirmed incidents.
- `CacheReuseRate`, `CacheAvoidedProviderCalls`, `CacheAvoidedTokenUsage`, and
  `CacheValueScore` by approved tenant/use-case/cache-class dimensions.
- `CacheFalsePositiveRate`, `CacheFalseNegativeRate`, and `CacheSemanticDriftRate` with
  metric/evaluator/baseline versions and sample sufficiency.
- Entry/byte/candidate capacity, eviction, expiration, fragmentation, saturation, and
  tenant-quota rejection.
- Invalidation queue age, namespace rotation, purge count, dead letters, and reconciliation.
- Single-flight wait, lock timeout, cold-cache amplification, provider-call avoidance, token,
  latency, and estimated/reconciled cost saving.
- Provider prompt-cache tokens/read/write, expiry, bypass, and provider error where exposed.

Tenant IDs, user/employee IDs, raw/security fingerprints, queries, embeddings, responses,
citations, source IDs, keys, similarity values for individual requests, and secrets are not
general telemetry labels/logs. Authorized drilldown uses restricted audit/evidence records.

Initial service objectives are effective-dated configuration. Mandatory invariants include
zero confirmed unauthorized/cross-tenant cache hits and zero served entries after failed
current authorization/dependency validation.

Effectiveness and quality metrics are defined as follows:

- `CacheReuseRate`: validated cache responses/retrievals reused divided by eligible requests;
  ineligible and bypassed traffic is reported separately.
- `CacheAvoidedProviderCalls`: provider generations proven unnecessary because a validated
  response hit was served; request coalescing and provider prompt-cache hits are separate.
- `CacheAvoidedTokenUsage`: versioned counterfactual token estimate based on the approved
  uncached baseline, reconciled with provider usage where available.
- `CacheValueScore`: versioned composite of validated latency/cost/load benefit minus
  infrastructure, embedding, validation, false-hit, stale-hit, and incident cost. It is a
  decision-support score, not authorization or a quality gate override.
- `CacheFalsePositiveRate`: semantic hits that should have been misses or generated a
  materially non-equivalent answer.
- `CacheFalseNegativeRate`: eligible equivalent requests missed by the evaluated cache.
- `CacheSemanticDriftRate`: increase in false-positive/false-negative or answer-equivalence
  degradation against the approved baseline after embedding, corpus, query, provider, or
  population change.

Metric formulas, baselines, confidence intervals, sample requirements, exclusions, and
evaluator versions are effective-dated. Unknown/insufficient labels remain visible and are
not counted as successful reuse.

## 23. Gate cache policy and threshold changes through ADR-034

Each cache-enabled release candidate is evaluated against:

- Exact and semantic hit correctness.
- Semantic false-hit and false-miss rate by language/jurisdiction/slice.
- Negation, number, date, entity, policy-version, and near-neighbor confusion.
- Cross-tenant, cross-user, permission, purpose, and ABAC boundary attacks.
- Stale source/effective-date/permission rejection and invalidation completion.
- Poisoning, key collision, cache probing, timing, replay, and concurrent-write attacks.
- Citation/grounding/confidence/safety non-inferiority against uncached generation.
- Redis outage, corruption, eviction, cold start, mass invalidation, and recovery.
- Latency, token, embedding, provider, storage, and cost impact.

Similarity threshold, margin, canonicalization, embedding, cache eligibility, TTL, provider
prompt policy, and hit-validation changes are material release-candidate changes. They require
versioned benchmark evidence and promotion approval. A higher cache-hit rate is not a quality
goal when false/stale/unauthorized reuse increases.

## 24. Integrate cost governance without making cache mandatory

ADR-033 records cache infrastructure, embeddings, lookup/write operations, provider cached
tokens, avoided calls, and estimated/reconciled savings by tenant/use case/provider/cache
class. Savings reports separate:

- Exact response hit.
- Semantic response hit.
- Retrieval/embedding hit.
- Provider prompt/context cache hit.
- Request coalescing.

FinOps reporting includes `CacheReuseRate`, `CacheAvoidedProviderCalls`,
`CacheAvoidedTokenUsage`, and `CacheValueScore` with baseline/method versions. Avoided calls
or tokens cannot be double-counted across semantic response, request coalescing, retrieval,
and provider prompt-cache layers. Estimated savings remain distinct from reconciled provider
cost and from the cost of Redis, embeddings, validation, operations, and incidents.

The platform accounts for the cost of hit validation and query embedding. An entry is not
cached solely because it is expensive; it must remain eligible and evaluated.

Budget pressure may disable cache writes, shorten retention, or choose an approved cheaper
embedding adapter, but cannot broaden partitions, lower safety/quality gates, extend stale
content, or permit personal response caching. Cache outage/cold-start forecasts prevent an
unexpected provider-spend surge.

## 25. Define versioned API and permission requirements

The Phase 6D OpenAPI package must include:

| Endpoint | Permission | Behavior |
|---|---|---|
| `GET /api/v1/ai/admin/cache-policies` | `AI.ViewCache` | Tenant-scoped current/future policies and evaluation state |
| `PUT /api/v1/ai/admin/cache-policies/{policyId}` | `AI.ManageCache` | Create immutable future-effective policy version |
| `GET /api/v1/ai/admin/cache-health` | `AI.ViewCache` | Own-tenant class health, capacity, hit/rejection, invalidation, and incident state |
| `POST /api/v1/ai/admin/cache-invalidations` | `AI.InvalidateCache` | Request scoped namespace/source/policy invalidation with reason |
| `GET /api/v1/ai/admin/cache-invalidations/{id}` | `AI.ViewCache` | Status, counts, reconciliation, and failure without entry content |
| `POST /api/v1/ai/admin/cache-namespaces/{id}/rotate` | `AI.InvalidateCache` | Immediate generation rotation with reason, approver, evidence, and asynchronous purge |
| `POST /api/v1/ai/admin/cache-warm-up-runs` | `AI.WarmUpCache` | Execute approved policy/source manifest through normal eligibility and budget controls |
| `GET /api/v1/ai/admin/cache-warm-up-runs/{id}` | `AI.ViewCache` | Audited accepted/rejected/write counts and execution status |
| `POST /api/v1/ai/admin/cache-emergency-controls` | `AI.EmergencyDisableCache` | Immediately disable scoped reads/writes with incident, reason, approval, and expiry policy |
| `POST /api/v1/ai/admin/cache-emergency-controls/{id}/reactivate` | `AI.EmergencyDisableCache` | Reactivate only after purge/reconciliation/evaluation evidence and approval |
| `GET /api/v1/platform/ai/cache-providers` | `AI.ManageCacheProviders` | Restricted adapter/capability/placement health |
| `PUT /api/v1/platform/ai/cache-providers/{id}` | `AI.ManageCacheProviders` | Future-effective provider configuration/placement version |

Initial permissions:

| Permission | Scope |
|---|---|
| `AI.ViewCache` | View authorized own-tenant policy and aggregate health |
| `AI.ManageCache` | Create future-effective own-tenant cache policy versions within platform limits |
| `AI.InvalidateCache` | Rotate/invalidate authorized tenant/use-case/source scope |
| `AI.WarmUpCache` | Execute only an approved scoped warm-up policy and source manifest |
| `AI.EmergencyDisableCache` | Disable/reactivate cache scope; global scope restricted to platform Security/Operations |
| `AI.ManageCacheProviders` | Restricted platform adapter, placement, capability, and provider prompt-cache management |
| `AI.ViewAllCacheHealth` | Restricted cross-tenant aggregate operational health without content |

No administrative endpoint returns raw queries, embeddings, response bodies, keys, security
fingerprints, provider cache keys, or another tenant's cache detail. Break-glass access does
not make cache content generally browsable.

All endpoints use `/api/v1`, JWT, trusted tenant context, RBAC plus ABAC, correlation IDs,
standard envelopes, pagination/filter limits, rate limits, and audit. Mutations require
`Idempotency-Key`, reason, effective date where applicable, and optimistic concurrency.
OpenAPI documentation and contract/security/isolation tests are mandatory.

## 26. Publish low-content cache events through the outbox

ADR-009 events include:

- `AiCachePolicyChanged`
- `AiCacheNamespaceRotated`
- `AiCachePolicyReviewDue`
- `AiCachePolicyExpired`
- `AiCacheWarmUpStarted`
- `AiCacheWarmUpCompleted`
- `AiCacheWarmUpFailed`
- `AiCacheEmergencyDisabled`
- `AiCacheEmergencyReactivated`
- `AiCacheInvalidationRequested`
- `AiCacheInvalidationCompleted`
- `AiCacheInvalidationFailed`
- `AiCacheReconciliationRequired`
- `AiCachePoisoningSuspected`
- `AiCacheCrossTenantIncidentDetected`
- `AiCacheCapacityThresholdCrossed`
- `AiCacheProviderDegraded`
- `AiCacheProviderRecovered`
- `AiCacheQualityDriftDetected`

High-volume cache hits/misses are telemetry, not domain events. Events contain identifiers,
versions, scope, reason category, severity, status, and correlation data only. They do not
contain query/response content, embeddings, keys, citations, source text, employee data,
credentials, or permission attributes. Consumers are idempotent.

## 27. Apply retention, deletion, legal hold, backup, and offboarding controls

Cache retention is bounded by ADR-022 before implementation approval. Cache TTL is always no
longer than the controlling data/policy retention and is usually materially shorter.

Semantic/retrieval/embedding caches are derived and rebuildable. Production backup/persistence
is disabled by default unless an approved availability requirement justifies it and deletion,
encryption, restore isolation, and expiry-on-restore are proven.

Deletion/offboarding covers:

- Redis entries, vector indexes, secondary indexes, replicas, snapshots/backups where enabled,
  exports, warm-up inputs, and dependency indexes.
- Provider prompt/context cache state to the extent supported by provider contract/API, with
  documented residual TTL when immediate deletion cannot be proven.
- Namespace rotation before asynchronous physical purge.
- Restore/rebuild tests proving deleted/expired entries do not reappear or become reachable.

Legal hold applies to authoritative source/audit records, not automatic continued serving of
cached content. Held content is not made available to AI merely because a cache copy exists.

## 28. Define operations, disaster recovery, and incident runbooks

Required runbooks include:

- Redis outage, failover, corruption, saturation, and recovery.
- Semantic index rebuild and entry-schema migration.
- Cache poisoning, cross-tenant suspicion, key compromise, and integrity failure.
- Invalidation backlog/dead letter, source dependency mismatch, and namespace rotation.
- Permission/policy event loss and reconciliation.
- Cold-cache/provider cost storm and controlled warm-up.
- Provider prompt-cache privacy/retention incident.
- Tenant offboarding/deletion proof and restore validation.

Because cache is derived, recovery prioritizes secure disablement/miss behavior over restoring
old response entries. Recovery point objectives may be `no cache restore`; service recovery
time covers returning to safe miss behavior first and optional cache rebuild later.

### 28.1 Use risk- and scale-based Redis high-availability profiles

Initial local development may use a standalone version-pinned Redis instance. Production
cannot use a single unprotected node unless an explicitly approved low-risk deployment can
meet availability through immediate cache bypass.

Approved production profiles are:

- **Redis Sentinel profile:** primary-replica deployment with an odd quorum of at least three
  failure-domain-separated Sentinel voters for automatic primary failover when one shard is
  sufficient.
- **Redis Cluster profile:** multiple primary shards with replicas distributed across
  failure domains for horizontal capacity, partitioned indexes, and automatic shard failover.
- **Dedicated profile:** isolated Sentinel/Cluster deployment for regulated, high-volume, or
  high-risk tenants when shared placement cannot meet isolation/capacity policy.

Profile choice is effective-dated configuration based on data volume, vector-index size,
throughput, tenant isolation, failure domains, maintenance, and service tier. Clients use
topology-aware discovery, bounded retries, circuit breakers, connection limits, and safe
miss behavior. Failover, split-brain/network partition, rolling patch, node loss, zone loss,
resynchronization, and stale-replica scenarios are rehearsed.

Semantic cache content has an initial logical RPO of zero restored entries because it is
derived and may be discarded. Safe cache-bypass RTO is immediate at the application layer;
the infrastructure recovery and optional warm-up targets are defined by service tier in
ADR-031. Redis persistence/backups are disabled by default. When enabled for a justified
recovery/cost objective, RDB/AOF/snapshot policy, encryption, retention, offsite access,
expiry-on-restore, namespace compatibility, deletion proof, RPO/RTO, and restore isolation
must be approved and tested. Persistence can never make an expired or rotated namespace
reachable.

## 29. Deliver cache capability in controlled increments

Implementation documentation must preserve this order:

1. Policy, eligibility, HMAC key builder, tenant/security partitioning, exact/embedding cache,
   TTL, quotas, encryption, and safe miss behavior.
2. Retrieval cache with per-hit source reauthorization and event/namespace invalidation.
3. Semantic response cache with Redis vector filters, strict calibrated thresholds/margins,
   dependency manifests, poisoning controls, and ADR-034 evidence.
4. Single-flight, capacity isolation, reconciliation, dashboards, incidents, and operations.
5. Optional provider prompt/context-cache adapters after contract/privacy/residency review.
6. Any future alternate semantic-cache store only after portability, deletion, isolation,
   performance, cost, and security evaluation.

No later increment may bypass an earlier control. No cache code starts until the
constitutional Business, Technical, Database, UI, and Test documents plus Security and
OpenAPI requirements are Approved.

---

# Alternatives Considered

## Do not cache AI/RAG operations

Strong simplicity and freshness but repeats embeddings, retrieval, and provider generation,
increasing latency, cost, and capacity. Retained as a supported policy mode, rejected as the
only platform mode.

## Cache every model response by query text

Maximizes reuse but ignores authorization, personalization, source versions, effective dates,
prompt/index changes, and semantic risk. Rejected.

## Share one semantic cache across tenants

Could improve hit rate but violates tenant isolation and commercial/privacy boundaries.
Rejected; no cross-tenant reuse is permitted.

## Use Qdrant for response-cache vectors first

Would reuse existing vector infrastructure but mixes short-lived derived answers with
approved canonical knowledge and conflicts with the current ADR-032 boundary. Rejected for
the initial architecture; requires a future ADR amendment and separate placement.

## Use only provider prompt caching

Reduces repeated prefix processing but does not cache approved responses/retrieval and has
provider-specific TTL/routing/retention behavior. Rejected as the platform cache architecture;
retained as optional adapter optimization.

## Trust TTL as the only freshness control

Simple but cannot react immediately to permission, policy, source, incident, or effective-date
change. Rejected in favor of versioned keys, namespace rotation, events, and per-hit checks.

## Reauthorize only when writing an entry

Permissions and sources can change after write. Rejected; every hit reauthorizes and validates
current dependencies.

## Use one similarity threshold globally

Distance scales and ambiguity differ by embedding, language, corpus, and use case. Rejected in
favor of evaluated effective-dated thresholds and margins.

## Require a paid managed semantic-cache service first

May reduce operational work but adds initial cost and lock-in. Rejected as mandatory. The
first adapter is local/self-hosted Redis; managed providers remain optional adapters.

---

# Consequences

## Positive

- Repeated eligible knowledge answers can reduce latency, tokens, cost, and infrastructure
  load without becoming authorization or system-of-record data.
- Redis-first development avoids a mandatory managed-cache subscription.
- Hard tenant/security partitions and per-hit reauthorization protect isolation.
- Source/version manifests and namespace invalidation prevent common stale reuse.
- Qdrant remains cleanly focused on canonical approved knowledge vectors.
- Provider prompt caches remain optional and do not weaken portability.
- Cache changes are evaluated and promoted as part of the full ADR-034 system bundle.
- Cache loss safely degrades to a miss.

## Negative

- Per-hit reauthorization, dependency checks, output guards, and query embedding reduce some
  latency savings.
- Redis vector search, indexes, encryption, quotas, and invalidation add operational complexity.
- Strict eligibility excludes many personal/live HR use cases with high theoretical reuse.
- Provider prompt-cache behavior cannot be normalized perfectly.
- Cold starts or namespace rotations may temporarily increase provider cost and latency.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Cross-tenant/permission hit | Trusted scope first, hard partition/filter, fingerprint versions, per-hit authorization, negative tests |
| False semantic hit | Strict evaluated threshold/margin, near-miss suites, miss fallback, no universal score |
| Stale policy/source answer | Version-complete key, dependency hash, absolute TTL, namespace event, per-hit source check |
| Poisoned response persists | Internal post-guardrail writes, injection checks, immutability, integrity hash, incident rotation |
| Personal data cached | Deny-by-default eligibility, classification, no personal/live response cache, encryption, audit |
| Query/key probing | HMAC keys, no raw status/score disclosure, rate/anomaly controls, authorization before lookup |
| Delayed invalidation event | Namespace/version makes old entry unreachable; per-hit checks; reconciliation |
| Cache stampede after loss | Tenant-scoped single-flight, rate limits, circuit breaker, budget/capacity controls |
| Redis workload evicts critical keys | Separate placement/keyspace/eviction domain, quotas, bulkheads, monitoring |
| Provider cache retains sensitive prefix | Static-only default, provider policy/DPA/residency review, optional/disable route |
| Cost savings hide quality regression | ADR-034 non-inferiority, false/stale-hit metrics, quality gates independent of cost |
| Backup restores deleted/stale entry | Backup disabled by default; namespace versions, expiry-on-restore, deletion/restore tests |
| Adapter lock-in | Provider-neutral contracts, capability registry, portability evaluation |
| Cache value is overstated | Versioned counterfactuals, no cross-layer double count, include infrastructure/validation/incident cost |
| Policy remains active after assumptions change | Review/expiry dates, warnings, safe disablement, immutable renewal version |
| Warm-up introduces private or unsafe entries | Approved source manifest, no conversations, normal eligibility/guards, audit and quotas |
| Embedding/threshold quality drifts | Explicit false-positive/false-negative/semantic-drift signals and ADR-034 revalidation |
| Incident containment needs deployment | Global/tenant/use-case emergency disablement, namespace rotation, controlled reactivation |
| Redis node/zone failure disrupts cache | Sentinel/Cluster profiles, replicas/failure domains, topology-aware client, safe miss |
| Namespace rotation lacks evidence | Required reason, approver, evidence reference, immutable audit and event |

---

# Acceptance Criteria Before Approval/Implementation

| ID | Criterion |
|---|---|
| CA-AC-001 | Semantic/exact response caching is disabled by default and enabled only through an effective-dated evaluated tenant/use-case policy. |
| CA-AC-002 | Cache is disposable derived data and cannot authorize, become a system of record, replace current sources, or recreate deleted memory. |
| CA-AC-003 | Initial development uses version-pinned self-hosted Redis behind `ICacheProvider`/`ISemanticCacheStore`; no managed cache subscription is mandatory. |
| CA-AC-004 | Qdrant remains the canonical knowledge-vector store and contains no semantic response, conversation, or user-preference cache vectors. |
| CA-AC-005 | Employee/applicant/payroll/attendance/leave/health/disciplinary/performance/recruitment/live-workflow and other personal/transactional responses are not cached by default. |
| CA-AC-006 | Tenant, user, RBAC/ABAC, delegation, purpose, classification, locale/jurisdiction, and security context are resolved from trusted server state before lookup. |
| CA-AC-007 | Similarity search occurs only after hard tenant/security partition and metadata filtering; global search followed by tenant filtering is prohibited. |
| CA-AC-008 | Keys use centralized structured canonicalization and HMAC and expose no query, user, employee, role, source, or policy content. |
| CA-AC-009 | Keys/entries bind prompt, model, embedding, index, source, tool, safety, confidence, evaluation, policy, schema, and namespace versions where applicable. |
| CA-AC-010 | Semantic thresholds/margins are effective-dated, embedding/language/use-case specific, ADR-034 evaluated, and never treated as universal probabilities. |
| CA-AC-011 | Every candidate hit revalidates current authorization, sources, versions/hashes, effective dates, jurisdiction, safety, citations, confidence, integrity, TTL, and policy before release. |
| CA-AC-012 | A failed or unavailable hit validation produces a miss and cannot fall back to a broader/older tenant, permission, source, or provider cache scope. |
| CA-AC-013 | Retrieval-cache content is limited to authorized source/version/rank/filter metadata by default; source bodies are re-fetched and reauthorized. |
| CA-AC-014 | Only post-guardrail grounded/cited/high-enough-confidence eligible outputs are written; users cannot force cache writes, keys, thresholds, or eligibility. |
| CA-AC-015 | Cache entries are immutable, encrypted, integrity-protected, TTL-bound, size-limited, and contain no hidden reasoning, secrets, raw authorization attributes, or unnecessary source/tool payloads. |
| CA-AC-016 | Absolute TTL cannot exceed source/policy/model/index/entitlement/retention limits and reads cannot make semantic policy answers live indefinitely. |
| CA-AC-017 | Document, permission, role matrix, assignment, employment, model/prompt/index/tool/safety/policy, incident, suspension, and offboarding changes make affected entries unreachable and trigger idempotent purge/reconciliation. |
| CA-AC-018 | Cross-tenant, cross-user, permission-change, guessed-key, collision, injection, poisoning, probing, timing, replay, and concurrent-write tests produce zero unauthorized hits/disclosures. |
| CA-AC-019 | Tenant-scoped single-flight prevents duplicate generation without sharing locks/results across security partitions or publishing failed/unsafe output. |
| CA-AC-020 | Provider prompt caching is optional, adapter-controlled, static-content-only by default, contract/residency/retention reviewed, and never replaces platform validation. |
| CA-AC-021 | Conversation turns, summaries, inferred preferences, and deleted/reset memory cannot enter or be reconstructed from semantic response cache. |
| CA-AC-022 | Per-tenant/use-case quotas, placement, eviction, candidate, rate, byte, and concurrency controls prevent noisy-neighbor impact. |
| CA-AC-023 | Redis/index/provider-cache outage or corruption degrades to safe miss; tenant/authorization failure remains fail-closed and core HRMS continues without cache. |
| CA-AC-024 | Invalidation backlog/dead-letter beyond policy rotates/disables the namespace before stale/security-risk content can be served. |
| CA-AC-025 | Telemetry reports class-level hit/miss/rejection, false/stale/unauthorized hit, invalidation, capacity, latency, cost, and incident health without sensitive content/identifiers. |
| CA-AC-026 | ADR-034 evaluation proves cached answers are non-inferior for grounding, citations, confidence, safety, fairness where applicable, and mandatory language/jurisdiction slices. |
| CA-AC-027 | Higher hit rate or lower cost cannot approve increased false, stale, unsafe, poisoned, or unauthorized reuse. |
| CA-AC-028 | ADR-033 tracks Redis/embedding/provider-cache cost and savings by tenant/use case/cache class without weakening cache policy. |
| CA-AC-029 | Cache APIs are versioned, OpenAPI-documented, tenant-isolated, RBAC/ABAC protected, idempotent for mutations, audited, rate-limited, and contract-tested. |
| CA-AC-030 | Cache events use the outbox, are idempotent, and contain no queries, answers, embeddings, keys, employee data, credentials, source text, or permission attributes. |
| CA-AC-031 | Tenant deletion/offboarding rotates namespaces and removes eligible Redis indexes/entries, replicas, enabled backups/snapshots, exports, dependency indexes, and supported provider cache state. |
| CA-AC-032 | Restore/rebuild tests prove deleted/expired entries do not reappear or become reachable and tenant isolation remains intact. |
| CA-AC-033 | Cache provider replacement uses adapters/configuration and requires no AI feature-code change or loss of invalidation/security semantics. |
| CA-AC-034 | Unit coverage is at least 85%, with integration, isolation, security, concurrency, performance, expiry, invalidation, poisoning, outage, deletion, restore, API, and end-to-end tests. |
| CA-AC-035 | Effectiveness reporting exposes versioned `CacheReuseRate`, `CacheAvoidedProviderCalls`, `CacheAvoidedTokenUsage`, and `CacheValueScore` without double counting or treating estimates as reconciled savings. |
| CA-AC-036 | Every cache policy records `PolicyReviewDate` and `PolicyExpiryDate`, generates warnings, disables safely when overdue/expired, and requires an immutable reviewed version for renewal. |
| CA-AC-037 | Warm-up records `WarmUpPolicyVersion`, `WarmUpSourceType`, and `WarmUpApprovalReference`; uses no employee/applicant conversations and passes normal eligibility, authorization, safety, evaluation, quota, and budget controls. |
| CA-AC-038 | Production monitoring reports versioned `CacheFalsePositiveRate`, `CacheFalseNegativeRate`, and `CacheSemanticDriftRate` with sample sufficiency and triggers severity-based revalidation/disablement. |
| CA-AC-039 | Authorized global, tenant, and use-case emergency disablement takes effect without deployment, is audited/evented, supports namespace rotation, and cannot reactivate critical-incident scope without evidence and approval. |
| CA-AC-040 | Production Redis deployment uses an approved standalone-bypass, Sentinel, Cluster, or dedicated profile with tested failover, failure-domain placement, client topology handling, persistence decision, and service-tier RPO/RTO. |
| CA-AC-041 | Every namespace rotation records `NamespaceRotationReason`, `NamespaceRotationApprovedBy`, and `NamespaceRotationEvidenceReference` and preserves immutable investigation/audit history. |

---

# Impact

## Architecture

Adds cache eligibility, HMAC key building, hard partitioning, semantic lookup, hit validation,
dependency registry, namespace invalidation, provider prompt-cache adapters, request
coalescing, governed warm-up, emergency disablement, cache-quality drift, and cache
incident/reconciliation services. Redis is the first ephemeral semantic cache store; Qdrant
remains the canonical knowledge-vector store.

## Database and Cache Storage

Adds `AI.AiCachePolicy`, `AI.AiCacheNamespace`, `AI.AiCacheInvalidationRequest`,
`AI.AiCacheWarmUpRun`, `AI.AiCacheEmergencyControl`, `AI.AiProviderPromptCachePolicy`, and
`AI.AiCacheIncident` in SQL Server with RLS, effective dates, mandatory audit/version columns,
and tenant-leading indexes. Policy review/expiry, warm-up approval, emergency scope, and
namespace rotation evidence are explicit. Redis entry and
index design must define encrypted payload, vector type/dimension, metadata schema, key
prefix/ACL, HMAC, TTL, quotas, eviction, namespace, integrity, and migration behavior.

## Security and Privacy

Adds deny-by-default eligibility, hard pre-search tenant/security filters, per-hit current
authorization/source validation, poisoning/probing/collision controls, encrypted entries,
provider-cache data policy, and immediate namespace rotation. Cache content cannot become a
secondary employee profile, permission source, or hidden retention path.

## Performance and Cost

Exact/semantic/retrieval/embedding/provider-prefix hits can reduce latency, tokens, provider
calls, Qdrant/source load, and cost. Query embedding, metadata filtering, reauthorization,
source checks, decryption, safety validation, and strict thresholds consume some benefit.
Capacity, cold-start, invalidation, and stampede behavior require load and cost testing.

## Development and Delivery

Requires Business, Technical, Database, UI, Test, Security, Operations, and OpenAPI documents
before code. Cache policy/version must be included in the ADR-034 release-candidate bundle;
CI/CD promotion binds the evaluated cache configuration and Redis entry schema exactly.

## Operations

Operations owns Redis placement/version/patching, capacity, ACL/TLS, expiry/eviction,
Sentinel/Cluster failover, persistence/RPO/RTO decisions, invalidation/reconciliation,
governed warm-up, emergency disablement, cache-quality drift, cold-start controls, incident
runbooks, deletion/restore proof, and provider cache health. Security/Privacy own eligibility and incident controls; Product/AI
and domain owners own use-case/quality/TTL policy; Finance owns cost/saving governance.

---

# Official and Primary References

- RedisVL semantic cache guide:
  `https://docs.redisvl.com/en/latest/user_guide/03_llmcache.html`
- Redis vector search concepts:
  `https://redis.io/docs/latest/develop/ai/search-and-query/vectors/`
- Redis key expiration:
  `https://redis.io/docs/latest/commands/expire/`
- Redis Access Control Lists:
  `https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/`
- Anthropic prompt caching:
  `https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching`
- OpenAI prompt caching:
  `https://platform.openai.com/docs/guides/prompt-caching`
- Google Gemini context caching:
  `https://ai.google.dev/gemini-api/docs/caching`
- OWASP prompt injection risk:
  `https://genai.owasp.org/llmrisk/llm01-prompt-injection/`
- NIST AI 600-1, Generative AI Profile:
  `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`

Provider documentation illustrates optional provider-cache behavior only and does not create
a provider dependency. Capability, retention, pricing, model, and legal terms must be
revalidated before each provider/use-case activation.

References last validated: 2026-06-25.

---

# Approval

Solution Architect: Approved (Codex)  
Prompt/Context Architect: Architecture controls incorporated  
Security Architect: Security controls incorporated  
Database Architect: Database controls incorporated  
Operations Architect: Operations/HA controls incorporated  
Privacy Reviewer: Privacy controls incorporated  
Product Owner: Bhajan Lal - Approved 2026-06-25

(Status: Approved)
