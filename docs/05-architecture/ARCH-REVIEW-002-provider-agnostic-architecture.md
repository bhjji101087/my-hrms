# Architecture Review — Provider-Agnostic / Vendor-Independence

Document Owner: Solution Architect (Agent 6), with SaaS / Integration / Security hats
Created Date: 2026-06-15
Version: 1.0
Status: Approved (Bhajan Lal, 2026-06-18)

> Evaluates long-term extensibility and vendor independence: tenants choosing their own
> **storage, cache, messaging, notification, identity, search, and BI** providers via
> **configuration only** — no app code change, no deployment, no developer. Generalizes the
> LLM multi-provider decision (ADR-019) into a **universal provider framework**. Umbrella
> decision = ADR-027.

---

## 1. Verdict & Guiding Stance

**Yes — design the seams now, build adapters on demand.** The right architecture is a
**thin abstraction + adapter + per-tenant registry + resolver** for every external
dependency. Doing this *interface-first* is cheap and is the single biggest hedge against
lock-in. **But:** implementing *every* adapter (S3 + GCS + on-prem + NAS + Kafka + …) is
**not part of Phase 7A** — that's YAGNI. Phase 7A ships **Azure-default adapters behind the interfaces**;
additional adapters are added when a customer actually requires one. The cost of skipping
the *abstraction* now is a painful rewrite later; the cost of building *all adapters* now is
wasted effort.

> Honesty on "runtime switching": **new operations** switch by config. **Existing state**
> often needs a migration/transition (storage = data copy/dual-read; messaging = drain
> in-flight; search = reindex; identity = re-auth sessions). Cache switching is safe
> (cold start). We must not market "instant switch" without these caveats.

---

## 2. The Universal Provider Pattern

```
 Domain / Application code  ──► depends only on ►──  Provider INTERFACE (e.g. IFileStorageProvider)
                                                          ▲
                                   IProviderResolver<T> selects the adapter per request:
                                   (tenantId) → TenantProviderConfig → Adapter + secrets(KeyVault)
                                                          ▲                    + health + fallback
        ┌──────────────┬──────────────┬─────────────────┴───────────────┐
   AzureBlobAdapter   S3Adapter    GcsAdapter   OnPremSmbAdapter   NasAdapter   …
```

Five building blocks (identical for every category):
1. **Interface** — a *thin, lowest-common-denominator* contract (no vendor SDK types leak out).
2. **Adapters** — one per provider, implementing the interface.
3. **Registry** — catalog of available adapters (`ProviderKey` → adapter type + capabilities).
4. **Per-tenant config** — which provider + settings + secret reference + fallback, per tenant.
5. **Resolver/Factory** — resolves the adapter for the current tenant at runtime, with
   health-check + fallback + caching.

**Capability flags** handle provider-specific extras (e.g. S3 pre-signed URLs vs SMB paths)
without polluting the core interface — code checks `provider.Supports(Capability.SignedUrl)`.

---

## 3. Per-Category Recommendations

| Category | Interface (sketch) | Phase 7A default | Adapters (on demand) | Lock-in notes |
|---|---|---|---|---|
| **Storage** | `IFileStorageProvider` (Save/Get/Delete/Exists/GetSignedUrl/Stream) | Azure Blob | AWS S3, GCS, Azure File, **SMB/network share**, customer VM FS, NAS/SAN | URL signing & ACL models differ → capability flags; on-prem needs secure connectivity |
| **Cache** | `ICacheProvider` (Get/Set/Remove/GetOrAdd, TTL) | Redis / Azure Cache for Redis | NCache, In-Memory, other distributed | **Tenant-namespaced keys mandatory** (`{tenantId}:{key}`) regardless of provider |
| **Messaging** | `IMessageBus` (Publish/Subscribe) + **outbox** (ADR-009) | Azure Service Bus / RabbitMQ | AWS SQS, **Kafka**, ActiveMQ | Ordering/semantics differ; outbox stays provider-independent; switching needs drain |
| **Email** | `IEmailSender` | SMTP / SendGrid | Microsoft Graph, Amazon SES | Templating stays ours; provider sends only |
| **SMS** | `ISmsSender` | MSG91 (India) / Twilio | Gupshup, Textlocal | DLT/sender-ID (India) per provider config |
| **Push** | `IPushSender` | Firebase | Azure Notification Hub | Token formats differ |
| **Identity** | `IIdentityProvider` / OIDC validation (ADR-008) | Entra ID / Google / Okta | Auth0, Ping Identity | Stick to **OIDC/OAuth2 + SCIM** standards; avoid proprietary flows |
| **Search** | `ISearchProvider` (Index/Search/Delete, per-tenant index) | Elasticsearch | Azure AI Search, OpenSearch | Query DSL differs → use a neutral query model + capability flags |
| **Reporting/BI** | `IReportingProvider` / `IEmbeddedAnalyticsProvider` | SSRS / embedded | Power BI, embedded vendors | Embedding + row-level security model differs per vendor |

Notification email/SMS/push unify under an `INotificationChannel` abstraction + a channel
router (already surfaced as Notification preferences in the UI).

---

## 4. Configuration Model

- **Resolution order:** Tenant config → tenant tier default → platform default.
- **Per-tenant, per-category:** `{ providerKey, configJson, secretRef, isPrimary,
  fallbackProviderKey, enabled, effectiveFrom }`. Secrets are **Key Vault references**,
  never raw values in DB or app config (extends ADR-005 catalog rule).
- **Feature-flag gated**; changes are **admin-only** (`Providers.Manage`), audited, and
  validated (test-connection) before activation — surfaced in the **Integration Hub** UI.
- **Sandbox→prod** promotion for provider config (reuses ARCH-REVIEW-001 §1B).

---

## 5. Required Database Entities (`catalog` schema)

```
catalog.ProviderType          -- reference: Storage, Cache, Messaging, Email, Sms, Push,
                                 Identity, Search, Reporting
  ProviderTypeId(PK), [Key], Description
catalog.Provider              -- registry of available adapters per type + capabilities
  ProviderId(PK), ProviderTypeId(FK), [Key](e.g. "AzureBlob","S3","Kafka"),
  DisplayName, CapabilitiesJson, Status(GA/Beta/Deprecated)
catalog.TenantProviderConfig  -- per-tenant selection (the heart)
  TenantProviderConfigId(PK), TenantId, ProviderTypeId, ProviderId,
  ConfigJson, SecretRef(KeyVault), IsPrimary(bit), FallbackProviderId(NULL),
  Enabled(bit), EffectiveFrom, + audit
catalog.ProviderHealth        -- monitoring/failover
  ProviderHealthId(PK), TenantId, ProviderTypeId, ProviderId,
  Status(Healthy/Degraded/Down), LatencyMs, LastCheckedAt, LastError
```
Indexed on `(TenantId, ProviderTypeId)`; config changes audited (admin-only).

---

## 6. Required Abstraction Layers

- `IProviderResolver<TProvider>` + `IProviderFactory` (generic: resolve per tenant + health + fallback).
- `IFileStorageProvider`, `ICacheProvider`, `IMessageBus`, `IEmailSender`/`ISmsSender`/`IPushSender`
  (`INotificationChannel`), `IIdentityProvider`, `ISearchProvider`, `IReportingProvider`.
- `ISecretResolver` (Key Vault), `IProviderHealthCheck`, `ICapabilityProbe`.
- Rule: **domain/application code references only these interfaces** — vendor SDKs live in
  adapter projects, never in core. (Enforce with architecture tests.)

---

## 7. Design Requirements — Assessment

| # | Requirement | Supported by | 
|---|---|---|
| 1 | Provider abstraction via interfaces/adapters | §2, §6 — yes |
| 2 | Config-driven selection | §4 — yes |
| 3 | Tenant-specific provider config | §5 `TenantProviderConfig` — yes |
| 4 | Runtime switching w/o deploy | Yes for **new ops**; existing state needs migration (§1 caveat) |
| 5 | Secrets in Key Vault | §4 `SecretRef` — yes (mandatory) |
| 6 | Per-tenant provider config | §5 — yes |
| 7 | Provider health monitoring | §5 `ProviderHealth` + `IProviderHealthCheck` — yes |
| 8 | Failover/fallback | `FallbackProviderId` + resolver — yes (idempotent ops only) |
| 9 | Multi-provider coexistence | Resolver picks per tenant per request → Tenant A (RabbitMQ/Redis/Blob) and Tenant B (Service Bus/NCache/on-prem) run **simultaneously** — yes |

---

## 8. Security Implications

- **Secrets:** per-tenant credentials in Key Vault; least-privilege; rotation; never logged.
- **Tenant isolation across providers:** storage paths/buckets, cache key namespaces, and
  search indices are **per-tenant** regardless of provider; cross-tenant must be impossible
  even when tenants share a provider.
- **Customer-managed providers** (on-prem file server, customer S3): a new **trust boundary**
  — require private connectivity (VPNet/Private Link/agent), SSRF egress allow-listing,
  and clear data-processing responsibility. The platform must fail safe if the customer
  endpoint is unreachable.
- **Config validation:** test-connection + schema-validate before activation; config changes
  are admin-only and audited (old→new).
- **Failover data-residency:** fallback must not move data across a forbidden region.

---

## 9. Scalability Implications

- **Connection/client pooling per (tenant, provider)**; bound the number of live clients
  (10k tenants × N providers) — lazy-init + LRU eviction of idle clients.
- **Resolver caching** (per-tenant config cached in Redis, short TTL, invalidated on change)
  to avoid a catalog hit per request.
- **Health-check overhead** — async, sampled, circuit-breaker; don't check on hot path.
- **Noisy-provider isolation** — a slow/down provider for one tenant must not exhaust shared
  threads (bulkheads/timeouts/circuit breakers).
- Multi-provider coexistence multiplies adapter code paths — keep interfaces thin.

---

## 10. Operational Implications

- Each enabled provider = an **ops surface**: monitoring, credential rotation, SLAs, cost.
- **Customer-managed providers shift some ops to the customer** — define an RACI + a support
  boundary; surface health in the **Integration Hub**.
- **Switching runbooks** per category (storage migration/dual-read; messaging drain; search
  reindex; identity re-auth). "Config switch" ≠ "no migration".
- Observability: per-(tenant, provider) metrics, error rates, latency, fallback events.
- Cost: egress/inter-cloud transfer can be significant (esp. storage) — surface to tenant.

---

## 11. Vendor Lock-In Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Vendor SDK types leak into domain code | Adapters isolate SDKs; core sees only interfaces; arch tests enforce |
| Provider-specific features bleed into the interface | Keep interface LCD; expose extras via **capability flags**, not core methods |
| Data-format lock-in (storage/search/BI) | Store our own canonical formats; treat provider as transport/index, not system of record |
| Identity proprietary flows | Standardize on **OIDC/OAuth2 + SCIM**; reject vendor-only protocols |
| Messaging semantics (ordering/exactly-once) | Design for at-least-once + idempotent consumers (ADR-009) — portable across brokers |
| Egress/cost lock-in | Per-tenant placement + cost visibility; avoid cross-cloud chatter |
| "All-in on one cloud" ops assumptions | Abstractions + IaC parameterized per provider |

---

## 12. Missing ADRs (to author)

- **ADR-027 — Provider-Abstraction Framework (umbrella)** — Approved 2026-06-18.
- **ADR-016 — Storage providers** (Azure Blob default; S3/GCS/Azure File/SMB/on-prem/NAS adapters; AV scan; retention).
- **ADR-014 — Cache providers** (Redis default; NCache/in-memory; **tenant-namespaced keys**).
- **ADR-009 — Messaging** (exists; *extend* to multi-provider: SQS/Kafka/ActiveMQ adapters + outbox).
- **ADR-028 — Notification providers** (email/SMS/push channel abstraction + routing).
- **ADR-008 — Identity** (exists; *extend* multi-IdP: Auth0/Ping via OIDC/SCIM).
- **ADR-015 — Search providers** (ES default; Azure AI Search/OpenSearch; neutral query model).
- **ADR-029 — Reporting/BI providers** (SSRS/embedded default; Power BI/embedded vendors; RLS model).

---

## Approval

Solution Architect: Approved · Integration Architect: Approved · Security Architect: Approved · Database Architect: Approved
Product Owner: Approved (Bhajan Lal, 2026-06-18)
