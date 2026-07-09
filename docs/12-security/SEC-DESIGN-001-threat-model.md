# Security Design & Threat Model — Platform Foundations

Document Owner: Security Architect (Agent 9)
Created Date: 2026-06-14
Version: 1.0
Status: Approved (Bhajan Lal, 2026-06-18)

> Scope: platform-level security design and threat model for the Phase 7A foundations
> (multi-tenant isolation, identity, workflow/rule engines, event/outbox, provider
> abstraction, audit, data protection).
> Implements `SECURITY_STANDARDS.md`; aligns with ADR-005 (RLS), ADR-006 (tenant
> context), ADR-008 (identity), ADR-009 (events/outbox), ADR-027 (provider abstraction),
> and ADR-024 (audit immutability). Module-specific threat models follow per feature.

---

# 1. Security Objectives

- **Tenant isolation is absolute** — no cross-tenant read/write under any code path.
- **Deny-by-default authorization** — RBAC + ABAC on every request and every object.
- **Confidentiality of PII & payroll** — encryption, masking, least privilege.
- **Tamper-evident audit** — who did what, when, on whose behalf.
- **OWASP Top 10 defended** by design, verified by tests (≥85% incl. security tests).

---

# 2. Trust Boundaries (ASCII)

```
  [ Browser / Mobile ]  ──TLS──►  [ API Gateway / WAF ]
        (untrusted)                   │  rate-limit, schema-validate
                                      ▼
                            [ Auth: JWT verify + tenant resolve ]
                                      │  (tenant context established here)
                                      ▼
                    [ Application services (modular monolith) ]
                       │ RBAC+ABAC policy checks (deny-by-default)
                       ▼
              [ Data access layer: injected tenant predicate + RLS session ctx ]
                       ▼
        [ SQL Server (RLS) | Provider Resolver | Redis (ns) | ES (per-tenant) | Blob | Key Vault ]
```
Every inward hop **re-establishes or re-validates** identity + tenant; nothing trusts the
layer above blindly.

---

# 3. STRIDE Threat Model (foundations)

| Threat | Example | Control |
|---|---|---|
| **Spoofing** | Forged JWT, stolen token | Signed short-lived JWT, refresh rotation + revocation, MFA, audience/issuer checks |
| **Tampering** | Modify another tenant's record, alter audit | TenantId + **RLS**, object-level authz, append-only/WORM audit, hash-chain |
| **Repudiation** | "I didn't approve that" | Immutable audit incl. `OnBehalfOf`; correlation IDs |
| **Information disclosure** | Cross-tenant leak, PII in logs | RLS + global filter, field-level encryption/masking, log redaction |
| **Denial of service** | One tenant exhausts resources | Per-tenant rate limits/quotas, async back-pressure, isolated batch workers |
| **Elevation of privilege** | Tenant admin → platform admin; expression RCE | Role separation, least-privilege scopes, **sandboxed rule expressions (no eval)** |
| **Provider boundary abuse** | Tenant-managed storage/search/SMS endpoint used for SSRF or data exfiltration | Provider allowlists, private connectivity, secret isolation, egress controls, audited config |

---

# 4. Multi-Tenant Isolation (the #1 risk)

Defense-in-depth (a single bug must not leak data):
1. **Validated tenant context** from JWT/host — never client-supplied.
2. **Repository-injected tenant predicate** on `TenantId` (app layer; central `RepositoryBase`/SQL-builder, ADR-037).
3. **SQL Server Row-Level Security** bound to `SESSION_CONTEXT('TenantId')` (DB layer) —
   blocks even a query that forgot the filter.
4. **Object-level authorization** — every entity fetch checks ownership (anti-IDOR).
5. **Namespaced caches / per-tenant search indices**; no shared mutable keys.
6. **Tests:** automated cross-tenant access tests in CI; a deliberately-unfiltered query
   must return zero rows.

---

# 5. Identity & Access (see ADR-008)

- **AuthN:** JWT (local) + OIDC SSO (Entra ID/Google/Okta) per tenant; SCIM provisioning;
  MFA; refresh-token rotation; forced logout; concurrent-session limits.
- **AuthZ:** RBAC (roles→permissions) **AND** ABAC (attributes: department/location/BU)
  via a central policy engine, deny-by-default. Example: manager sees only their dept.
- **Sensitive operations:** maker-checker / segregation of duties; salary-visibility rules;
  delegation/impersonation are scoped, time-boxed, and fully audited.

---

# 6. Data Protection

- **In transit:** TLS 1.2+ everywhere; per-white-label-domain certs.
- **At rest:** TDE; **field-level encryption** for high-sensitivity PII (bank, PAN, Aadhaar
  refs, salary); **BCrypt** for any local password; AES-256 for secrets.
- **Secrets:** Azure Key Vault; never in code/config/repo; rotation policy.
- **Masking:** role-based field masking (e.g., CTC hidden from non-authorized roles).
- **Classification:** PII tagged in schema → drives encryption, masking, retention, DSAR.

---

# 7. Application Security (OWASP)

- **Injection:** parameterized queries only; no dynamic SQL; **rule/expression sandbox**
  (JSON-AST, whitelist, no arbitrary code — ADR-011).
- **Broken access control:** central authz, object-level checks, no IDOR.
- **XSS/CSRF:** output encoding, CSP, anti-CSRF tokens; config-driven UI sanitized.
- **SSRF:** workflow/connector outbound calls use an **egress allowlist**.
- **File upload:** AV scan + MIME/extension/size validation + quarantine.
- **Provider integrations:** provider configs are admin-only, schema-validated, test-connection
  validated, egress-restricted, and audited before activation.
- **Mass assignment:** explicit DTOs, never bind to entities.
- **API:** schema validation, rate limiting, least-privilege OAuth scopes (ADR-023).

---

# 8. Audit & Monitoring

- Append-only `audit.ChangeLog` (field-level) + `audit.AccessLog` (login/logout/
  impersonation/denied) with correlation IDs; tamper-evident (hash chain); per-retention
  archival (ADR-022).
- Security monitoring: anomaly alerts (impossible travel, brute force, mass export),
  per-tenant dashboards.

---

# 9. Compliance Hooks (India-first)

- **DPDP:** consent capture, data residency (India), breach-notification readiness, DSAR
  + right-to-erasure workflow (with legal-hold precedence).
- Future GDPR (EU expansion): portability + erasure already modeled.
- Statutory data retention vs erasure conflict resolved by legal-hold rules.

---

# 10. Residual Risks & Mitigation Status

| Risk | Status | Plan |
|---|---|---|
| RLS performance overhead | Open | Benchmark in S1; index TenantId; accept as cost of safety |
| Expression-language abuse | Mitigated by design | AST + sandbox + tests (ADR-011) |
| Impersonation misuse | Mitigated | Scoped, time-boxed, audited; alerting |
| Third-party IdP outage | Open | Local-auth fallback per tenant policy |
| Secret sprawl | Mitigated | Key Vault + rotation; secret-scanning in CI |

---

## Approval

Security Architect: Approved · Solution Architect: Approved · Database Architect: Approved ·
Product Owner: Approved (Bhajan Lal, 2026-06-18)
