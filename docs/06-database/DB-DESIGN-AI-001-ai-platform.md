# Database Design - Governed AI Platform

Module: AI (`AI` schema)
Owner: Database Architect
Created Date: 2026-06-27
Version: 1.0
Status: Approved

> Doc 3 of 5 required before implementation. Companion docs:
> FEAT-AI-001, TECH-AI-001, UI-AI-001, TEST-AI-001.
> No AI implementation may start until all five documents are Approved.

---

# 1. Purpose

This document defines SQL Server database structures for the governed AI platform:
conversation governance, knowledge metadata, prompt/model/policy versions, evaluation,
cost governance, operational controls, disaster recovery evidence, and retention
reconciliation.

Vectors are not stored as raw vectors in SQL Server. SQL Server stores authoritative
metadata, governance state, audit references, and vector placement records. Vector content
is stored through the approved `IVectorStore` adapter, with Qdrant as the first
implementation.

---

# 2. Mandatory Table Rules

Every tenant-scoped table must include:

- `TenantId`
- `CreatedBy`
- `CreatedDate`
- `ModifiedBy`
- `ModifiedDate`
- `IsDeleted`
- `VersionNumber`

Every tenant-scoped table must have:

- SQL Server Row-Level Security predicate on `TenantId`.
- Index beginning with `TenantId`.
- Audit logging through the platform audit mechanism.
- Soft delete behavior unless a retention/deletion workflow authorizes physical purge.
- Data classification metadata where sensitive HR or AI content is stored.

No AI table may rely on the client request body for tenant identity.

---

# 3. Schemas

| Schema | Purpose |
|---|---|
| `AI` | AI platform metadata, conversations, knowledge, policies, evaluation, cost, operations. |
| `Audit` | Existing audit/change log and immutable security evidence. |
| `Eventing` | Existing outbox and event publication. |
| `Security` | Existing identity, RBAC, ABAC, role, and permission references. |
| `Tenant` | Existing tenant catalog and provider configuration references. |

---

# 4. Conversation and Memory Tables

## 4.1 `AI.Conversation`

Stores tenant-scoped conversation metadata.

Required columns:

- `ConversationId` uniqueidentifier PK
- `TenantId`
- `UserId`
- `Purpose`
- `UseCaseCode`
- `Locale`
- `Status`
- `MemoryMode`
- `LastMessageDate`
- `ResetCount`
- mandatory audit columns

Indexes:

- `(TenantId, UserId, LastMessageDate DESC)`
- `(TenantId, Purpose, Status)`

## 4.2 `AI.ConversationMessage`

Stores governed message metadata and sanitized message text where policy permits storage.

Required columns:

- `ConversationMessageId` uniqueidentifier PK
- `TenantId`
- `ConversationId`
- `Role`
- `ContentStorageMode`
- `SanitizedContent`
- `ContentHash`
- `ProviderRequestId`
- `AuditReferenceId`
- `TokenEstimate`
- mandatory audit columns

Rules:

- Raw provider payloads are not stored.
- Sensitive content storage requires policy approval and encryption.
- Message content must remain scoped to conversation purpose.

## 4.3 `AI.ConversationSummary`

Stores optional encrypted summaries.

Required columns:

- `ConversationSummaryId` uniqueidentifier PK
- `TenantId`
- `ConversationId`
- `SummaryTextEncrypted`
- `SummaryVersion`
- `SummarySourceTurnStart`
- `SummarySourceTurnEnd`
- `SummaryQualityScore`
- `Purpose`
- `ExpiresAt`
- `InvalidatedAt`
- `InvalidationReason`
- mandatory audit columns

Rules:

- Summary quality score is informational only.
- Summary cannot authorize access.
- Summary must be invalidated when role, purpose, legal hold, deletion, or source changes
  require reevaluation.

## 4.4 `AI.ConversationReset`

Stores reset events without deleting audit evidence.

Required columns:

- `ConversationResetId` uniqueidentifier PK
- `TenantId`
- `ConversationId`
- `ResetBy`
- `ResetReason`
- `ResetDate`
- `AuditReferenceId`

---

# 5. Knowledge and RAG Tables

## 5.1 `AI.KnowledgeSource`

Stores business source identity.

Required columns:

- `KnowledgeSourceId` uniqueidentifier PK
- `TenantId`
- `SourceCode`
- `Title`
- `SourceType`
- `OwnerRole`
- `Classification`
- `RetentionPolicyId`
- `DefaultLocale`
- `Status`
- mandatory audit columns

Indexes:

- unique `(TenantId, SourceCode)`
- `(TenantId, Status, Classification)`

## 5.2 `AI.KnowledgeSourceVersion`

Stores versioned source metadata.

Required columns:

- `KnowledgeSourceVersionId` uniqueidentifier PK
- `TenantId`
- `KnowledgeSourceId`
- `VersionNumber`
- `StorageReference`
- `FileHash`
- `EffectiveFrom`
- `EffectiveTo`
- `ValidationStatus`
- `PublicationStatus`
- `LegalHoldStatus`
- `PublishedAt`
- `PublishedBy`
- mandatory audit columns

Rules:

- Publication requires validation evidence and approval.
- Effective dating controls which policy version answers a date-sensitive question.

## 5.3 `AI.KnowledgeChunk`

Stores chunk metadata and citation anchors.

Required columns:

- `KnowledgeChunkId` uniqueidentifier PK
- `TenantId`
- `KnowledgeSourceVersionId`
- `ChunkSequence`
- `ChunkHash`
- `CitationLabel`
- `SectionPath`
- `PageNumber`
- `EffectiveFrom`
- `EffectiveTo`
- `SecurityScope`
- `VectorPlacementId`
- mandatory audit columns

Indexes:

- `(TenantId, KnowledgeSourceVersionId, ChunkSequence)`
- `(TenantId, SecurityScope)`

## 5.4 `AI.VectorPlacement`

Maps SQL metadata to vector store placement.

Required columns:

- `VectorPlacementId` uniqueidentifier PK
- `TenantId`
- `VectorStoreProviderCode`
- `CollectionName`
- `PartitionKey`
- `VectorNamespace`
- `EmbeddingModelCode`
- `EmbeddingModelVersion`
- `IndexVersionId`
- `PayloadSchemaVersion`
- mandatory audit columns

Rules:

- SQL Server stores placement metadata only.
- Vector store payload must include tenant and security filters.

## 5.5 `AI.VectorIndexVersion`

Tracks shadow and production index lifecycle.

Required columns:

- `VectorIndexVersionId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `IndexVersion`
- `IndexState`
- `ShadowNamespace`
- `ProductionNamespace`
- `PromotionApprovalReference`
- `RollbackIndexVersionId`
- `PublishedAt`
- mandatory audit columns

## 5.6 `AI.IngestionJob`

Tracks validation, chunking, embedding, indexing, publication, and rollback jobs.

Required columns:

- `IngestionJobId` uniqueidentifier PK
- `TenantId`
- `KnowledgeSourceVersionId`
- `JobType`
- `JobStatus`
- `StartedAt`
- `CompletedAt`
- `FailureCode`
- `FailureMessage`
- `EvidenceReference`
- mandatory audit columns

---

# 6. Prompt, Model, Provider, and Bundle Tables

## 6.1 `AI.PromptVersion`

Required columns:

- `PromptVersionId` uniqueidentifier PK
- `TenantId`
- `PromptCode`
- `VersionNumber`
- `Purpose`
- `Locale`
- `PromptTextEncrypted`
- `SafetyNotes`
- `EffectiveFrom`
- `EffectiveTo`
- `ApprovalStatus`
- mandatory audit columns

## 6.2 `AI.ModelRegistryVersion`

Required columns:

- `ModelRegistryVersionId` uniqueidentifier PK
- `ProviderCode`
- `ModelCode`
- `ModelVersion`
- `CapabilityType`
- `ContextWindowTokens`
- `SupportsStreaming`
- `SupportsJsonMode`
- `Status`
- `EffectiveFrom`
- `EffectiveTo`
- mandatory audit columns

Provider-wide rows may be global. Tenant-specific activation is stored separately.

## 6.3 `AI.ModelAssignment`

Required columns:

- `ModelAssignmentId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `ProviderCode`
- `ModelCode`
- `ModelRegistryVersionId`
- `Priority`
- `FallbackPolicy`
- `EffectiveFrom`
- `EffectiveTo`
- mandatory audit columns

## 6.4 `AI.AiBundle`

Stores deployable AI configuration bundle.

Required columns:

- `AiBundleId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `BundleVersion`
- `LifecycleStatus`
- `PromptVersionId`
- `ModelAssignmentId`
- `VectorIndexVersionId`
- `SafetyPolicyId`
- `MemoryPolicyId`
- `CachePolicyId`
- `EvaluationApprovalId`
- `RollbackBundleId`
- mandatory audit columns

---

# 7. Policy Tables

## 7.1 `AI.SafetyPolicy`

Required columns:

- `SafetyPolicyId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `PolicyVersion`
- `RiskTier`
- `AllowedToolsJson`
- `BlockedTopicsJson`
- `OutputRulesJson`
- `HumanReviewRequired`
- `EffectiveFrom`
- `EffectiveTo`
- mandatory audit columns

## 7.2 `AI.MemoryPolicy`

Required columns:

- `MemoryPolicyId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `MemoryMode`
- `SummaryRetentionDays`
- `PurposeBoundaryMode`
- `ResetAllowed`
- `EffectiveFrom`
- `EffectiveTo`
- mandatory audit columns

## 7.3 `AI.AiCachePolicy`

Required columns:

- `AiCachePolicyId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `PolicyVersion`
- `EligibilityMode`
- `TtlSeconds`
- `SimilarityThreshold`
- `PolicyReviewDate`
- `PolicyExpiryDate`
- `WarmUpPolicyVersion`
- `WarmUpSourceType`
- `WarmUpApprovalReference`
- `EffectiveFrom`
- `EffectiveTo`
- mandatory audit columns

---

# 8. Evaluation Tables

## 8.1 `AI.AiEvaluationDataset`

Required columns:

- `AiEvaluationDatasetId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `DatasetVersion`
- `DatasetReviewDate`
- `DatasetExpiryDate`
- `SealedHash`
- `Status`
- mandatory audit columns

## 8.2 `AI.AiEvaluationRun`

Required columns:

- `AiEvaluationRunId` uniqueidentifier PK
- `TenantId`
- `AiBundleId`
- `DatasetId`
- `RunStatus`
- `StartedAt`
- `CompletedAt`
- `EvidenceReference`
- mandatory audit columns

## 8.3 `AI.AiEvaluationMetric`

Required columns:

- `AiEvaluationMetricId` uniqueidentifier PK
- `TenantId`
- `AiEvaluationRunId`
- `MetricCode`
- `MetricValue`
- `MetricThreshold`
- `PassFail`
- `MetricEvidenceReference`
- mandatory audit columns

Required metric codes include hallucination rate, hallucination severity, groundedness,
citation precision, citation recall, refusal correctness, safety violations, latency, cost,
reviewer agreement, and reviewer consistency.

## 8.4 `AI.AiEvaluationApproval`

Required columns:

- `AiEvaluationApprovalId` uniqueidentifier PK
- `TenantId`
- `AiEvaluationRunId`
- `ApprovedBy`
- `ApprovalDate`
- `ApprovalExpiryDate`
- `ApprovalExpiryReason`
- `ApprovalStatus`
- `ApprovalEvidenceReference`
- mandatory audit columns

## 8.5 `AI.AiEvaluationDriftSignal`

Required columns:

- `AiEvaluationDriftSignalId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `SignalType`
- `SignalValue`
- `DetectedAt`
- `Severity`
- `ActionRequired`
- mandatory audit columns

`SignalType` must support `ProviderBehaviorDrift`.

---

# 9. Usage, Cost, and Rate-Limit Tables

## 9.1 `AI.AiUsageLedger`

Required columns:

- `AiUsageLedgerId` uniqueidentifier PK
- `TenantId`
- `UserId`
- `UseCaseCode`
- `ProviderCode`
- `ModelCode`
- `RequestType`
- `InputTokenEstimate`
- `OutputTokenEstimate`
- `ProviderCallCount`
- `AvoidedProviderCallCount`
- `CacheHit`
- `CostAmount`
- `CurrencyCode`
- `CorrelationId`
- `AuditReferenceId`
- mandatory audit columns

## 9.2 `AI.AiBudgetReservation`

Required columns:

- `AiBudgetReservationId` uniqueidentifier PK
- `TenantId`
- `UseCaseCode`
- `ReservedAmount`
- `CurrencyCode`
- `ReservationReason`
- `ReservationStatus`
- `ExpiresAt`
- `ReleasedAt`
- mandatory audit columns

## 9.3 `AI.AiRateLimitCounter`

Required columns:

- `AiRateLimitCounterId` uniqueidentifier PK
- `TenantId`
- `UserId`
- `UseCaseCode`
- `WindowStart`
- `WindowEnd`
- `LimitValue`
- `ConsumedValue`
- `ResetAt`
- mandatory audit columns

---

# 10. Operations, DR, and Retention Tables

## 10.1 `AI.AiOperationalDisablement`

Required columns:

- `AiOperationalDisablementId` uniqueidentifier PK
- `TenantId`
- `ScopeType`
- `ScopeReference`
- `ReasonCode`
- `Severity`
- `StartsAt`
- `ExpiresAt`
- `ApprovedBy`
- `ReleasedAt`
- `ReleaseEvidenceReference`
- mandatory audit columns

## 10.2 `AI.AiNamespaceRotation`

Required columns:

- `AiNamespaceRotationId` uniqueidentifier PK
- `TenantId`
- `NamespaceType`
- `OldNamespace`
- `NewNamespace`
- `NamespaceRotationReason`
- `NamespaceRotationApprovedBy`
- `NamespaceRotationEvidenceReference`
- `CompletedAt`
- mandatory audit columns

## 10.3 `AI.AiDrExercise`

Required columns:

- `AiDrExerciseId` uniqueidentifier PK
- `TenantId`
- `ExerciseType`
- `RecoveryScope`
- `StartedAt`
- `CompletedAt`
- `RpoResult`
- `RtoResult`
- `PassFail`
- `EvidenceReference`
- mandatory audit columns

## 10.4 `AI.AiRetentionReconciliationJob`

Required columns:

- `AiRetentionReconciliationJobId` uniqueidentifier PK
- `TenantId`
- `ScopeType`
- `JobStatus`
- `StartedAt`
- `CompletedAt`
- `DeletedItemCount`
- `HeldItemCount`
- `BlockedItemCount`
- `EvidenceReference`
- mandatory audit columns

---

# 11. RLS and Tenant Isolation

RLS predicate example:

```sql
CREATE SECURITY POLICY AI.AiTenantSecurityPolicy
ADD FILTER PREDICATE Security.fn_tenantPredicate(TenantId)
ON AI.Conversation;
```

The final implementation must use the approved platform RLS function from
`DB-DESIGN-001-foundations.md` and `DB-DESIGN-TENANT-001.md`.

Developer test data must prove that:

- Tenant A cannot read Tenant B AI metadata.
- Tenant A cannot retrieve Tenant B vectors through SQL placement records.
- Restored deleted content remains unavailable until reconciliation completes.
- Legal hold blocks deletion but also prevents unsafe AI use when policy requires it.

---

# 12. Indexing Strategy

Minimum indexes:

- `AI.Conversation`: `(TenantId, UserId, LastMessageDate DESC)`
- `AI.ConversationSummary`: `(TenantId, ConversationId, ExpiresAt)`
- `AI.KnowledgeSource`: unique `(TenantId, SourceCode)`
- `AI.KnowledgeSourceVersion`: `(TenantId, KnowledgeSourceId, VersionNumber)`
- `AI.KnowledgeChunk`: `(TenantId, KnowledgeSourceVersionId, ChunkSequence)`
- `AI.VectorPlacement`: `(TenantId, VectorStoreProviderCode, VectorNamespace)`
- `AI.VectorIndexVersion`: `(TenantId, UseCaseCode, IndexState)`
- `AI.AiBundle`: `(TenantId, UseCaseCode, LifecycleStatus)`
- `AI.AiEvaluationRun`: `(TenantId, AiBundleId, RunStatus)`
- `AI.AiUsageLedger`: `(TenantId, UseCaseCode, CreatedDate)`
- `AI.AiOperationalDisablement`: `(TenantId, ScopeType, ScopeReference, ExpiresAt)`

High-growth ledger, message, metric, and job tables must be partition-ready by date and
tenant.

---

# 13. Data Retention

Retention follows ADR-022 and ADR-032:

- Session memory is short-lived.
- Conversation summaries use governed retention such as 30, 60, or 90 days where approved.
- Knowledge source retention follows source retention policy and legal hold.
- Evaluation evidence is retained according to governance/audit policy.
- Usage ledger is retained according to finance/audit policy.
- Deleted or expired content must be excluded from AI retrieval, cache, memory, and
  generated answers.

---

# 14. Migration Sequence

1. Create `AI` schema.
2. Create conversation and memory metadata tables.
3. Create knowledge metadata and vector placement tables.
4. Create prompt/model/provider/bundle tables.
5. Create safety, memory, and cache policy tables.
6. Create evaluation tables.
7. Create cost/rate-limit tables.
8. Create operations, DR, retention, and namespace rotation tables.
9. Apply RLS policies and tenant indexes.
10. Add outbox event integration.
11. Add seed data only for platform defaults, not tenant business rules.

---

# 15. Acceptance Criteria

| ID | Criterion |
|---|---|
| DB-AI-AC-001 | Every tenant-scoped AI table contains mandatory tenant, audit, soft-delete, and concurrency columns. |
| DB-AI-AC-002 | SQL Server RLS blocks cross-tenant AI metadata access. |
| DB-AI-AC-003 | SQL stores vector placement metadata but not raw vector payloads. |
| DB-AI-AC-004 | Knowledge versions, chunks, vector index versions, and publication states are auditable and reversible. |
| DB-AI-AC-005 | Prompt, model, safety, memory, cache, and bundle behavior is versioned and effective-dated. |
| DB-AI-AC-006 | Evaluation metrics include hallucination, citation, reviewer, and provider behavior drift evidence. |
| DB-AI-AC-007 | Usage, budget, and rate-limit tables support per-tenant governance and reporting. |
| DB-AI-AC-008 | Operational disablement, namespace rotation, DR exercise, and retention reconciliation evidence is persisted. |
| DB-AI-AC-009 | Deleted, expired, held, or unreconciled restored content cannot be selected for AI use. |
| DB-AI-AC-010 | All AI database changes are migration-controlled and reviewed before implementation. |

---

# 16. Official and Primary References

- SQL Server Row-Level Security:
  `https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security`
- Qdrant multitenancy documentation:
  `https://qdrant.tech/documentation/manage-data/multitenancy/`
- Qdrant snapshots:
  `https://qdrant.tech/documentation/concepts/snapshots/`
- Redis Cluster documentation:
  `https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/`
- NIST AI Risk Management Framework:
  `https://www.nist.gov/itl/ai-risk-management-framework`

References last validated: 2026-06-27.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-27  
Database Architect: Approved as part of owner-approved AI implementation package 2026-06-27  
Solution Architect: Approved as part of owner-approved AI implementation package 2026-06-27  
Security Architect: Approved as part of owner-approved AI implementation package 2026-06-27  
Data Governance/Privacy: Approved as part of owner-approved AI implementation package 2026-06-27  
Platform/Operations Architect: Approved as part of owner-approved AI implementation package 2026-06-27

(Status: Approved - owner approved 2026-06-27)
