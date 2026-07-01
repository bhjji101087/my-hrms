# ADR-030 - Enterprise Vector Store Strategy

Architecture Decision Record

Date: 2026-06-22
Status: Approved
Approved By: Bhajan Lal (Product Owner)
Approved Date: 2026-06-22

Related documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md` - Approved v2.1
- ADR-005 Multi-Tenancy Model
- ADR-006 Tenant Context and Data Access
- ADR-008 Identity and Access Management
- ADR-019 Enterprise AI / RAG Platform Architecture - Approved
- ADR-027 Provider-Abstraction Framework

---

# Context

The AI platform needs vector retrieval for tenant policies, SOPs, handbooks, FAQs, and
approved compliance knowledge. The store must support hybrid retrieval, rich metadata
filters, strong tenant boundaries, versioned indexing, backup/recovery, encryption,
provider portability, and predictable operations for tenants of approximately 50 to
10,000 employees.

The decision must not:

- Make a vector index the system of record.
- Trust a caller-supplied tenant identifier.
- Depend on shared filtering as the only tenant-isolation control.
- Couple AI feature code to a vendor SDK or query language.
- Replace the general HRMS search-provider decision. Global application search and AI
  vector retrieval have different data, lifecycle, security, and evaluation requirements.

The approved AI Strategy evaluated pgvector, Qdrant, Pinecone, Weaviate, Azure AI Search,
and OpenSearch Vector Search. ADR-027 requires thin provider abstractions and adapters built
only for validated deployment needs.

---

# Decision

## 1. Create a separate VectorStore provider category

Add `VectorStore` as a provider type in the ADR-027 registry. AI code depends only on a
thin `IVectorStore` contract. The existing general `ISearchProvider` remains responsible
for application search and is not changed by this ADR.

The same product may use Elasticsearch for global search and Qdrant for AI vectors. A
provider may implement both categories, but configuration and contracts remain separate.

The minimum `IVectorStore` capabilities are:

- Create and validate an immutable index version.
- Upsert/delete chunks within a trusted tenant partition.
- Hybrid keyword/vector retrieval with structured metadata filters.
- Return stable source IDs, relevance values, and provider diagnostics.
- Report health and supported capabilities.
- Promote/rollback an index alias or placement pointer.
- Export snapshot metadata or support deterministic rebuild.

Vendor-specific query objects, SDK models, and score semantics cannot cross the adapter
boundary.

## 2. Use self-hosted Qdrant as the first adapter

Qdrant is the first adapter for development and initial deployment. It can run locally or
self-hosted without a paid managed vector-search subscription and provides purpose-built
vector retrieval, payload filtering, custom shard/tenant partition options, snapshots,
and a portable deployment path.

Initial development uses a version-pinned Qdrant container and persistent local/test
storage. Production use requires approved infrastructure, encryption, backup, monitoring,
patching, scaling, and operational ownership. Open-source software avoids a managed-service
subscription; it does not make production infrastructure or operations free.

Activation still requires the isolation, security, performance, recovery, and acceptance
criteria in this ADR to pass.

## 3. Keep Azure AI Search as an optional later adapter

Azure AI Search may be added later for a tenant or service tier that chooses paid managed
Azure capabilities. It implements the same `IVectorStore` contract and is registered in
the provider catalog without changing AI feature code.

For a new tenant with no vectors, selection is configuration-driven. For an existing
tenant, the target Azure index must be rebuilt from canonical source documents, validated,
and promoted through the normal placement switch. Pinecone, Weaviate, OpenSearch, and
pgvector remain other future adapters, added only for validated demand.

## 4. Require a hard tenant partition

Tenant placement is resolved from trusted `ITenantContext` plus server-side catalog data.
The client cannot select or override tenant placement.

Isolation order:

1. Use a provider-native hard namespace, tenant partition, or collection where it provides
   an enforceable boundary.
2. If the provider cannot guarantee that boundary, use a dedicated index/collection per
   tenant.
3. Regulated, residency-bound, or high-volume tenants may use a dedicated provider
   service/cluster through catalog configuration.

For Qdrant, use a server-resolved tenant shard key or dedicated collection as the primary
partition, plus mandatory `TenantId` payload filtering and post-retrieval validation. A
regulated or high-volume tenant may receive a dedicated Qdrant collection or cluster.

For a future Azure AI Search adapter, use a dedicated tenant index because a shared
`TenantId` filter alone does not provide the required defense-in-depth. A placement
controller maps tenant indexes across services, subscriptions, and regions as capacity
grows.

`TenantId` remains metadata inside every chunk and is revalidated after retrieval even when
the physical index is tenant-dedicated. Cross-tenant retrieval must fail closed.

## 5. Keep source documents and SQL metadata authoritative

- Source files remain in the approved storage provider.
- Knowledge/document/index metadata remains in tenant-scoped SQL Server `AI` tables.
- Vector indexes and embeddings are derived, reproducible data.
- Deleting a source creates an audited deletion/tombstone event and removes eligible
  vectors, memory, and cache entries according to approved retention policy.

The future DB design must include at least:

- `AI.KnowledgeDocument`
- `AI.KnowledgeDocumentVersion`
- `AI.KnowledgeChunk`
- `AI.VectorPlacement`
- `AI.VectorIndexVersion`
- `AI.IngestionJob`

Every tenant-scoped table follows database standards, including `TenantId`, audit columns,
soft deletion, version number, RLS, and tenant indexes.

## 6. Use immutable versioned indexes

Each index version records:

- Tenant and placement IDs.
- Source-document manifest and content hashes.
- Chunking profile/version.
- Embedding provider, model, dimensions, and version.
- Vector adapter/provider version.
- Retrieval profile and metadata schema version.
- Build, validation, promotion, rollback, and retirement state.

Embedding models or dimensions are never mixed within an index version. A document,
chunking, embedding, or metadata-schema change builds a shadow index. The shadow version
must pass retrieval, citation, permission, isolation, performance, and cost tests before an
atomic catalog/alias promotion. The previous version remains available for rollback during
the approved safety window.

## 7. Standardize indexing and retrieval policy

The default retrieval profile is hybrid keyword plus approximate-nearest-neighbor vector
search. HNSW is the default algorithm where supported; algorithm, vector compression,
candidate count, top-k, and reranking are adapter capabilities and versioned configuration.

Every chunk carries:

`TenantId`, `DocumentId`, `ChunkId`, `SourceType`, `Section`, `DocumentVersion`,
`EffectiveFrom`, `EffectiveTo`, `Locale`, `Jurisdiction`, `Sensitivity`, `PermissionTags`,
`ApprovalStatus`, `EmbeddingModelVersion`, and `ContentHash`.

Retrieval applies these controls in order:

1. Resolve the hard tenant partition.
2. Restrict to approved, effective, authorized, locale/jurisdiction-compatible sources.
3. Execute hybrid retrieval.
4. Rerank only the already-authorized candidate set.
5. Revalidate tenant, permissions, sensitivity, version, and source status.
6. Return stable source identifiers for citation and audit.

Vendor relevance scores are normalized only for ranking/diagnostics. They are not treated
as a universal probability and do not alone determine response confidence.

## 8. Enforce encryption and provider security

- TLS 1.2 or higher is required in transit.
- Provider-supported encryption at rest is mandatory.
- Customer-managed keys are supported where the provider/service tier permits.
- Provider credentials use tenant-scoped secret references and least privilege.
- Public network access is disabled where private connectivity is available and required.
- Customer-managed endpoints require egress allow-listing, SSRF controls, certificate
  validation, health checks, and an approved support boundary.
- Provider logs and metrics cannot contain source text, prompts, answers, credentials, or
  employee identifiers.

## 9. Use snapshot where available and deterministic rebuild everywhere

The recovery design does not depend on a provider-specific snapshot feature.

- Source files, SQL metadata, index manifests, embedding configuration, and aliases are
  backed up under existing platform controls.
- Provider snapshots are used when supported and validated, but rebuild from canonical
  sources remains mandatory.
- Restore/rebuild occurs into a new version and must repeat isolation, retrieval, citation,
  and permission tests before promotion.
- Initial targets from the approved strategy are: source metadata RPO <= 15 minutes,
  vector index RPO <= 24 hours, and AI retrieval RTO <= 4 hours.
- Disaster-recovery exercises must prove both data recovery and tenant separation.

## 10. Scale through catalog-driven placement and quotas

`AI.VectorPlacement` maps each tenant to provider, region, service/cluster, index/collection,
active version, and recovery placement. Placement is configuration, so moving a tenant or
dedicating capacity does not change feature code.

Capacity controls include:

- Per-tenant document, chunk, storage, query, concurrency, and ingestion quotas.
- Provider service/index limits monitored before exhaustion.
- Bulkheads, timeouts, circuit breakers, and asynchronous ingestion.
- Separate ingestion and query capacity where the provider supports it.
- Noisy-neighbor monitoring and promotion to dedicated placement by approved policy.
- Benchmarks at representative small, medium, large, and two-times forecast tenant volumes.

The vector retrieval target is p95 <= 1.5 seconds under the approved workload profile.
No performance target can relax tenant or permission controls.

## 11. Govern cost without hardcoded vendor prices

Record vector-service capacity, storage, ingestion, embedding, query, reranking, network,
and operational costs in the tenant usage/cost ledger. Prices are effective-dated registry
data by provider, region, and service tier.

Selection considers total cost, including operations and migration, not only query price.
Tenant budgets and quotas are governed by ADR-033. Adapter-specific price changes do not
require feature-code changes.

During initial development, Qdrant runs locally/self-hosted to avoid a paid managed
vector-search subscription. Production planning must still price compute, storage, backup,
monitoring, support, and engineering operations.

## 12. Make provider switching an explicit rebuild migration

Vector-store switching is not an instant config flip for existing data:

1. Provision the target provider/placement.
2. Rebuild a target index from canonical sources and approved metadata.
3. Run parity, isolation, citation, performance, security, and cost validation.
4. Switch the active catalog/alias pointer for new queries.
5. Monitor during a rollback window.
6. Retire and securely delete the old index according to retention and contract rules.

Feature code remains unchanged. Migration status and failures are visible to authorized
administrators and operations staff.

---

# Candidate Assessment

| Candidate | Scale/filtering | Isolation/DR | Operations/cost | Portability and decision |
|---|---|---|---|---|
| pgvector | SQL filters; HNSW/IVFFlat; suitable for modest workloads | PostgreSQL database/schema/row controls and native backup ecosystem | Efficient when PostgreSQL already exists; adds another relational platform to this SQL Server architecture | Portable, but not selected as baseline due to stack mismatch |
| Qdrant | Purpose-built vector search, payload filtering, distributed options | Shard-key/collection tenant partition; snapshots and replication | Local/self-hosted avoids a managed-service subscription; production has infrastructure and operations cost | Selected first adapter |
| Pinecone | Managed scaling, namespaces, metadata filters | Namespace-based tenancy; recovery capabilities vary by plan/region | Low operations; consumption cost and service dependency | Viable managed adapter on customer demand |
| Weaviate | Hybrid/vector retrieval, filters, multi-tenancy | Tenant-aware collections; backup depends on deployment | Managed or self-hosted; moderate operations | Viable portable adapter on customer demand |
| Azure AI Search | Managed hybrid/vector retrieval and filtering | Dedicated tenant index; secondary/re-index recovery plan | Paid managed capacity; lower infrastructure operations; limits require placement control | Optional later adapter through `IVectorStore` |
| OpenSearch Vector Search | Distributed keyword/vector search and filters | Dedicated index/cluster; snapshot/restore | Managed or self-hosted; higher cluster tuning | Viable where customers already standardize on OpenSearch |

Commercial terms and provider capabilities change. They must be revalidated for the
selected region and tier before procurement or activation.

---

# Alternatives Considered

## Use the general search interface for vectors

Rejected. AI retrieval requires embedding lifecycle, chunk metadata, effective-date and
permission filters, citation identifiers, evaluation, and model-version compatibility that
should not expand or destabilize the general search contract.

## Use one shared vector index with `TenantId` filtering

Cheaper and operationally simple, but one missing/malformed filter can expose another
tenant's knowledge. Rejected as the sole isolation control.

## Use pgvector as the baseline

Would be attractive in a PostgreSQL platform, but this project standardizes on SQL Server.
Adding PostgreSQL only for vectors creates another database operational surface and weakens
the approved technology baseline. Rejected as the first adapter.

## Use Azure AI Search as the first adapter

Managed operations and Azure integration are attractive, but initial development would
introduce a paid managed dependency before it is needed. Rejected as the first adapter;
retained as an optional later plug-in.

## Use Pinecone or Weaviate as the first adapter

Both are viable, but neither aligns as directly with the approved Azure-default deployment.
Deferred to validated customer or regional requirements.

## Use OpenSearch for both global and vector search

Potentially useful for an OpenSearch-standardized customer, but it would change the current
default search stack and adds cluster operations. Deferred as an adapter option.

## Build all adapters immediately

Violates YAGNI and expands security, testing, support, and operations without validated
demand. Rejected; interfaces are designed now and adapters are built on demand.

---

# Consequences

## Positive

- No paid managed vector-search subscription is required for initial development.
- Qdrant-first deployment is portable across local, self-hosted, and customer-managed
  environments.
- Hard tenant isolation independent of feature-code filtering.
- Reproducible, versioned indexes with safe promotion and rollback.
- Vendor switching without changes to AI feature code.
- Clear separation between global application search and AI vector retrieval.
- Recovery does not depend on proprietary vector snapshots.

## Negative

- Self-hosted Qdrant requires patching, monitoring, backup, capacity, and incident ownership.
- Production Qdrant still incurs compute, storage, support, and engineering cost.
- Qdrant and Elasticsearch may coexist as separate operational services.
- Provider abstraction and normalized metadata require additional design and testing.
- Re-index migrations consume time, embeddings, network, and temporary duplicate capacity.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Qdrant operational failure or capacity exhaustion | Version-pinned deployment, health checks, snapshots, quotas, alerts, capacity tests |
| Cross-tenant retrieval | Dedicated/hard partition, trusted placement, post-retrieval checks, canary tests |
| Index/embedding incompatibility | Immutable version metadata; no mixed dimensions; shadow rebuild |
| Provider lock-in | `IVectorStore`, canonical source data, Azure/other adapter path, rebuild runbook |
| Stale or superseded policy | Effective-date/approval filters and event-driven invalidation/re-index |
| Restore returns unsafe data | Restore to new version and rerun isolation/authorization tests |
| Cost growth | Quotas, ledger, forecasts, adapter benchmarks, placement by service tier |
| Vendor score inconsistency | Adapter diagnostics plus evaluation; no universal score assumption |

---

# Acceptance Criteria Before Approval/Implementation

| ID | Criterion |
|---|---|
| VS-AC-001 | `IVectorStore` contract contains no vendor SDK or query-language types. |
| VS-AC-002 | Qdrant proof demonstrates server-resolved shard-key/dedicated-collection placement and fail-closed tenant resolution. |
| VS-AC-003 | Cross-tenant canary and deliberately malformed-filter tests return zero unauthorized chunks. |
| VS-AC-004 | RBAC/ABAC, sensitivity, effective-date, jurisdiction, locale, approval, and version filters are enforced and revalidated. |
| VS-AC-005 | Shadow index build, validation, promotion, rollback, and retirement complete without in-place mutation. |
| VS-AC-006 | Source deletion/offboarding removes eligible vectors, cache, and derived data under approved retention rules. |
| VS-AC-007 | Representative workload tests meet retrieval p95 <= 1.5 seconds without relaxing security controls. |
| VS-AC-008 | Restore or deterministic rebuild meets approved RPO/RTO and passes post-restore isolation tests. |
| VS-AC-009 | Provider/region/service prices and capacity limits are effective-dated configuration, not hardcoded. |
| VS-AC-010 | Qdrant-to-Azure AI Search migration rehearsal proves feature-code independence, controlled re-indexing, and documented rollback. |
| VS-AC-011 | Security review validates encryption, secrets, private connectivity/egress, audit, and data residency. |
| VS-AC-012 | Database, Technical Design, Security, Test, and OpenAPI documents reflect this decision before implementation. |

---

# Impact

## Architecture

Adds `VectorStore` to the provider framework, `IVectorStore`, a placement controller,
index lifecycle orchestration, and the Qdrant adapter. Azure AI Search remains an optional
later adapter through the same contract.

## Database

Requires tenant-scoped knowledge, chunk, placement, index-version, and ingestion metadata
in the future AI database design. Vector placement integrates with the provider catalog;
vectors remain external derived data.

## Security

Requires hard tenant partitions, post-retrieval authorization, tenant canaries, encryption,
secret isolation, private/controlled egress, and restore/migration security validation.

## Performance

Adds hybrid retrieval and optional reranking. Capacity is controlled through placement,
quotas, bulkheads, asynchronous ingestion, and representative benchmarks.

## Development

Feature code uses `IVectorStore` only. Adapter and architecture tests prevent SDK leakage.
No implementation starts until the required five-document set and OpenAPI are Approved.

---

# Official References

- pgvector: `https://github.com/pgvector/pgvector`
- Qdrant repository and license: `https://github.com/qdrant/qdrant`
- Qdrant local quickstart: `https://qdrant.tech/documentation/quickstart/`
- Qdrant multitenancy: `https://qdrant.tech/documentation/guides/multiple-partitions/`
- Pinecone multitenancy: `https://docs.pinecone.io/guides/index-data/implement-multitenancy`
- Weaviate multitenancy: `https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy`
- Azure AI Search vector overview:
  `https://learn.microsoft.com/en-us/azure/search/vector-search-overview`
- OpenSearch Vector Search: `https://docs.opensearch.org/latest/vector-search/`

References last validated: 2026-06-22.

---

# Approval

Solution Architect: Approved (Agent 6 / Codex)  
Security Architect: ____  
Database Architect: ____  
.NET Architect: ____  
Platform/Operations Architect: ____  
Product Owner: Bhajan Lal - Approved 2026-06-22

(Status: Approved)
