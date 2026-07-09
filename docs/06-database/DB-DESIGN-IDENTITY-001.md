# Database Design - Identity & Access (FR-002)

Module: Platform / `security` schema  
Author: Database Architect (Agent 7)  
Created Date: 2026-06-14  
Last Updated: 2026-06-28  
Version: 1.2  
Status: Approved (Bhajan Lal, 2026-06-28 amendment)

> Doc 3 of 5 required before development. Original approval: 2026-06-18. This
> amendment adds break-glass emergency access, tenant password policy configuration,
> authentication security events, enhanced session/device management, and
> effective-dated security configuration.

---

## 1. Purpose

This document defines the SQL Server database design for Identity, Authentication,
RBAC, ABAC, session governance, emergency access, and authentication security
monitoring.

The design must support:

- Multi-tenant SaaS isolation through `TenantId`, SQL Server Row-Level Security, and
  application tenant context.
- RBAC + ABAC authorization with deny-by-default behavior.
- Tenant-configurable password and authentication policies.
- Secure session, device, token, and revocation management.
- Controlled break-glass emergency administration.
- Full auditability and forensic traceability.
- Effective dating for role and ABAC policy changes.
- Extension-friendly implementation without hardcoded tenant or customer rules.

---

## 2. Standards Alignment

This design follows:

- `DATABASE_STANDARDS.md`
- `SECURITY_STANDARDS.md`
- `ADR-003 SQL Server`
- `ADR-005 Multi-tenancy`
- `ADR-006 Tenant Context & Data Access`
- `ADR-007 Effective-dated Data`
- `ADR-008 Identity & Access`
- `SEC-DESIGN-001 Threat Model`
- `FEAT-IDENTITY-001 Business Requirements`
- `TECH-IDENTITY-001 Technical Design`
- `UI-IDENTITY-001 UI Design`
- `TEST-IDENTITY-001 Test Plan`

All tenant-scoped tables must include the mandatory columns:

- `TenantId`
- `CreatedBy`
- `CreatedDate`
- `ModifiedBy`
- `ModifiedDate`
- `IsDeleted`
- `VersionNumber`

Physical deletion is not allowed for security records except controlled purge jobs
for expired tokens or telemetry records approved by retention policy.

---

## 3. Schema Overview

Schema: `security`

Global catalog tables:

- `security.Permission`

Tenant-scoped core tables:

- `security.UserAccount`
- `security.PasswordPolicy`
- `security.PasswordHistory`
- `security.Role`
- `security.RolePermission`
- `security.UserRole`
- `security.AbacPolicy`
- `security.Delegation`
- `security.RefreshToken`
- `security.Session`
- `security.AuthSecurityEvent`
- `security.BreakGlassAccess`
- `security.BreakGlassSession`

Supporting audit records continue to be written to the `audit` schema:

- `audit.AccessLog`
- `audit.ChangeLog`
- `audit.SecurityEventLog`

---

## 4. Table Designs

### 4.1 `security.UserAccount`

Stores tenant-scoped user identity records.

| Column | Purpose |
|---|---|
| `UserAccountId` | Primary key |
| `TenantId` | Tenant isolation key |
| `Email` | Normalized login email |
| `AuthProvider` | `Local`, `EntraID`, `Google`, `Okta`, or configured provider key |
| `ExternalSubjectId` | External identity-provider subject identifier |
| `PasswordHash` | Hashed password for local auth; null for pure SSO users |
| `PasswordPolicyId` | Active password policy reference where local auth applies |
| `Status` | `Active`, `Disabled`, `Locked`, `PendingActivation`, `PendingRecovery` |
| `MfaEnabled` | MFA enrollment state |
| `MfaSecretRef` | Secret reference, never raw secret material |
| `LastLoginAt` | Last successful authentication |
| `FailedLoginCount` | Current failed login counter |
| `LockedUntil` | Lockout expiry |
| `PasswordChangedAt` | Last local password change |
| `PasswordExpiresAt` | Tenant-policy-driven expiry date, if enabled |
| `SecurityStamp` | Changes on password, MFA, role, session, or risk-reset events |
| Mandatory audit columns | Required platform metadata |

Rules:

- `Email` is unique within a tenant.
- `ExternalSubjectId` is unique per tenant and provider when populated.
- Passwords must be stored only as strong adaptive hashes.
- MFA secrets and recovery material must be stored as secret references or encrypted
  values, never plain text.

### 4.2 `security.PasswordPolicy`

Stores tenant-specific password and account lockout configuration as data.

| Column | Purpose |
|---|---|
| `PasswordPolicyId` | Primary key |
| `TenantId` | Tenant isolation key |
| `Name` | Policy name |
| `MinimumPasswordLength` | Minimum configured length |
| `RequireUppercase` | Requires uppercase character |
| `RequireLowercase` | Requires lowercase character |
| `RequireNumeric` | Requires numeric character |
| `RequireSpecialCharacter` | Requires special character |
| `PasswordHistoryCount` | Number of previous password hashes blocked from reuse |
| `MaximumPasswordAgeDays` | Optional password age policy |
| `FailedLoginThreshold` | Failed login count before lockout/challenge |
| `AccountLockoutDurationMinutes` | Lockout duration |
| `PasswordReuseRestrictionDays` | Time-based reuse restriction |
| `CommonPasswordCheckEnabled` | Blocks known weak/common passwords |
| `CompromisedPasswordCheckEnabled` | Enables compromised credential screening where configured |
| `AdaptiveChallengeEnabled` | Allows extra challenge based on risk signals |
| `EffectiveFrom` | Policy start date/time |
| `EffectiveTo` | Policy end date/time |
| Mandatory audit columns | Required platform metadata |

Rules:

- Only one active default password policy per tenant may be effective at a time.
- Policy changes must create audit entries and must not silently weaken existing
  tenant security posture.
- Password policy is configuration, not code.

### 4.3 `security.PasswordHistory`

Stores historical password hashes needed to enforce password reuse restrictions.

| Column | Purpose |
|---|---|
| `PasswordHistoryId` | Primary key |
| `TenantId` | Tenant isolation key |
| `UserAccountId` | User reference |
| `PasswordHash` | Historical password hash |
| `RetainedUntil` | Retention expiry |
| Mandatory audit columns | Required platform metadata |

Rules:

- Hashes are retained only as long as required by tenant policy and legal/security
  retention limits.
- This table must never expose password history values through application APIs.

### 4.4 `security.Role`

Stores tenant-scoped roles.

| Column | Purpose |
|---|---|
| `RoleId` | Primary key |
| `TenantId` | Tenant isolation key |
| `Name` | Role name |
| `IsSystem` | System-managed role flag |
| `Description` | Human-readable purpose |
| `EffectiveFrom` | Role activation date/time |
| `EffectiveTo` | Role end date/time |
| Mandatory audit columns | Required platform metadata |

Rules:

- Role names are unique per tenant across active effective windows.
- System roles cannot be deleted or modified outside controlled migration/governance
  flows.

### 4.5 `security.Permission`

Global catalog of fine-grained platform permissions.

| Column | Purpose |
|---|---|
| `PermissionId` | Primary key |
| `Key` | Stable permission key, for example `Leave.Approve` |
| `Description` | Permission description |
| `Module` | Owning module |
| `SensitivityLevel` | Optional governance classification |
| `IsDeprecated` | Deprecation flag |

Rules:

- This is a global read-only catalog, not tenant-scoped.
- Tenant-specific permission enablement is handled through roles, policies, feature
  flags, and module configuration.

### 4.6 `security.RolePermission`

Maps roles to permissions with effective dating.

| Column | Purpose |
|---|---|
| `TenantId` | Tenant isolation key |
| `RoleId` | Role reference |
| `PermissionId` | Permission reference |
| `EffectiveFrom` | Permission assignment start |
| `EffectiveTo` | Permission assignment end |
| Mandatory audit columns | Required platform metadata |

Primary key:

- `TenantId`, `RoleId`, `PermissionId`, `EffectiveFrom`

Rules:

- Overlapping effective windows for the same role-permission pair are not allowed.
- Changes must publish `TenantRoleMatrixChanged`.

### 4.7 `security.UserRole`

Maps users to roles.

| Column | Purpose |
|---|---|
| `TenantId` | Tenant isolation key |
| `UserAccountId` | User reference |
| `RoleId` | Role reference |
| `AssignedBy` | Assigning user |
| `AssignedAt` | Assignment timestamp |
| `ValidFrom` | Optional assignment start |
| `ValidTo` | Optional assignment end |
| Mandatory audit columns | Required platform metadata |

Primary key:

- `TenantId`, `UserAccountId`, `RoleId`, `ValidFrom`

Rules:

- User role assignments must be tenant scoped.
- Changes must invalidate authorization and AI conversation memory where applicable.

### 4.8 `security.AbacPolicy`

Stores ABAC policy metadata and links to the rule engine.

| Column | Purpose |
|---|---|
| `AbacPolicyId` | Primary key |
| `TenantId` | Tenant isolation key |
| `Name` | Policy name |
| `PermissionKey` | Permission this policy constrains |
| `RuleSetId` | Rule engine rule-set reference |
| `Effect` | `Allow` or `Deny` |
| `PolicyVersion` | Version number used in decision traceability |
| `Priority` | Evaluation order |
| `EffectiveFrom` | Policy activation date/time |
| `EffectiveTo` | Policy end date/time |
| Mandatory audit columns | Required platform metadata |

Rules:

- Deny policies take precedence over allow policies.
- Policy changes must be versioned and auditable.
- Authorization logs must record evaluated policy version and decision reason.

### 4.9 `security.Delegation`

Stores controlled delegation and on-behalf-of access windows.

| Column | Purpose |
|---|---|
| `DelegationId` | Primary key |
| `TenantId` | Tenant isolation key |
| `FromUserId` | Delegating user |
| `ToUserId` | Delegate user |
| `ScopeJson` | Permission/resource scope |
| `ValidFrom` | Delegation start |
| `ValidTo` | Delegation end |
| `Active` | Current active flag |
| Mandatory audit columns | Required platform metadata |

Rules:

- Delegation must be time-bound.
- Delegated actions must write `OnBehalfOf` audit metadata.

### 4.10 `security.RefreshToken`

Stores refresh token metadata and revocation lineage.

| Column | Purpose |
|---|---|
| `RefreshTokenId` | Primary key |
| `TenantId` | Tenant isolation key |
| `UserAccountId` | User reference |
| `TokenHash` | Hashed token value |
| `IssuedAt` | Token issue timestamp |
| `ExpiresAt` | Expiry timestamp |
| `RevokedAt` | Revocation timestamp |
| `RevokedReason` | Revocation reason |
| `ReplacedById` | Rotation lineage |
| `SessionId` | Associated session |
| Mandatory audit columns | Required platform metadata |

Rules:

- Refresh tokens are stored only as hashes.
- Rotation must revoke the previous token and set `ReplacedById`.
- Cluster-wide revocation must use the distributed revocation architecture defined in
  `TECH-IDENTITY-001`.

### 4.11 `security.Session`

Stores authenticated session and device metadata for security dashboards, remote logout,
global logout, and distributed revocation.

| Column | Purpose |
|---|---|
| `SessionId` | Primary key |
| `TenantId` | Tenant isolation key |
| `UserAccountId` | User reference |
| `DeviceId` | Stable device/session fingerprint identifier where permitted |
| `DeviceName` | User-friendly device label |
| `Browser` | Browser family |
| `OperatingSystem` | Operating system family |
| `UserAgent` | User-agent string or normalized representation |
| `IPAddressHash` | Hashed IP address |
| `IPAddressEncrypted` | Optional encrypted IP value when policy permits storage |
| `ApproximateLocation` | Coarse location only |
| `IsCurrentSession` | UI projection or persisted flag for the requesting session |
| `CreatedAt` | Session creation |
| `LastSeenAt` | Last platform observation |
| `LastActivityAt` | Last user activity |
| `ExpiresAt` | Session expiry |
| `RevokedAt` | Revocation timestamp |
| `RevokedReason` | `UserLogout`, `AdminRevoked`, `GlobalLogout`, `Risk`, `BreakGlassExpired`, etc. |
| `SecurityStamp` | User security stamp at session issue |
| Mandatory audit columns | Required platform metadata |

Rules:

- Raw IP addresses should not be stored unless explicitly permitted by policy; prefer
  hash or encrypted representation.
- `IsCurrentSession` should normally be computed at query time from the caller session
  to avoid stale state. If persisted for performance, it must be treated as a projection.
- Session revocation must propagate across all application instances.

### 4.12 `security.AuthSecurityEvent`

Stores authentication and identity-security events for monitoring, investigation, and
compliance evidence.

| Column | Purpose |
|---|---|
| `AuthSecurityEventId` | Primary key |
| `TenantId` | Tenant isolation key |
| `UserAccountId` | Nullable user reference |
| `SessionId` | Nullable session reference |
| `EventType` | Event classification |
| `Severity` | `Info`, `Low`, `Medium`, `High`, `Critical` |
| `CorrelationId` | End-to-end trace identifier |
| `IPAddressHash` | Hashed source IP |
| `DeviceId` | Device reference |
| `ApproximateLocation` | Coarse location |
| `RiskScore` | Optional risk score |
| `EventJson` | Structured event metadata |
| `DetectedAt` | Detection timestamp |
| `ResolvedAt` | Resolution timestamp |
| Mandatory audit columns | Required platform metadata |

Event types include:

- `FailedLogin`
- `AccountLockout`
- `BruteForceDetected`
- `CredentialStuffingDetected`
- `ImpossibleTravelDetected`
- `SuspiciousDeviceLogin`
- `AdaptiveMfaChallenge`
- `MfaFailed`
- `PasswordResetRequested`
- `PasswordResetCompleted`
- `SessionRevoked`
- `BreakGlassRequested`
- `BreakGlassApproved`
- `BreakGlassActivated`
- `BreakGlassRevoked`
- `AuthorizationDenied`

Rules:

- Security events are append-only except controlled enrichment fields such as
  `ResolvedAt`.
- Sensitive values in `EventJson` must be redacted, hashed, tokenized, or encrypted.

### 4.13 `security.BreakGlassAccess`

Stores approved emergency-access grants for exceptional operational scenarios.

| Column | Purpose |
|---|---|
| `BreakGlassAccessId` | Primary key |
| `TenantId` | Tenant isolation key |
| `UserAccountId` | Emergency-access user |
| `Reason` | Mandatory business reason |
| `IncidentReference` | Incident or change reference |
| `RequestedBy` | Requesting user |
| `ApprovedBy` | Approving user, nullable if policy allows single-party emergency mode |
| `ApprovalWorkflowInstanceId` | Workflow reference where approval is required |
| `ValidFrom` | Emergency access start |
| `ValidTo` | Emergency access expiry |
| `Status` | `Requested`, `Approved`, `Active`, `Expired`, `Revoked`, `Denied` |
| `RevokedAt` | Revocation timestamp |
| `RevokedReason` | Revocation reason |
| Mandatory audit columns | Required platform metadata |

Rules:

- Break-glass access must be time-limited.
- A reason and incident/change reference are mandatory before activation.
- Emergency access must never become permanent administrative access.
- All lifecycle changes must create `AuthSecurityEvent` and audit entries.

### 4.14 `security.BreakGlassSession`

Links active emergency sessions to approved break-glass access records.

| Column | Purpose |
|---|---|
| `BreakGlassSessionId` | Primary key |
| `TenantId` | Tenant isolation key |
| `BreakGlassAccessId` | Emergency access grant reference |
| `UserAccountId` | Emergency-access user |
| `SessionId` | Authenticated session reference |
| `StartedAt` | Emergency session start |
| `ExpiresAt` | Emergency session expiry |
| `EndedAt` | Normal end timestamp |
| `RevokedAt` | Revocation timestamp |
| `RevokedReason` | Revocation reason |
| `EmergencyScopeJson` | Limited emergency access scope |
| `AuditReferenceId` | Audit event reference |
| Mandatory audit columns | Required platform metadata |

Rules:

- Emergency sessions expire automatically at `ExpiresAt`.
- Revoking `BreakGlassAccess` must revoke linked active sessions.
- Every action performed in this session must include break-glass context in audit.

---

## 5. Relationships

- `UserAccount` to `Role` is many-to-many through `UserRole`.
- `Role` to `Permission` is many-to-many through `RolePermission`.
- `AbacPolicy` references the rule engine through `RuleSetId`.
- `UserAccount` has many `RefreshToken`, `Session`, `PasswordHistory`, and
  `AuthSecurityEvent` records.
- `PasswordPolicy` applies to local-auth users and may be assigned per tenant or user
  class.
- `BreakGlassAccess` has zero or more `BreakGlassSession` records.
- `BreakGlassSession` references `Session`.
- `AuthSecurityEvent` may reference `UserAccount` and `Session` when known.

---

## 6. Indexing Strategy

Mandatory:

- Every tenant-scoped table has an index beginning with `TenantId`.
- All foreign keys are indexed.
- All frequently filtered effective-dated tables have active-window indexes.

Recommended indexes:

| Table | Index |
|---|---|
| `UserAccount` | Unique `(TenantId, Email)` |
| `UserAccount` | Unique filtered `(TenantId, AuthProvider, ExternalSubjectId)` where `ExternalSubjectId` is not null |
| `PasswordPolicy` | `(TenantId, EffectiveFrom, EffectiveTo)` |
| `PasswordHistory` | `(TenantId, UserAccountId, CreatedDate)` |
| `Role` | Unique active-window index on `(TenantId, Name, EffectiveFrom)` |
| `RolePermission` | `(TenantId, RoleId, PermissionId, EffectiveFrom, EffectiveTo)` |
| `UserRole` | `(TenantId, UserAccountId, RoleId, ValidFrom, ValidTo)` |
| `AbacPolicy` | `(TenantId, PermissionKey, EffectiveFrom, EffectiveTo, Priority)` |
| `Delegation` | `(TenantId, FromUserId, ToUserId, ValidFrom, ValidTo, Active)` |
| `RefreshToken` | Unique `TokenHash` |
| `RefreshToken` | `(TenantId, UserAccountId, RevokedAt, ExpiresAt)` |
| `Session` | `(TenantId, UserAccountId, RevokedAt, ExpiresAt)` |
| `Session` | `(TenantId, DeviceId, LastActivityAt)` |
| `AuthSecurityEvent` | `(TenantId, EventType, DetectedAt)` |
| `AuthSecurityEvent` | `(TenantId, UserAccountId, DetectedAt)` |
| `AuthSecurityEvent` | `(TenantId, CorrelationId)` |
| `BreakGlassAccess` | `(TenantId, UserAccountId, Status, ValidFrom, ValidTo)` |
| `BreakGlassSession` | `(TenantId, BreakGlassAccessId, ExpiresAt, RevokedAt)` |
| `Permission` | Unique `Key` |

---

## 7. Tenant Isolation and Row-Level Security

All tenant-scoped tables must enforce:

- `TenantId` as a required non-null column.
- SQL Server Row-Level Security filter predicates.
- SQL Server Row-Level Security block predicates where write protection is required.
- Application tenant context validation before database access.
- No cross-tenant joins unless explicitly performed by approved platform operations.
- No tenant inference from user input alone.

`security.Permission` is the only non-tenant-scoped table in this design. It is a
global catalog and must be treated as controlled reference data.

---

## 8. Encryption, Hashing, and Sensitive Data

- Passwords must use strong adaptive hashing.
- Refresh tokens must be stored only as hashes.
- MFA secrets, recovery secrets, emergency credentials, and sensitive identity provider
  secrets must use Key Vault, HSM, or encrypted secret references.
- IP addresses should be hashed for routine security analytics and encrypted only when
  exact recovery is justified by policy.
- `EventJson`, `ScopeJson`, and `EmergencyScopeJson` must not contain plain-text
  credentials, tokens, session secrets, or full sensitive identity payloads.
- Always Encrypted or equivalent protection should be used where sensitive values must
  be queryable or stored in SQL Server.

---

## 9. Effective Dating and Historical Traceability

Effective dating is mandatory for:

- `security.Role`
- `security.RolePermission`
- `security.AbacPolicy`
- `security.PasswordPolicy`

Rules:

- Scheduled role and policy changes must be represented as future-effective rows.
- Historical authorization investigations must be able to identify which role,
  permission, and ABAC policy versions were active at the decision time.
- Overlapping active windows are not allowed for the same logical configuration key.
- Policy changes must generate audit entries and invalidation events.

---

## 10. Audit and Event Requirements

The database design must support audit coverage for:

- Login success and failure.
- Password reset and account unlock.
- MFA enrollment, challenge, success, and failure.
- Role assignment changes.
- Role-permission matrix changes.
- ABAC policy changes.
- Delegation and impersonation.
- Session creation, remote logout, global logout, expiry, and revocation.
- Break-glass request, approval, activation, expiry, and revocation.
- Authorization allow/deny decisions.

Required trace fields:

- `TenantId`
- `UserAccountId`
- `OnBehalfOfUserId` where delegation or impersonation applies
- `SessionId`
- `CorrelationId`
- `PermissionKey`
- `PolicyVersion`
- `Decision`
- `DecisionReason`
- `OccurredAt`

---

## 11. Data Retention

Retention is governed by ADR-022 and tenant/compliance policy.

Minimum expectations:

- Expired refresh tokens may be purged after the configured security retention window.
- Security events must be retained long enough for audit, investigation, and compliance.
- Break-glass access and break-glass session records must be retained as high-value
  security evidence.
- Password history must be retained only as required for password reuse enforcement.
- Legal hold overrides normal deletion or archival jobs.

---

## 12. Migration Notes

Implementation must use DbUp SQL-script migrations only (ADR-037).

Migration order:

1. Add `PasswordPolicy` and `PasswordHistory`.
2. Extend `UserAccount` with password governance columns.
3. Add effective dating to `Role`, `RolePermission`, and `AbacPolicy`.
4. Extend `Session` for device, location, revocation, and activity fields.
5. Add `AuthSecurityEvent`.
6. Add `BreakGlassAccess` and `BreakGlassSession`.
7. Add indexes, constraints, and RLS policies.
8. Backfill default tenant password policies.
9. Validate no tenant-scoped table is missing `TenantId` or mandatory audit columns.

Backward compatibility:

- Existing active roles and ABAC policies receive `EffectiveFrom` equal to migration
  time and `EffectiveTo = NULL`.
- Existing sessions may have nullable device and location fields until reauthentication.
- Existing local users are assigned the tenant default password policy.

---

## 13. Acceptance Criteria

| ID | Criteria |
|---|---|
| DB-IDENTITY-AC-001 | Every tenant-scoped identity table includes `TenantId`, mandatory audit columns, and RLS coverage. |
| DB-IDENTITY-AC-002 | Break-glass emergency access can be represented with approval, reason, incident reference, time limit, revocation, and audit traceability. |
| DB-IDENTITY-AC-003 | Break-glass sessions are linked to approved access grants and normal sessions. |
| DB-IDENTITY-AC-004 | Tenant-configurable password policies are stored as effective-dated configuration data. |
| DB-IDENTITY-AC-005 | Password history supports password reuse prevention without exposing password material. |
| DB-IDENTITY-AC-006 | Authentication security events support brute-force, credential stuffing, suspicious device, adaptive MFA, account lockout, and break-glass monitoring. |
| DB-IDENTITY-AC-007 | Session records support active sessions, device visibility, remote logout, global logout, last activity, expiry, and revocation reason. |
| DB-IDENTITY-AC-008 | Role, role-permission, ABAC, and password-policy changes are effective-dated and auditable. |
| DB-IDENTITY-AC-009 | Token and session revocation can be enforced consistently across distributed application instances. |
| DB-IDENTITY-AC-010 | Sensitive authentication values are hashed, encrypted, or stored as secret references according to security policy. |
| DB-IDENTITY-AC-011 | Authorization investigations can identify evaluated permission, ABAC policy version, decision, reason, tenant, user, and correlation ID. |
| DB-IDENTITY-AC-012 | No customer-specific rule, password rule, role rule, or access rule requires a database schema change or core code change. |

---

## 14. External References

References last validated: 2026-06-28.

- Microsoft Learn - SQL Server Row-Level Security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
- Microsoft Learn - SQL Server Always Encrypted: https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-database-engine
- Microsoft Learn - Manage emergency access admin accounts: https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access
- NIST SP 800-63B Digital Identity Guidelines, Authentication and Authenticator Management: https://pages.nist.gov/800-63-4/sp800-63b.html
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

---

## 15. Approval

Database Architect: Approved  
Security Architect: Approved  
Solution Architect: Approved  
Product Owner: Approved (Bhajan Lal, 2026-06-28 amendment)
