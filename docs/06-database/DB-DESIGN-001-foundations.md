# Database Design — Platform Foundations (Phase 7A)

Document Owner: Database Architect (Agent 7)
Created Date: 2026-06-14
Version: 1.2
Status: Approved (Bhajan Lal, 2026-06-18)
Owner Amendment: 2026-06-22 - VectorStore provider type added for Qdrant-first AI architecture

> Scope: the foundational SQL Server schema for Phase 7A — tenant catalog, security/identity,
> effective-dated core HR, workflow, rules, event/outbox, provider configuration, and audit. Module schemas (leave, attendance,
> payroll) get their own DB design docs. Follows `DATABASE_STANDARDS.md`, ADR-003 (SQL
> Server), ADR-005 (multi-tenancy + RLS), ADR-006 (tenant context), ADR-007
> (effective-dating), ADR-008 (identity), ADR-009 (events/outbox), ADR-010 (workflow),
> ADR-011 (rules), and ADR-027 (provider abstraction).

---

# Purpose

Provide a secure, multi-tenant, auditable, time-aware foundation that every module builds
on, designed so tenants can later move to a dedicated DB/region via the catalog without
code change.

---

# Conventions (from DATABASE_STANDARDS)

- **PascalCase** tables/columns; PK = `TableNameId`; FK = `ReferencedTableId`.
- **Mandatory columns on every business table:** `TenantId`, `CreatedBy`, `CreatedDate`,
  `ModifiedBy`, `ModifiedDate`, `IsDeleted`, `VersionNumber`.
- **Soft delete** (`IsDeleted`), never physical delete of business data.
- **Mandatory index on `TenantId`**; PK/FK indexed; parameterized queries only.
- **EF Core migrations only.** No manual prod schema changes.
- **RLS** (ADR-005) on every tenant-scoped table as defense-in-depth.

> The **catalog** database is the only thing NOT tenant-scoped (it *defines* tenants).

---

# Schemas

`catalog` (control-plane) · `security` · `core` (employee/org) · `workflow` · `rules` ·
`events` · `audit`. Module schemas (`leave`, `attendance`, `payroll`, ...) added later.

---

# 1. `catalog` schema (control plane — single regional control DB)

```
catalog.Tenant
  TenantId (PK, uniqueidentifier), Code (unique), Name, Status(Active/Suspended/Offboarding),
  Region, ShardKey, PlacementType(Pooled/Dedicated), Tier, CreatedDate, ...
catalog.TenantShard
  ShardId (PK), Region, ConnectionRef(secret reference, NOT a raw connection string),
  Capacity, TenantCount
catalog.TenantBranding         -- white-label (FR-010)
  TenantId (FK), LogoUrl, ThemeJson, CustomDomain, EmailFromDomain, DkimVerified
catalog.TenantFeatureFlag      -- per-tenant module/feature enablement + entitlement
  TenantId (FK), FeatureKey, Enabled, EntitlementJson
catalog.TenantConfigVersion    -- sandbox→prod config promotion (ARCH-REVIEW §1B)
  TenantId (FK), Environment(Sandbox/Prod), Version, SnapshotRef, PromotedBy, PromotedDate
catalog.ProviderType           -- Registry-driven categories: Storage, Cache, Messaging,
                                  Email, SMS, Push, Identity, Search, Reporting, LLM,
                                  VectorStore; new categories require data/config, not schema change
  ProviderTypeId (PK), [Key], Description
catalog.Provider               -- available adapter registry
  ProviderId (PK), ProviderTypeId (FK), [Key], DisplayName, CapabilitiesJson, Status
catalog.TenantProviderConfig   -- per-tenant provider selection (ADR-027)
  TenantProviderConfigId (PK), TenantId (FK), ProviderTypeId (FK), ProviderId (FK),
  ConfigJson, SecretRef, IsPrimary, FallbackProviderId, Enabled, EffectiveFrom, + audit
catalog.ProviderHealth         -- per-tenant/provider health view
  ProviderHealthId (PK), TenantId (FK), ProviderTypeId (FK), ProviderId (FK),
  Status, LatencyMs, LastCheckedAt, LastError
```
Connection strings live in **Key Vault**, referenced by `ConnectionRef` (never stored raw).

---

# 2. `security` schema

```
security.UserAccount
  UserAccountId (PK), TenantId, Email, AuthProvider(Local/EntraID/Google/Okta),
  ExternalSubjectId, Status, MfaEnabled, + audit cols
security.Role
  RoleId (PK), TenantId, Name, IsSystem, + audit
security.Permission            -- catalog of fine-grained permissions
  PermissionId (PK), Key, Description
security.RolePermission        (TenantId, RoleId, PermissionId)
security.UserRole              (TenantId, UserAccountId, RoleId)
security.AbacPolicy            -- attribute rules (department/location/BU scoping)
  AbacPolicyId (PK), TenantId, Name, RuleRef(→ rules engine), Effect(Allow/Deny)
security.Delegation            -- delegation/proxy approvals (ARCH-REVIEW §5)
  DelegationId (PK), TenantId, FromUserId, ToUserId, ScopeJson, ValidFrom, ValidTo, Active
security.RefreshToken / security.Session
  ...token lifecycle, forced logout, concurrent-session limits
```

---

# 3. `core` schema — effective-dated (ADR-007)

Master/assignment entities are **effective-dated** (valid time) and use SQL Server
**temporal tables** for system-time history.

```
core.Employee                  -- identity-level, slow-changing
  EmployeeId (PK), TenantId, EmployeeNumber, UserAccountId (FK), Status, + audit
  (SYSTEM_VERSIONING = ON → core.EmployeeHistory)
core.EmployeeDetail            -- EFFECTIVE-DATED attributes (name, contact, designation)
  EmployeeDetailId (PK), TenantId, EmployeeId (FK),
  EffectiveFrom (date), EffectiveTo (date NULL=open),
  FirstName, LastName, Email, Phone, DesignationId, ... , + audit
  -- "current" = row where today ∈ [EffectiveFrom, EffectiveTo)
core.LegalEntity               -- multi-legal-entity reserved now (UI deferred)
  LegalEntityId (PK), TenantId, Name, CountryCode, RegistrationNo
core.OrgUnit                   -- department/location/business-unit tree
  OrgUnitId (PK), TenantId, ParentOrgUnitId, Type, Name, LegalEntityId
core.Position                  -- position mgmt (vacant positions) reserved
  PositionId (PK), TenantId, Title, OrgUnitId, IsVacant
core.EmployeeAssignment        -- EFFECTIVE-DATED: which position/org/manager/grade
  EmployeeAssignmentId (PK), TenantId, EmployeeId, PositionId, OrgUnitId,
  ManagerEmployeeId, GradeId, EffectiveFrom, EffectiveTo, + audit
```

**As-of query pattern** (repository default = today):
```sql
SELECT * FROM core.EmployeeDetail
WHERE TenantId = @tenantId AND EmployeeId = @id
  AND @asOf >= EffectiveFrom AND (@asOf < EffectiveTo OR EffectiveTo IS NULL)
  AND IsDeleted = 0;
```

---

# 4. `workflow` schema (ADR-010)

```
workflow.Definition   (DefinitionId, TenantId, [Key], Version, Status, JsonSpec,
                       PublishedBy, PublishedDate, + audit)  UNIQUE(TenantId,[Key],Version)
workflow.Instance     (InstanceId, TenantId, DefinitionId, DefinitionVersion, BusinessKey,
                       CurrentState, Status, ContextJson, + audit)
workflow.InstanceToken(TokenId, TenantId, InstanceId, State, Status) -- parallel branches
workflow.Task         (TaskId, TenantId, InstanceId, State, AssigneeType, AssigneeId,
                       OnBehalfOfId, DueAt, Status, DecidedBy, DecidedAt, Comment)
workflow.EventLog     (EventId, TenantId, InstanceId, Type, FromState, ToState, ActorId,
                       OnBehalfOfId, PayloadJson, CreatedAt)         -- APPEND-ONLY
workflow.Timer        (TimerId, TenantId, InstanceId, FireAt, Type, Fired)
workflow.Template     (TemplateId, TenantId, [Key], Version, JsonSpec, MetadataJson)
```
`EventLog` and `Instance` **partitioned by month**; index `(TenantId, InstanceId)`.

---

# 5. `rules` schema (ADR-011)

```
rules.RuleSet  (RuleSetId, TenantId, [Key], Version, Status, EffectiveFrom, EffectiveTo,
                + audit)  UNIQUE(TenantId,[Key],Version)        -- immutable on publish
rules.Rule     (RuleId, RuleSetId, [Key], Priority, WhenJson(AST), ThenJson, Description)
rules.DecisionTable (DecisionTableId, RuleSetId, [Key], InputSchemaJson, RowsJson)  -- payroll/tax slabs
rules.RuleAudit (RuleAuditId, TenantId, RuleSetId, Action, Diff, ActorId, CreatedAt)
```
Statutory change ⇒ **new effective-dated RuleSet version**, never edit a published one.

---

# 6. `events` schema (ADR-009 — Event Bus + Outbox)

The event schema defines the default outbox/inbox pattern. A large module may own its
own outbox table, but it must keep this shape so the dispatcher, monitoring, and replay
tools stay generic.

```
events.Outbox
  OutboxId (PK, bigint), TenantId, ModuleKey, AggregateType, AggregateId,
  EventType, EventVersion, PayloadJson, IdempotencyKey, Status(Pending/Published/Failed),
  Attempts, OccurredAt, PublishedAt(NULL), LastError, + audit
events.Inbox
  InboxId (PK, bigint), TenantId, MessageId, ConsumerKey, ProcessedAt, Status, Error
events.EventContract
  EventContractId (PK), EventType, EventVersion, SchemaJson, Status, EffectiveFrom
```

Outbox writes happen in the same database transaction as the business change. Consumers
dedupe through `(TenantId, MessageId, ConsumerKey)`. Payloads carry no unnecessary PII.

---

# 7. `audit` schema (FR-008 — Time Machine)

```
audit.ChangeLog   -- generic field-level audit across modules (APPEND-ONLY / WORM)
  ChangeLogId (PK, bigint), TenantId, EntityType, EntityId, Action(Create/Update/Delete),
  FieldName, OldValue, NewValue, Reason, ActorId, OnBehalfOfId, CreatedAt
audit.AccessLog   -- login/logout/impersonation/permission-denied
  AccessLogId (PK), TenantId, UserAccountId, Event, Ip, CorrelationId, CreatedAt
```
Append-only; consider hash-chaining for tamper-evidence; partition by month; archive per
retention policy (ADR-022).

---

# Relationships (key cardinalities)

- Tenant 1—* UserAccount, Employee, Definition, RuleSet, Outbox, TenantProviderConfig
  (everything tenant-scoped unless explicitly catalog control-plane reference data).
- Employee 1—* EmployeeDetail / EmployeeAssignment (effective-dated versions).
- WorkflowDefinition 1—* Instance; Instance 1—* Task / EventLog / Timer.
- RuleSet 1—* Rule / DecisionTable.

# Indexes

- Mandatory `TenantId` index on every tenant-scoped table.
- Effective-dated: `(TenantId, EmployeeId, EffectiveFrom, EffectiveTo)`.
- Workflow: `(TenantId, Status)` on Task/Instance; `FireAt` on Timer.
- Audit/EventLog: `(TenantId, EntityType, EntityId)` / `(TenantId, InstanceId)`;
  time-partitioned.
- Events: `(TenantId, Status, OccurredAt)` on Outbox and unique
  `(TenantId, MessageId, ConsumerKey)` on Inbox.
- Provider config: `(TenantId, ProviderTypeId)` and `(TenantId, ProviderId)`.

# Tenant Strategy

All tenant-data and tenant-config tables carry `TenantId` + **RLS predicate** filtering
on the session's tenant context (ADR-005/006). `catalog` control-plane reference tables
define tenants, shards, and provider registries; `catalog.TenantProviderConfig` and other
tenant-specific catalog tables carry `TenantId`.

# Growth & Archival

- High-growth tables: `workflow.EventLog`, `events.Outbox`, `events.Inbox`,
  `audit.ChangeLog`, `audit.AccessLog`,
  attendance (later). Monthly partitioning + archival tier; retention per ADR-022.
- Estimate (per 1,000-employee tenant): audit/event rows in the millions/year → partition
  from day one.

---

## Approval

Database Architect: Approved · Solution Architect: Approved · Security Architect: Approved ·
Product Owner: Approved (Bhajan Lal, 2026-06-18)
