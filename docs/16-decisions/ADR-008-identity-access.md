# ADR-008 — Identity & Access Management

Architecture Decision Record

Date: 2026-06-14
Status: Approved (Bhajan Lal, 2026-06-18)

---

# Context

Every module needs authentication and fine-grained authorization (RBAC + ABAC), per
`ARCHITECTURE_PRINCIPLES.md` and `SECURITY_STANDARDS.md`. Tenants are enterprises that
expect SSO and automated provisioning. We must decide the identity architecture without
locking into a single IdP. See `SEC-DESIGN-001` §5.

# Decision

1. **Authentication:** JWT access tokens (short-lived) + rotating refresh tokens with
   revocation. **OIDC SSO per tenant** (Microsoft Entra ID, Google, Okta); local auth as
   fallback. MFA supported; forced logout + concurrent-session limits. **SAML** deferred.
2. **Provisioning:** **SCIM 2.0** for automated user provisioning/deprovisioning from
   tenant IdPs.
3. **Authorization:** a **central policy engine** enforcing **RBAC (roles→permissions)
   AND ABAC (attributes: department/location/business-unit/region)**, **deny-by-default**,
   evaluated on every request and every object (anti-IDOR). ABAC predicates are expressed
   via the Rule Engine (ADR-011), so policies are config-as-data.
4. **Sensitive controls:** maker-checker / segregation of duties; scoped, time-boxed,
   audited delegation (ADR via security schema) and support impersonation.
5. **Tokens carry** TenantId + userId + roles claims; ABAC attributes resolved server-side
   (not trusted from the token alone).

# Alternatives Considered

- **Build a bespoke IdP** — high cost/risk; rejected. Use standards (OIDC/SCIM) and a
  library/identity provider (e.g. Duende/ASP.NET Identity or managed) behind our policy layer.
- **RBAC only** — cannot express "manager sees only their department"; insufficient.
- **Per-module ad-hoc checks** — inconsistent, unauditable; rejected.

# Consequences

Positive: enterprise-ready SSO/SCIM, consistent deny-by-default authz, config-as-data
policies. Negative: policy-engine complexity; multi-IdP testing. Risks: token theft
(mitigated: short tokens, rotation, MFA); ABAC performance (mitigated: cached compiled
policies).

# Impact

Architecture: auth middleware + central PDP/PEP; `security` schema (ADR DB-DESIGN-001).
Security: core of the isolation/authz model. Performance: policy cache. Development: all
endpoints declare required permission + ABAC scope; no inline role checks.

# Approval

Security Architect: Approved · Solution Architect: Approved ·
Product Owner: Approved (Bhajan Lal, 2026-06-18)
