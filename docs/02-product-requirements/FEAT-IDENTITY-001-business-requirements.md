# Feature Specification — Identity, AuthN & RBAC + ABAC (Business Requirements)

Feature Name: Identity & Access (FR-002)
Module: Platform / Security
Priority: Must (Phase 7A / Sprint S1)
Sprint: S1
Owner: Product Owner (Agent 2) / Security Architect (Agent 9)
Created Date: 2026-06-14
Last Updated: 2026-06-28
Version: 1.1
Status: Approved

> Doc 1 of 5 (Rule 1). Built in S1 alongside FR-015. Companions: TECH-IDENTITY-001,
> DB-DESIGN-IDENTITY-001, UI-IDENTITY-001, TEST-IDENTITY-001. Ratified by ADR-008;
> security per SEC-DESIGN-001.

---

# Problem Statement

Every module needs to know **who** the user is and **what** they may do. Enterprises require
**SSO + automated provisioning**, and authorization must be **fine-grained** (role *and*
attributes, e.g. "a manager sees only their department"). This is foundational to all modules.

# User Stories

- *As a User*, I want to log in via my company SSO (or local) with MFA, so access is secure and seamless.
- *As a Tenant Admin*, I want to define roles, permissions, and attribute scopes **without code**, so access matches our org.
- *As the System*, every request must be authorized **deny-by-default**, on both role and attributes, and every object access checked.

# Scope

**In:** JWT auth; **OIDC SSO** (Entra ID/Google/Okta) per tenant + local fallback; **MFA**;
adaptive/risk-based MFA; refresh-token rotation/revocation; forced logout; active session
and device management; configurable local-auth password policy; account lockout and
brute-force protection; break-glass emergency access; **SCIM** provisioning/deprovisioning;
**RBAC** (roles→permissions); **ABAC** (branch/office/department/location/BU/region);
central policy engine;
**delegation** + support **impersonation** (scoped, audited).
**Out (later):** SAML, passwordless/passkeys, fine-grained consent UI.

# Business Rules

1. **Deny-by-default**: no permission ⇒ no access; checked on every request **and** object (anti-IDOR).
2. RBAC **AND** ABAC both apply (e.g. `Leave.Approve` *and* same-department attribute).
3. Tokens are short-lived; refresh rotates and can be revoked; concurrent-session limits.
4. Sensitive operations support **maker-checker** (segregation of duties).
5. Delegation/impersonation are time-boxed, scoped, and **fully audited** (`OnBehalfOf`).
6. ABAC predicates are **config-as-data** (via the Rule Engine), not code.
7. Break-glass emergency access is allowed only for approved operational scenarios, is
   time-limited, requires a business reason and incident/change reference where applicable,
   may require dual approval, is fully audited, and must never become a permanent privilege.
8. Local-auth password rules are tenant-configurable within platform minimums: minimum
   length, complexity, password history, expiry where tenant policy requires it, reset
   verification, and compromised/common-password prevention.
9. Users and administrators can view and terminate active sessions/devices according to
   permission, including remote session termination and global logout.
10. Adaptive MFA must be triggered by configurable risk signals such as new device, new
    geography, impossible travel, high-risk administrative operation, unusual login
    behavior, leaked/compromised credential signal, or external IdP risk score.
11. Authentication endpoints must have configurable brute-force protections: failed-attempt
    thresholds, temporary lockout, progressive retry delay, rate limiting, optional
    challenge/CAPTCHA after suspicious behavior, security event generation, and audit.

# UI Requirements (UI-IDENTITY-001)

Login + tenant resolution (SSO/local/MFA); Roles & Permissions builder (matrix + ABAC scope,
clone/create); delegation; support impersonation (platform).

# API Requirements (API-SPEC-001 §1)

`/auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/sso/{tenant}`, `/me`; role/permission
admin endpoints; SCIM `/scim/v2/*`.

# Database Requirements (DB-DESIGN-IDENTITY-001)

`security` schema: UserAccount, Role, Permission, RolePermission, UserRole, AbacPolicy,
Delegation, RefreshToken/Session.

# Security Requirements

Core of the platform's security (SEC-DESIGN-001 §5). JWT signing/rotation; MFA; least-privilege
scopes; central PDP/PEP; all auth events audited.

# Enterprise Security Enhancements

## 1. Break Glass Emergency Access

The platform must support controlled break-glass emergency access for exceptional
operational situations only, such as:

- Identity provider outage.
- Tenant administrator lockout.
- Disaster recovery.
- Security incident response.
- Critical production support where normal privileged access is unavailable.

Requirements:

- Emergency access must be explicitly enabled by platform policy.
- Access is time-limited and expires automatically.
- Requester, approver, reason, duration, scope, incident/change reference, and all actions
  are audited.
- Highly privileged break-glass sessions may require dual approval.
- Break-glass access cannot bypass tenant isolation, audit, or data protection controls.
- Break-glass access cannot be converted into a permanent administrator role.
- Emergency sessions must be easy to identify in audit, monitoring, and reports.

## 2. Enterprise Password Policy

Local authentication must support tenant-configurable password policies with platform
minimums. The current platform baseline follows `SECURITY_STANDARDS.md`: minimum length 12
with uppercase, lowercase, number, and special character requirements.

Additional requirements:

- Password history prevents immediate reuse.
- Password expiry can be enabled where tenant policy or regulation requires it.
- Password reset requires verified recovery channel or administrator-approved reset flow.
- Common, weak, and known-compromised passwords are blocked.
- Passwords are never stored in plaintext and are hashed using approved password hashing.
- Password policy changes are audited and versioned.

## 3. Device and Session Management

The platform must provide session and device visibility.

User capabilities:

- View active sessions and logged-in devices.
- See login time, last activity, device/browser information, IP address and location where
  permitted by policy.
- Terminate a single session.
- Logout from all devices.

Administrator capabilities:

- View user sessions where authorized.
- Revoke sessions for compromised, terminated, suspended, or high-risk users.
- Enforce tenant session-expiry policies.
- Force logout after role, permission, tenant status, or risk changes.

## 4. Adaptive Risk-Based MFA

The platform must support adaptive MFA and step-up authentication. MFA may be required
when risk exceeds tenant-configured thresholds.

Risk signals include:

- New or unknown device.
- New country, region, network, or IP profile.
- Impossible or atypical travel.
- High-risk administrative operation.
- Unusual login behavior.
- Suspicious token or session behavior.
- Leaked credential or compromised-account signal.
- External identity-provider risk score.

Adaptive MFA reduces user friction by requiring additional verification only when policy
and risk require it. Sensitive operations may always require step-up authentication
regardless of sign-in risk.

## 5. Account Lockout and Brute-Force Protection

The platform must protect against credential stuffing, password guessing, and brute-force
attacks.

Requirements:

- Failed login attempt thresholds are configurable by tenant within platform limits.
- Temporary account lockout is applied after repeated failures.
- Progressive retry delays or exponential backoff are supported.
- Authentication endpoints are rate-limited by user, tenant, IP/network, device, and
  risk signal where appropriate.
- Optional CAPTCHA or equivalent challenge can be required after suspicious behavior.
- Repeated failures, lockouts, password-spray indicators, and suspicious authentication
  attempts generate security events and audit records.
- Lockout controls must avoid creating easy denial-of-service paths against legitimate
  users.

# Non-Functional

Auth adds < 50ms; policy decisions cached; supports multi-IdP per tenant; P95 login < 2s.

# Acceptance Criteria

1. A user logs in via SSO **and** local fallback; MFA challenge enforced when enabled.
2. A manager can access **only** their department's employees (ABAC) — cross-department is **403**.
3. A branch administrator can access only assigned branch/office employees and operational
   records unless explicit scope grants allow child branches.
3. A missing permission yields **403**; a forged/expired token yields **401**.
4. A Tenant Admin creates a custom role + ABAC scope **with no code**, and it takes effect.
5. Impersonation and delegated actions are recorded as `OnBehalfOf` in the audit trail.
6. Break-glass access requires approved scenario, reason, expiry, audit, and cannot become
   a permanent privilege.
7. Tenant-configurable password policy enforces platform minimums, history, reset
   verification, and compromised-password prevention.
8. Users and authorized admins can view and terminate active sessions/devices; global logout
   revokes active refresh/session state.
9. Adaptive MFA is triggered for configured high-risk signals and sensitive operations.
10. Failed login thresholds, temporary lockout, retry delay/rate limit, optional challenge,
    and security-event logging protect authentication endpoints.

# Official and Primary References

- NIST SP 800-63B Digital Identity Guidelines - Authentication and Authenticator Management:
  `https://pages.nist.gov/800-63-4/sp800-63b.html`
- OWASP Authentication Cheat Sheet:
  `https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html`
- OWASP Session Management Cheat Sheet:
  `https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html`
- Microsoft Entra emergency access admin accounts:
  `https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access`
- Microsoft Entra risk detections:
  `https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks`

References last validated: 2026-06-28.

---

## Approval

Product Owner: Approved by Bhajan Lal 2026-06-28 · Security Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28 · Solution Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  (Status: Approved - owner approved 2026-06-28)
