# ADR-027 — Provider-Abstraction Framework (Vendor Independence)

Architecture Decision Record

Date: 2026-06-15
Status: Approved (Bhajan Lal, 2026-06-18)

---

# Context

The platform must let tenants choose their own infrastructure/integration providers —
storage (Azure Blob/S3/GCS/on-prem), cache (Redis/NCache/in-memory), messaging (Service
Bus/RabbitMQ/SQS/Kafka), notifications (SMTP/SendGrid/Graph/SES, Twilio/MSG91, Firebase),
identity (Entra/Okta/Google/Auth0/Ping), search (ES/Azure AI Search/OpenSearch), and BI
(SSRS/Power BI/embedded) — via **configuration only**, with multiple providers coexisting
across tenants in one environment. Without a uniform approach this becomes per-vendor
spaghetti and hard lock-in. Generalizes ADR-019 (multi-provider LLM). See ARCH-REVIEW-002.

# Decision

Adopt a **single, uniform Provider-Abstraction Framework** for every external dependency:

1. **Thin interface per category** (LCD contract) — domain/application code depends only on
   the interface; vendor SDKs live in adapter projects and never leak into core.
2. **Adapters** per provider; a **provider registry** (`catalog.Provider`) with capability
   metadata.
3. **Per-tenant configuration** (`catalog.TenantProviderConfig`): providerKey + configJson +
   **Key Vault secret reference** + primary/fallback + enabled + effective-date.
4. **`IProviderResolver<T>`** resolves the adapter for the current tenant at runtime, with
   **health-check, fallback, and config caching**; clients pooled per (tenant, provider).
5. **Capability flags** expose provider-specific extras without polluting the core interface.
6. **Admin-only, audited, validated** provider config (test-connection before activate),
   surfaced in the Integration Hub; sandbox→prod promotion.
7. **Honest switching:** new operations switch by config; existing state requires a
   documented migration/transition (storage copy, messaging drain, search reindex, identity
   re-auth). Cache switch is safe (cold start).

**Build scope (full-product launch, phased execution):** build the framework + the provider adapters
the launch requires (Azure defaults + the specific providers committed launch customers
use). Every interface is pluggable, so *additional* providers are added as later tenants
need them — adapters are an **integration axis, not a feature gate**. Building speculative
adapters for providers no customer has requested remains wasteful and is avoided.

# Alternatives Considered

- **Direct SDK usage per dependency** — fastest initially, but couples core to vendors and
  blocks tenant choice; high lock-in. Rejected.
- **One giant generic "provider" interface** — too leaky; each category has distinct
  semantics. Rejected for per-category thin interfaces + shared resolver.
- **Build all adapters now** — wasted effort for unproven demand. Rejected (design seams,
  build on demand).

# Consequences

Positive: vendor independence, per-tenant choice, multi-provider coexistence, testability
(mock interfaces), strong lock-in hedge. Negative: more abstraction + adapter code; resolver/
health/pooling infrastructure; switching runbooks. Risks: interface leakage (mitigated:
arch tests + capability flags), client sprawl at scale (mitigated: lazy-init + LRU pooling),
customer-managed-provider trust boundary (mitigated: private connectivity + fail-safe).

# Impact

Architecture: `IProviderResolver<T>` + per-category interfaces + adapter projects. Database:
`catalog.ProviderType/Provider/TenantProviderConfig/ProviderHealth`. Security: per-tenant
Key Vault secrets, cross-provider tenant isolation, SSRF/egress controls for customer
endpoints. Performance: resolver caching, pooling, circuit breakers. Development: never
reference a vendor SDK in core; add an adapter, not an `if`. Spawns per-category ADRs
(016 storage, 014 cache, 009 messaging-extend, 028 notifications, 008 identity-extend,
015 search, 029 BI).

# Approval

Solution Architect: Approved · Integration Architect: Approved · Security Architect: Approved · Database Architect: Approved ·
Product Owner: Approved (Bhajan Lal, 2026-06-18)
