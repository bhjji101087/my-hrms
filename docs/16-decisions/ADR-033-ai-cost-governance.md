# ADR-033 - AI Cost Governance

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
- ADR-008 Identity and Access Management - Approved
- ADR-009 Event-Driven Backbone - Approved
- ADR-019 Enterprise AI/RAG Platform Architecture - Approved
- ADR-027 Provider-Abstraction Framework - Approved
- ADR-030 Enterprise Vector Store Strategy - Approved
- ADR-031 AI Observability and Telemetry - Approved
- ADR-032 Conversation Memory Strategy - Approved

---

# Context

AI cost is created by more than a model request. It may include input, output, and cached
tokens; embeddings; reranking; vector storage and search; cache and database storage;
telemetry; network transfer; and allocated platform infrastructure. Cost also varies by
provider, model, region, agreement, currency, billing mode, and effective date.

Without platform-controlled cost governance, the HRMS could:

- Enable a paid provider or feature without an explicit owner decision.
- Allow concurrent requests to exceed a tenant budget.
- Calculate cost using stale or hardcoded provider prices.
- Allow a time-bound trial or AI feature to continue as paid usage after expiry.
- Produce invoices or internal chargeback from unverified estimates.
- Expose one tenant's usage or commercial terms to another tenant.
- Reduce model quality or safety silently to save cost.
- Block essential security, audit, deletion, or cost-administration operations when an AI
  budget is exhausted.
- Use an emergency override as a permanent bypass of financial or security controls.
- Depend on a provider billing dashboard and lose provider independence.

Initial development must avoid unnecessary paid services. Self-hosted Qdrant and the
self-hosted observability stack remain the first adapters under ADR-030 and ADR-031.
However, self-hosted infrastructure is not assumed to be free in production: compute,
storage, backups, support, operations, and energy still require attribution.

The platform therefore needs a provider-independent cost-control layer that supports
zero-spend development, tenant budgets, accurate showback, future chargeback, forecasting,
and safe enforcement without changing AI feature code.

---

# Decision

## 1. Use a platform-owned AI cost-governance service

All AI use cases pass through a provider-independent cost-governance service before and
after execution. Feature modules do not call provider billing APIs or implement their own
budget logic.

The service owns:

- Effective-dated price resolution.
- Usage estimation and atomic budget reservation.
- Final usage recording and reservation settlement.
- Provider-bill reconciliation.
- Budget, quota, threshold, and entitlement enforcement.
- Cost allocation, showback, forecasting, and alerts.
- Auditable administrative changes.

Provider adapters expose normalized usage through contracts such as
`IAiUsageMeterAdapter` and `IAiProviderBillingAdapter`. Model, vector, cache, and other AI
adapters remain replaceable through the provider-abstraction framework in ADR-027.

No feature-code change is permitted when a supported provider, model, price version,
currency, or billing mode is added.

## 2. Require explicit activation before any paid provider use

Paid AI capability is disabled by default for a new environment and tenant. It can run
only when all of the following are active and effective:

1. The platform provider adapter is approved and enabled for the environment.
2. The tenant is entitled to the AI use case.
3. An authorized administrator explicitly enables the provider/model assignment.
4. A valid credential reference exists in the approved secret store.
5. A budget and hard-limit policy cover the intended scope.
6. Security, evaluation, data-residency, and provider-processing policies permit the call.
7. Any time-bound trial or feature entitlement has not expired.

There is no automatic upgrade from a local or self-hosted component to a paid managed
service. Trial expiry, capacity pressure, provider recommendation, model fallback, or
missing configuration cannot activate paid usage.

Development and test environments may use a zero monetary budget, local/test adapters,
provider sandboxes, or explicitly capped paid accounts. Mock usage still exercises the
same reservation, ledger, threshold, and denial paths.

### 2.1 Govern time-bound AI entitlements and trial expiry

An AI entitlement may define `TrialExpiryDate` and `FeatureExpiryDate`. These dates are
independent: a promotional trial may end before the tenant's separately contracted feature
entitlement, and a feature entitlement may exist without a trial.

- Entitlement evaluation uses trusted platform time and effective-dated policy.
- Configurable warning notifications are issued before an upcoming expiry.
- At expiry, new ineligible requests are denied and in-flight behavior follows an approved,
  bounded completion policy.
- An expired trial cannot silently convert to `PlatformBilled`, another paid model/provider,
  or a tenant-direct credential.
- Renewal creates a new effective-dated entitlement version; it does not edit prior history.
- Expiry, renewal, suspension, and reactivation require authorization and immutable audit.
- Expiration never bypasses budget, quota, provider assignment, security, evaluation,
  residency, or tenant-isolation controls.

The entitlement service publishes warnings and expiry events but cannot automatically buy,
renew, extend, or activate a paid service. Administrative screens must show trial and
feature expiry separately from budget reset dates.

## 3. Maintain an immutable, tenant-isolated usage and cost ledger

SQL Server is the durable system of record. Operational telemetry is not the billing or
showback ledger.

Required conceptual entities:

```text
AI.AiUsageLedger
  AiUsageLedgerId, TenantId, UsageDate, BillingPeriod,
  EnvironmentKey, UseCaseKey, ProviderKey, ModelKey, RegionKey,
  BillingMode, ProviderRequestId, IdempotencyKey,
  InputTokens, OutputTokens, CachedInputTokens, EmbeddingUnits,
  RerankUnits, VectorQueryUnits, VectorStorageUnits,
  OtherUsageJson, PriceVersionId, CurrencyCode,
  EstimatedCost, ActualCost, CostStatus, AllocationStatus,
  CorrelationId, CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiBudget
  AiBudgetId, TenantId, BudgetScopeType, BudgetScopeKey,
  EnvironmentKey, BillingPeriodType, CurrencyCode,
  MonetaryLimit, RequestLimit, TokenLimit, ConcurrencyLimit,
  SoftThresholdPolicyJson, HardLimitAction, EssentialUsePolicyJson,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiBudgetReservation
  AiBudgetReservationId, TenantId, AiBudgetId, IdempotencyKey,
  CorrelationId, ReservationReason, EstimatedMaximumCost, ReservedUsageJson,
  Status, ExpiresDate, SettledDate, ActualCost,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCostAllocation
  AiCostAllocationId, TenantId, AiUsageLedgerId,
  CostCenterKey, ProjectKey, DepartmentKey, AllocationRuleVersion,
  AllocationPercentage, AllocatedCost, CurrencyCode,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCostReconciliation
  AiCostReconciliationId, TenantId, ProviderKey, BillingPeriod,
  ProviderStatementReference, EstimatedCost, ProviderReportedCost,
  VarianceAmount, VarianceReason, Status, ReconciledBy, ReconciledDate,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCostAlert
  AiCostAlertId, TenantId, AiBudgetId, AlertType,
  ThresholdValue, ObservedValue, ForecastValue, Status,
  RaisedDate, AcknowledgedDate, ResolvedDate,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiFeatureEntitlement
  AiFeatureEntitlementId, TenantId, FeatureKey, UseCaseKey,
  EntitlementType, TrialExpiryDate, FeatureExpiryDate,
  ProviderAssignmentVersion, BudgetPolicyVersion,
  EffectiveFrom, EffectiveTo, Status, RenewalReference,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCostForecast
  AiCostForecastId, TenantId, BudgetScopeType, BudgetScopeKey,
  ForecastAmount, CurrencyCode, ForecastHorizon, AsOfDate,
  ForecastConfidenceScore, ForecastMethodVersion,
  ConfidenceEvaluationVersion, ExclusionsJson, UnpricedUsageJson,
  ProjectedBreachDate, EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiBudgetUtilizationSnapshot
  AiBudgetUtilizationSnapshotId, TenantId, AiBudgetId,
  BillingPeriod, UsageThroughDate, ConsumedAmount, ReservedAmount,
  RemainingAmount, CurrencyCode, SourceLedgerWatermark,
  RefreshStatus, RefreshRunId, EffectiveFrom, EffectiveTo,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.TenantAiCommercialTerm
  TenantAiCommercialTermId, TenantId, ProviderKey, ServiceType,
  ModelKey, RegionKey, ContractReference, PricingRuleType,
  PricingRuleJson, CurrencyCode, GlobalPriceVersionReference,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiCostEmergencyOverride
  AiCostEmergencyOverrideId, TenantId, OverrideScopeType, OverrideScopeKey,
  IncidentReference, OverrideReason, RequestedBy, ApprovedBy,
  EffectiveFrom, EffectiveTo, Status, RevokedBy, RevokedDate,
  PostEventReviewStatus, PostEventReviewReference,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

catalog.AiProviderPrice
  AiProviderPriceId, ProviderKey, ServiceType, ModelKey, RegionKey,
  UsageUnit, PricePerUnit, CurrencyCode, PriceSourceReference,
  PriceSourceVersion, EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

catalog.ExchangeRate
  ExchangeRateId, SourceCurrencyCode, TargetCurrencyCode,
  Rate, SourceProviderKey, SourceReference, SourceVersion,
  EffectiveFrom, EffectiveTo, Status, ValidatedBy, ValidatedDate,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber
```

Every tenant table includes `TenantId`, SQL Server RLS, mandatory tenant-filtered queries,
audit/version columns, and indexes beginning with `TenantId`. The global price catalog is
a restricted control-plane table and cannot contain tenant credentials or expose one
tenant's negotiated terms to another.

Usage ledger records are append-only for financial traceability. Corrections create
adjustment records that reference the original entry; they do not overwrite recorded
usage. `IsDeleted` supports governance workflow but does not authorize erasure of required
financial or audit history.

`ReservationReason` is selected from an approved business-use-case/reason catalog or an
approved incident/recovery reason. It is required, auditable, included in authorized budget
and reconciliation reporting, and cannot contain prompts, employee data, secrets, or
uncontrolled free text. APIs may accept a reason key plus a bounded supporting reference;
the server validates both against the current entitlement and use case.

Prompts, responses, retrieved chunks, conversation summaries, employee identifiers, and
hidden reasoning are prohibited from the cost ledger.

## 4. Normalize all measurable AI usage

The ledger records provider-neutral quantities where they are available:

- Input, output, and cached-input tokens.
- Model requests, tool calls, and batch operations.
- Embedding inputs and generated vector count.
- Reranking documents or provider-specific rerank units.
- Vector queries, indexed vectors, and storage duration/size.
- Cache, database, object-storage, telemetry, and network allocation units.
- Self-hosted compute and storage allocation units.

Every entry is classified by tenant, environment, use case, provider, model/service,
region, billing period, and billing mode. Optional cost-center, project, department, and
business-module dimensions support showback when authorized.

Provider-specific units are retained in `OtherUsageJson` using a versioned schema and are
mapped into normalized units when possible. Unknown units are visible as unpriced usage;
they are never silently valued at zero.

## 5. Use effective-dated, auditable price catalogs

Provider prices are configuration data, never constants in feature code. Each price row
defines provider, service/model, region, currency, unit, source, version, and non-overlapping
effective dates.

The price used for a request is resolved at the request's usage time and recorded by
`PriceVersionId`, so historical cost remains reproducible after prices change. Authorized
discounts, enterprise agreements, credits, taxes, minimum commitments, and currency
conversion are represented by separate versioned commercial rules rather than altering
the public list price.

Price changes require `AI.ManagePriceCatalog`, a source reference, reason, effective date,
four-eyes approval for production, and audit. Past effective prices cannot be edited;
corrections create a new version or reconciliation adjustment.

The platform may import prices through an approved adapter, but automatic imports cannot
activate a provider or change tenant budgets. Stale, missing, overlapping, or ambiguous
prices make paid execution ineligible unless an approved conservative fallback price
policy exists.

### 5.1 Preserve a global catalog while allowing future tenant commercial terms

The global price catalog remains immutable shared reference history. Future tenant-specific
negotiated prices, enterprise discounts, commitments, and contract terms are stored as
separate `AI.TenantAiCommercialTerm` versions layered over a referenced global price
version. A tenant term never edits, deletes, or backdates global catalog history.

The pricing resolver applies an explicit, versioned precedence rule and records both the
global price version and tenant commercial-term version used. Terms are tenant-scoped with
RLS, separately encrypted where required, and accessible only to authorized commercial or
finance roles. Aggregated reports cannot reveal another tenant's agreement. New pricing
rule types are introduced through provider-independent strategy/configuration contracts,
not provider logic in AI feature modules.

## 6. Reserve budget atomically before execution

For a metered request, the orchestrator performs this sequence:

1. Resolve tenant, entitlement, use case, provider/model assignment, and current policy.
2. Estimate the maximum permitted usage and cost for the request.
3. Atomically check applicable budgets and reserve the estimate.
4. Execute the approved provider operation.
5. Record normalized actual usage and the provider request reference.
6. Settle the reservation using actual or best-known cost and release the difference.
7. Reconcile later when authoritative provider billing data becomes available.

The reservation is concurrency-safe and idempotent by trusted tenant scope plus
`IdempotencyKey`. A provider request ID is unique within its provider/tenant scope. Retries
cannot create a second charge, and parallel requests cannot spend the same available
budget.

The reservation records `ReservationReason`, the resolved AI use case, and authorized
supporting reference. These values flow to settlement, reconciliation, audit, budget-review,
and authorized consumption-pattern reports without exposing prompt or employee content.

Reservations have a configured expiry and reconciliation workflow for timeouts or unknown
provider outcomes. An expired reservation is not simply discarded when the provider may
have completed the request; it moves to investigation or delayed reconciliation.

## 7. Support hierarchical, effective-dated budgets and quotas

Governance may define limits at these scopes:

- Platform and environment.
- Tenant.
- Use case or business module.
- Provider or model/service.
- Cost center, project, or department where authorized.
- Daily, monthly, or contract billing period.

Controls may include monetary budget, requests, tokens/usage units, storage, concurrency,
and rate limits. More-specific policy can be stricter but cannot bypass platform security,
provider, compliance, or environment limits.

Soft thresholds and hard limits are effective-dated configuration. Threshold percentages,
notification recipients, grace behavior, and actions are not hardcoded. Budget changes
require `AI.ManageBudgets`, a reason, an effective date, and audit; production increases
above platform-defined risk limits require separate approval.

Currency mismatches are normalized using an approved effective-dated exchange-rate source
or are rejected. A budget cannot compare unconverted values from different currencies.

### 7.1 Govern exchange rates through a dedicated architectural decision

`ADR-036 Financial Exchange-Rate Governance` is reserved as the governing future decision
for shared platform currency conversion. Until ADR-036 and its companion designs are
Approved, cross-currency AI budget comparison, chargeback, and reconciliation cannot enter
implementation; same-currency governance may proceed.

Exchange-rate management follows the same principles as provider pricing:

- Approved source/provider, source reference, currency pair, version, and non-overlapping
  effective dates.
- Restricted permission, segregation of duties, validation, reason, and immutable audit.
- Reproducible historical conversion by recording the exact exchange-rate version used.
- Configurable freshness and variance validation against approved reference sources.
- No feature-code constants, silently inferred rates, or reuse beyond the valid period.

If a required rate is missing, stale, invalid, overlapping, or unavailable, the platform
does not assume parity or use the latest value indefinitely. A cross-currency paid request
fails closed unless a separately approved conservative fallback policy is effective; the
condition raises an alert and cannot activate or extend an emergency override by itself.

## 8. Apply safe threshold and hard-limit behavior

At a soft threshold, the platform may:

- Notify authorized tenant and platform administrators.
- Display current usage, remaining amount, and forecast.
- Reduce optional batch work or reschedule non-urgent operations.
- Route to an approved lower-cost model only when its security, quality, data-processing,
  and evaluation gates are already satisfied.

At a hard limit, the platform rejects or pauses non-essential AI requests with a clear,
non-sensitive error and next-reset/effective-policy information. It does not silently incur
additional paid usage or silently switch provider/model.

Budget exhaustion must not block:

- Core non-AI HRMS functionality.
- Authentication, authorization, security response, and tenant isolation.
- Audit capture and mandatory event delivery.
- Privacy/deletion, legal-hold, and tenant-offboarding controls.
- Viewing cost/usage and requesting an authorized budget change.
- Administrative disabling of AI capability or provider credentials.

An essential AI exception is permitted only when explicitly classified, budgeted, approved,
time-bound, and audited. The model cannot classify its own request as essential.

### 8.1 Permit only controlled emergency administrative overrides

An emergency override exists for exceptional business-continuity, cost-governance outage,
provider-billing incident, or recovery operations. It is not a normal budget increase or a
way to continue an expired trial.

Every override must:

1. Be requested by an explicitly authorized platform role with an incident reference and
   documented reason.
2. Receive approval from a different authorized person under four-eyes control, except a
   separately approved break-glass process that requires immediate retrospective approval.
3. Define the exact tenant/environment/use-case/provider scope, maximum monetary or usage
   exposure, and short `EffectiveFrom`/`EffectiveTo` period.
4. Generate immutable audit, security, cost, and alert records on request, activation, use,
   expiry, revocation, and review.
5. Expire automatically and require a new approval for any extension.
6. Trigger post-event review, reconciliation, and credential/access review.

An override may relax only the specifically approved cost-availability control. It cannot
bypass tenant isolation, authentication, RBAC/ABAC, data residency, model/provider approval,
privacy, legal hold, audit, entitlement expiry, prohibited use cases, or financial ledger
recording. It cannot alter price history, erase charges, or become permanent configuration.
The platform must always permit immediate revocation.

## 9. Distinguish platform-billed and tenant-direct billing

Supported billing modes are configuration values, initially:

- `PlatformBilled` - the platform account is charged and provider billing is reconciled to
  the HRMS ledger.
- `TenantDirect` - the tenant supplies an approved credential/account and pays the provider
  directly; HRMS records estimated usage and showback but does not claim it as an invoice.
- `SelfHostedAllocated` - infrastructure cost is allocated from approved compute, storage,
  backup, support, and operations rates.
- `NoChargeTest` - test/mock usage with no external financial charge; still governed by
  quotas and ledger paths.

Credentials are referenced by secret ID only and never stored in the ledger. Tenant-direct
billing does not bypass provider approval, data residency, security, quotas, or platform
capacity controls.

## 10. Forecast cost and projected budget breaches

The service produces tenant- and platform-authorized forecasts using current committed
usage, run rate, billing-period progress, known scheduled workloads, and sufficient
historical patterns. Forecast output includes:

- Forecast amount and currency.
- Forecast horizon and as-of time.
- Method/version and confidence band.
- `ForecastConfidenceScore`, its defined scale, and confidence-evaluation version.
- Known exclusions and unpriced usage.
- Projected threshold or hard-limit breach date.

Forecasts are decision support, not guaranteed invoices. Low-data and unusual-usage
conditions are clearly marked. A forecast cannot increase a budget or authorize provider
use automatically.

`ForecastConfidenceScore` quantifies reliability only. It is versioned, auditable, and
stored separately from `ForecastAmount`; changing the confidence method cannot alter the
forecast value or historical budget consumption. The score considers data sufficiency,
volatility, missing/unpriced usage, method validation, and forecast horizon. It cannot grant
authorization, suppress a hard limit, or make an estimate customer-billable.

## 11. Use showback first; introduce chargeback only after reconciliation approval

Initial reporting is showback: tenants and platform operators can see authorized usage,
estimated costs, budgets, forecasts, forecast-confidence scores, entitlement/trial expiry,
and authorized reservation-reason summaries. The platform does not generate customer
invoices from estimated token calculations.

Chargeback requires a separate approved commercial policy and must use reconciled cost,
contract/tax/currency rules, dispute handling, immutable invoice lineage, finance approval,
and legal/compliance review. Ledger estimates remain distinct from provider-reported actual
cost and customer-billable amounts.

### 11.1 Use optional rebuildable budget-utilization snapshots

`AI.AiBudgetUtilizationSnapshot` may accelerate dashboards and reporting when ledger volume
makes direct aggregation impractical. It is a derived read model, never the source of truth
for authorization, reservation, settlement, reconciliation, or financial history.

- Each snapshot records its source-ledger watermark, refresh run, usage-through time, and
  effective period.
- Refresh and rebuild are idempotent, auditable, tenant-isolated, and monitored.
- A snapshot can be deleted and fully rebuilt from the immutable ledger and reservations.
- Corruption, staleness, or refresh failure cannot change ledger history or remaining-budget
  enforcement; dashboards fall back to authoritative queries or show data as unavailable.
- Snapshot data uses the same RLS, permission, retention, currency, and commercial-term
  protections as the source records.

## 12. Enforce cost permissions, segregation, and tenant privacy

Initial permissions:

| Permission | Scope |
|---|---|
| `AI.ViewUsage` | View authorized tenant usage quantities |
| `AI.ViewCosts` | View authorized tenant estimated/actual cost and forecast |
| `AI.ManageBudgets` | Create future-effective tenant budget/policy versions |
| `AI.ManageEntitlements` | Create future-effective trial/feature entitlement versions |
| `AI.EmergencyCostOverride` | Request/approve/revoke a scoped time-bound emergency override; platform restricted |
| `AI.ViewAllCosts` | Restricted platform cross-tenant financial view |
| `AI.ManagePriceCatalog` | Restricted platform price and commercial-rule management |
| `AI.ManageTenantCommercialTerms` | Restricted tenant commercial-term version management |
| `AI.ManageExchangeRates` | Restricted platform exchange-rate version management under ADR-036 |
| `AI.ReconcileCosts` | Restricted finance/operations reconciliation workflow |

Every operation uses RBAC plus ABAC, tenant isolation, purpose checks, and audit. Tenant
administrators can see only their tenant's permitted data. Cross-tenant aggregation is
restricted to approved platform roles and does not expose tenant-level details unless the
role has a separately audited operational need.

Commercial terms, discounts, credentials, and provider statements are more restricted than
ordinary usage summaries. Support impersonation or delegation cannot grant financial
permissions implicitly.

`AI.EmergencyCostOverride` is never granted to a tenant role, model, provider adapter, or
ordinary support role. Request and approval must be performed by different platform
principals unless the approved break-glass policy is invoked, and every use is alerted and
included in post-event access review.

## 13. Publish cost events without financial or HR data leakage

ADR-009 events include:

- `AiUsageRecorded`
- `AiBudgetThresholdCrossed`
- `AiBudgetExceeded`
- `AiBudgetChanged`
- `AiPriceCatalogChanged`
- `AiCostReconciled`
- `AiCostForecastBreachProjected`
- `AiFeatureEntitlementExpiring`
- `AiFeatureEntitlementExpired`
- `AiFeatureEntitlementRenewed`
- `AiEmergencyCostOverrideActivated`
- `AiEmergencyCostOverrideExpired`
- `AiEmergencyCostOverrideRevoked`
- `AiEmergencyCostOverrideReviewed`
- `AiTenantCommercialTermChanged`
- `AiExchangeRateChanged`
- `AiBudgetUtilizationSnapshotRefreshed`

Events contain trusted identifiers, scope/version, status, severity, and correlation data.
They do not contain prompts, responses, employee data, credentials, provider statements,
or negotiated commercial terms. Consumers are idempotent and use the transactional outbox.

## 14. Define versioned API requirements

The Phase 6D OpenAPI package must include:

| Endpoint | Permission | Behavior |
|---|---|---|
| `GET /api/v1/ai/admin/usage` | `AI.ViewUsage` | Filtered tenant usage with governed dimensions and pagination |
| `GET /api/v1/ai/admin/costs` | `AI.ViewCosts` | Estimated, reconciled, and unpriced cost clearly separated |
| `GET /api/v1/ai/admin/cost-forecast` | `AI.ViewCosts` | Forecast value, separate versioned confidence score, exclusions, and projected breach |
| `GET /api/v1/ai/admin/budgets` | `AI.ViewCosts` | Current and future-effective authorized budget policies |
| `PUT /api/v1/ai/admin/budgets/{budgetId}` | `AI.ManageBudgets` | Create an immutable future-effective budget version |
| `GET /api/v1/ai/admin/entitlements` | `AI.ViewCosts` | Current/future trial and feature expiry with warning state |
| `PUT /api/v1/ai/admin/entitlements/{entitlementId}` | `AI.ManageEntitlements` | Create an audited future-effective entitlement/renewal version |
| `POST /api/v1/platform/ai/emergency-overrides` | `AI.EmergencyCostOverride` | Request scoped, capped, time-bound override with reason and incident reference |
| `POST /api/v1/platform/ai/emergency-overrides/{id}/approve` | `AI.EmergencyCostOverride` | Four-eyes approval and activation |
| `POST /api/v1/platform/ai/emergency-overrides/{id}/revoke` | `AI.EmergencyCostOverride` | Immediately revoke and trigger review/reconciliation |
| `GET /api/v1/platform/ai/prices` | `AI.ManagePriceCatalog` | Restricted price catalog and validation state |
| `PUT /api/v1/platform/ai/prices/{priceId}` | `AI.ManagePriceCatalog` | Create a reviewed effective-dated price version |
| `PUT /api/v1/platform/ai/commercial-terms/{termId}` | `AI.ManageTenantCommercialTerms` | Create tenant-isolated negotiated-term version without changing global prices |
| `PUT /api/v1/platform/exchange-rates/{rateId}` | `AI.ManageExchangeRates` | Create validated effective-dated rate version under ADR-036 |
| `POST /api/v1/platform/ai/reconciliations` | `AI.ReconcileCosts` | Import/reference and reconcile provider billing data |

All endpoints use `/api/v1`, JWT, server-resolved tenant context, RBAC plus ABAC,
correlation IDs, standard envelopes, pagination/filter limits, rate limits, and audit.
Mutations require `Idempotency-Key` and optimistic concurrency. OpenAPI documentation,
contract tests, examples, permissions, errors, and rate-limit behavior are mandatory before
implementation.

Exports are asynchronous, access-controlled, size-limited, encrypted, time-bound, audited,
and subject to retention. They cannot expose another tenant or raw provider credentials.
Reservation APIs and internal contracts require the governed `ReservationReason` key;
forecast responses expose `ForecastConfidenceScore`, scale, method version, and confidence
evaluation version separately from the forecast amount.

## 15. Keep observability separate from financial records

ADR-031 telemetry monitors budget-service latency, reservation failures, ledger lag,
reconciliation variance bands, stale price catalogs, projected breaches, denied-request
rates, and provider-usage reporting failures.

Tenant IDs, user IDs, prompts, responses, commercial terms, and high-cardinality billing
dimensions are not exported as unrestricted telemetry labels. Tenant and financial drilldown
uses the authorized SQL ledger and application APIs.

Alerting covers:

- Missing, stale, overlapping, or unpriced price records.
- Budget reservation/settlement failures and stuck reservations.
- Ledger/outbox backlog and duplicate provider-request detection.
- Unexpected usage spikes or cost anomalies.
- Reconciliation variance above configured policy.
- Forecasted and actual threshold breaches.
- Low or degrading forecast-confidence scores and evaluation-version changes.
- Trial/feature expiry warnings, renewal failures, and post-expiry denied requests.
- Emergency override activation, usage, nearing expiry, revocation, and overdue review.
- Snapshot refresh lag, watermark mismatch, corruption, rebuild, and fallback usage.
- Stale/missing exchange rates and invalid/overlapping tenant commercial terms.

## 16. Fail closed against uncontrolled spend

- If tenant or authorization context is unavailable, the request fails closed.
- If the cost-governance service or durable reservation path is unavailable, paid
  non-essential AI execution fails closed.
- An explicitly approved local/no-charge adapter may continue only when policy permits and
  its quota enforcement remains available.
- Missing or invalid price data cannot be treated as zero cost.
- Missing, stale, or invalid required exchange rates cannot be treated as currency parity.
- An expired trial or feature entitlement cannot continue, convert, renew, or switch to paid
  usage automatically.
- A ledger write failure after provider execution enters durable recovery/reconciliation;
  it cannot be hidden by a successful user response.
- A provider timeout with unknown outcome retains/resolves the reservation conservatively.
- Budget denial cannot fall back to an unapproved provider, model, region, or credential.
- Snapshot failure cannot change enforcement; the ledger/reservation path remains
  authoritative or the request fails according to its normal governance policy.
- An emergency override is rejected when scope, cap, approval, audit, or expiry validation
  is unavailable and can never serve as a tenant/security/compliance bypass.
- Core HRMS functionality remains available without paid AI.

Runbooks must cover stuck reservations, unknown provider outcomes, price errors, usage
spikes, reconciliation variance, budget breach, credential compromise, and provider-billing
API outage, entitlement expiry, emergency override/revocation, snapshot recovery, stale
exchange rates, and commercial-term resolution failure.

## 17. Apply retention, audit, and privacy controls

Usage, budget, price, reconciliation, and financial-audit retention is defined by ADR-022
and applicable finance/compliance policy before implementation. Retention values are
effective-dated configuration within platform-governed limits.

Cost records contain only the minimum identifiers needed for authorization, allocation,
reconciliation, dispute handling, and audit. Business-purpose use of employee-level AI
cost is prohibited unless separately documented and approved. Cost governance cannot be
used for hidden employee productivity scoring or employment decisions.

Deletion requests remove eligible operational data while preserving records that must be
retained for legal, financial, security, or audit obligations. Legal hold is separately
authorized and does not make held data available to AI processing.

## 18. Deliver cost governance in controlled increments

Implementation documentation must preserve this order:

1. Usage normalization, price catalog, ledger, and tenant isolation.
2. Atomic reservation with reason, budgets/quotas, entitlement expiry, denial behavior,
   emergency override controls, and audit.
3. Tenant showback, alerts, forecast confidence, and optional utilization snapshots.
4. Provider billing reconciliation and self-hosted allocation.
5. Tenant-specific commercial terms and cross-currency conversion only after their
   respective approved governance designs.
6. Chargeback only after separate commercial, finance, legal, and compliance approval.

No later increment may bypass the controls and tests required by an earlier increment.
No code starts until the constitutional Business, Technical, Database, UI, and Test
documents plus the OpenAPI and security requirements are Approved.

---

# Alternatives Considered

## Use provider billing dashboards only

Simple for one provider, but does not provide request-time enforcement, normalized
multi-provider usage, tenant isolation, self-hosted allocation, or provider independence.
Rejected.

## Estimate cost only from observability metrics

Useful for operations, but metrics may be sampled, delayed, aggregated, high-cardinality,
or retained differently from financial records. Rejected as the system of record.

## Hardcode provider prices and thresholds

Fast initially, but prices, agreements, models, currencies, and tenant policies change.
It violates configuration-as-data and open-for-extension requirements. Rejected.

## Record cost only after requests complete

Simpler, but concurrent requests can overspend a budget before the ledger is updated.
Rejected in favor of atomic reservation and settlement.

## Allow unlimited use during initial development

Avoids early governance work but creates uncontrolled spend and makes enforcement expensive
to retrofit. Rejected. Zero-cost/test adapters still pass through governance controls.

## Adopt a paid FinOps product first

May accelerate mature reporting, but adds initial cost and vendor dependency. Rejected as
the required first implementation. Future tools may integrate through export/adapter
contracts without replacing the platform ledger or enforcement layer.

## Treat self-hosted AI infrastructure as free

Misstates total cost and prevents fair capacity planning. Rejected. Development may use a
zero external-charge policy while production tracks allocated infrastructure cost.

---

# Consequences

## Positive

- No paid AI provider is activated without explicit approval and budget.
- Tenants receive isolated usage, budget, forecast, and showback information.
- Atomic reservations prevent common concurrent-overspend scenarios.
- Historical cost remains reproducible through effective-dated prices.
- Provider/model switching does not change feature code or financial controls.
- Core HRMS and mandatory security/privacy operations remain available at budget limits.
- Local/self-hosted development and future managed providers follow the same governance.
- The architecture supports future chargeback without treating estimates as invoices.

## Negative

- Request preflight and reservation add latency and implementation complexity.
- Provider usage units and billing statements vary and require adapters/reconciliation.
- Forecasts and allocated self-hosted costs are estimates with documented uncertainty.
- Finance, operations, product, security, and tenant administrators share governance work.
- Conservative failure behavior may temporarily deny non-essential AI requests.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Concurrent requests exceed budget | Atomic reservation, scoped locking/transaction, idempotency |
| Duplicate charge on retry | Tenant-scoped idempotency and unique provider request reference |
| Stale or incorrect price | Effective-dated catalog, source/version, validation, reconciliation |
| Estimate differs from provider bill | Separate estimated/actual status and adjustment-based reconciliation |
| Cross-tenant financial disclosure | RLS, trusted tenant context, RBAC/ABAC, negative tests, restricted exports |
| Cost saving reduces answer safety/quality | Only pre-approved evaluated routes; no silent model/provider switch |
| Ledger outage creates uncontrolled spend | Paid non-essential execution fails closed; durable recovery/outbox |
| Self-hosted cost appears free | Allocated infrastructure cost and explicit `SelfHostedAllocated` mode |
| Tenant-direct key bypasses policy | Central gateway, provider approval, quota and security enforcement |
| Budget limit blocks mandatory controls | Explicit protected operations outside non-essential AI denial |
| Cost data becomes employee surveillance | Data minimization and prohibition on hidden productivity/employment use |
| Forecast is treated as invoice | Confidence/exclusion labeling; showback and chargeback remain separate |
| Expired trial silently becomes paid | Independent trial/feature expiry, automatic denial, warnings, no automatic conversion |
| Emergency override becomes permanent bypass | Platform-only four-eyes approval, cap, short expiry, immutable audit, alert, post-review |
| Low-confidence forecast drives budget decision | Separate versioned confidence score, method lineage, visible exclusions; no authorization effect |
| Snapshot corrupts budget history | Derived rebuildable read model; ledger/reservations remain authoritative |
| Negotiated price leaks across tenants | Tenant RLS, restricted commercial permission, encryption, no cross-tenant detail |
| Stale exchange rate produces wrong cost | ADR-036 governance, effective-dated validated source, alert and fail-closed conversion |

---

# Acceptance Criteria Before Approval/Implementation

| ID | Criterion |
|---|---|
| CG-AC-001 | Paid AI is disabled by default and cannot activate without approved provider, entitlement, credential reference, assignment, security/evaluation policy, and budget. |
| CG-AC-002 | Local, self-hosted, tenant-direct, and platform-billed usage use the same normalized governance contracts without feature-code changes. |
| CG-AC-003 | Every tenant ledger, budget, reservation, allocation, alert, and reconciliation operation derives `TenantId` from trusted context and passes RLS plus RBAC/ABAC. |
| CG-AC-004 | Cross-tenant, guessed-ID, delegated, export, and platform-admin negative tests disclose no unauthorized usage, cost, budget, or commercial term. |
| CG-AC-005 | Price catalogs are effective-dated, source/versioned, non-overlapping, auditable, and reproduce the historical price used by every costed ledger entry. |
| CG-AC-006 | Missing, stale, ambiguous, or unpriced paid usage cannot be silently valued at zero or executed outside approved conservative policy. |
| CG-AC-007 | Concurrent reservation tests prove parallel requests cannot spend the same available budget. |
| CG-AC-008 | Retry, timeout, replay, and duplicate-provider-response tests create one settled usage charge per provider operation. |
| CG-AC-009 | Reservation expiry and unknown provider outcome have durable investigation/reconciliation behavior without silent release or double charge. |
| CG-AC-010 | Soft thresholds notify and may use only pre-approved lower-cost routes; hard limits reject non-essential AI without silent paid overrun. |
| CG-AC-011 | Budget exhaustion does not block core HRMS, security, audit, deletion/legal hold, tenant offboarding, cost viewing, or AI disablement. |
| CG-AC-012 | Budget, threshold, quota, currency, allocation, and essential-use rules are effective-dated configuration rather than feature-code constants. |
| CG-AC-013 | Forecasts include as-of time, method/version, confidence, exclusions, unpriced usage, and projected breach; they cannot alter budgets automatically. |
| CG-AC-014 | Estimated, provider-reported, reconciled, allocated, credited, and customer-billable amounts remain distinct and auditable. |
| CG-AC-015 | Chargeback is disabled until separate commercial/finance/legal/compliance documentation and reconciled-cost controls are Approved. |
| CG-AC-016 | Cost ledger, API, telemetry, events, and exports contain no prompts, responses, retrieved chunks, hidden reasoning, credentials, or unnecessary employee data. |
| CG-AC-017 | Provider/model/price/currency/billing-mode additions use adapters/configuration and require no change to AI feature code. |
| CG-AC-018 | Paid non-essential AI fails closed when reservation or durable cost enforcement is unavailable and never falls back to an unapproved provider. |
| CG-AC-019 | Cost events use the outbox, are idempotent, and expose no sensitive HR content or negotiated commercial terms. |
| CG-AC-020 | All cost APIs are versioned, OpenAPI-documented, audited, tenant-isolated, rate-limited, and contract-tested before implementation. |
| CG-AC-021 | Provider statement and self-hosted allocation reconciliation produce adjustment lineage rather than rewriting usage history. |
| CG-AC-022 | Unit coverage is at least 85%, with integration, isolation, security, concurrency, recovery, reconciliation, API, and end-to-end budget tests. |
| CG-AC-023 | Every reservation records a validated `ReservationReason` and authorized supporting reference that flow through settlement, audit, reconciliation, API, and reporting without sensitive content. |
| CG-AC-024 | Forecast responses and records expose `ForecastConfidenceScore`, scale, method/version, evaluation version, and audit lineage separately from forecast value. |
| CG-AC-025 | Trial and feature entitlements have independent effective-dated expiry; warnings occur before expiry and expired access cannot silently convert, renew, switch, or incur paid usage. |
| CG-AC-026 | Entitlement expiry/renewal APIs, events, notifications, authorization, immutable audit, and in-flight-request behavior pass integration and end-to-end tests. |
| CG-AC-027 | Emergency overrides require platform-only permission, documented incident/reason, scoped cap, time limit, separate approval or approved break-glass process, immutable audit, alert, immediate revocation, and post-event review. |
| CG-AC-028 | Emergency override tests prove no bypass of tenant isolation, security, compliance, entitlement expiry, provider/model approval, data residency, audit, or ledger recording. |
| CG-AC-029 | Budget-utilization snapshots are tenant-isolated, derived, watermarked, auditable, rebuildable, and unable to alter ledger history or authoritative enforcement. |
| CG-AC-030 | Tenant-specific commercial terms are effective-dated, reference global price history, preserve provider independence, and cannot disclose or modify another tenant's terms or global catalog. |
| CG-AC-031 | Cross-currency implementation remains gated by Approved ADR-036; each conversion records a validated effective-dated rate version and fails closed on missing/stale/invalid data unless an approved fallback exists. |

---

# Impact

## Architecture

Adds a centralized AI cost-governance service, normalized usage contracts, price resolver,
atomic reservation/settlement flow, forecast and threshold engine, reconciliation adapters,
and authorized showback APIs. AI feature modules remain unaware of provider billing details.

## Database

Requires tenant-scoped usage, budget, reservation, allocation, reconciliation, and alert
tables plus entitlement, forecast, optional utilization snapshot, tenant commercial-term,
emergency-override, restricted global price-catalog, and exchange-rate entities. Detailed
DB design must define keys, constraints, RLS predicates, partitioning/retention, decimal
precision, currency handling, indexes, concurrency, effective dates, snapshot watermarks,
immutable override records, and adjustment lineage. The ledger remains authoritative over
all snapshots.

## Security

Adds financial permissions, segregation of duties, explicit paid-provider activation,
tenant-isolation tests, restricted commercial data, audited budget/price changes, and
fail-closed spend controls. It also adds entitlement expiry enforcement, platform-only
four-eyes emergency overrides, immutable override audit, tenant-isolated negotiated terms,
and restricted exchange-rate administration. Secrets remain in the approved secret store.

## Performance

Every metered request adds a policy lookup and atomic reservation. Cached read models may
improve performance, but authoritative remaining budget is decided transactionally. Async
ledger enrichment, forecasting, snapshot refresh, and reconciliation cannot weaken
request-time enforcement. Utilization snapshots reduce reporting aggregation cost but must
fall back safely when stale or unavailable.

## Development

Requires Business, Technical, Database, UI, Test, Security, and OpenAPI documentation before
code. Adapters must normalize usage and provider billing without leaking provider-specific
logic into AI features.

## Operations and Finance

Operations owns service health, reservation recovery, price freshness, alerts, capacity,
entitlement-expiry jobs, snapshot refresh/rebuild, exchange-rate freshness, emergency
override monitoring/revocation, post-event review tracking, and runbooks. Finance owns
provider-statement reconciliation, tenant commercial rules, exchange-rate governance with
the future ADR-036 owner, and any future chargeback approval. Product Owner owns use-case
value, priority, entitlement, and budget policy. Security reviews override access and every
break-glass use.

---

# Official References

- FinOps Framework - Budgeting:
  `https://www.finops.org/framework/capabilities/budgeting/`
- FinOps Framework - Forecasting:
  `https://www.finops.org/framework/capabilities/forecasting/`
- Anthropic API pricing documentation:
  `https://docs.anthropic.com/en/docs/about-claude/pricing`

Provider pricing links are references to mutable source catalogs; this ADR intentionally
does not hardcode current prices.

References last validated: 2026-06-25.

---

# Approval

Solution Architect: Approved (Codex)  
Platform/Operations Architect: Architecture controls incorporated  
Security Architect: Security controls incorporated  
Database Architect: Database controls incorporated  
Finance Reviewer: Financial-governance controls incorporated  
Product Owner: Bhajan Lal - Approved 2026-06-25

(Status: Approved)
