# Test Plan - Identity and Access

Feature Name: Identity and Access
Requirement ID: FR-002
Module: Platform / Security
Owner: QA Architect
Created Date: 2026-06-14
Last Updated: 2026-06-28
Version: 1.1
Status: Approved

> Doc 5 of 5 required before implementation. Companion docs:
> FEAT-IDENTITY-001, TECH-IDENTITY-001, DB-DESIGN-IDENTITY-001, UI-IDENTITY-001.
> Identity implementation may start only after all five documents are Approved.

---

# 1. Purpose

This test plan validates Identity and Access Management for the HRMS platform. It covers
local authentication, OIDC/SSO, MFA, adaptive MFA, break-glass emergency access, JWT and
refresh-token lifecycle, distributed session and revocation behavior, SCIM provisioning,
RBAC, ABAC, delegation, impersonation, audit, traceability, high availability, failover,
and attack resistance.

Identity is a Phase 7A foundation. Any confirmed authentication bypass, authorization
bypass, cross-tenant identity leak, ungoverned emergency access, or audit failure blocks
implementation acceptance.

---

# 2. Scope

In scope:

- Local authentication.
- OIDC/SSO authentication.
- MFA and adaptive/risk-based MFA.
- Password policy, reset, expiry, unlock, and recovery.
- Account lockout, throttling, rate limiting, and progressive challenges.
- JWT access tokens and signing key rotation.
- Refresh token rotation, reuse detection, and revocation.
- Distributed session management across application nodes.
- Break-glass emergency access.
- RBAC permission enforcement.
- ABAC policy enforcement through the Rule Engine.
- Object-level authorization and anti-IDOR.
- Delegation and impersonation.
- SCIM user and group provisioning/deprovisioning.
- Audit, compliance, and authorization decision traceability.
- UI security flows.
- Performance, high availability, and failover.

Out of scope:

- SAML.
- Passwordless/passkeys.
- Payroll/leave/business-module-specific authorization scenarios beyond identity
  enforcement tests.

---

# 3. Quality Gates

| Gate | Requirement |
|---|---|
| Security bypass | Zero tolerated authentication, authorization, tenant, or emergency-access bypass. |
| Unit coverage | At least 85 percent line and branch coverage; 90 percent target. |
| Critical identity coverage | 95 percent coverage for token, session, PDP/PEP, ABAC, revocation, break-glass, and audit services. |
| API contract | All identity APIs conform to approved OpenAPI before acceptance. |
| UI automation | Login, MFA, recovery, sessions, roles, delegation, impersonation, and break-glass flows covered by E2E tests. |
| Audit quality | Mandatory audit and traceability fields verified for full auth lifecycle. |
| Distributed readiness | Multi-node logout, revocation, cache failover, and session consistency pass. |
| Performance | Login, token refresh, PDP decision, and policy-cache targets meet approved SLOs. |

---

# 4. Test Environments

Required environments:

- Local developer test environment with fake IdP and deterministic clock.
- Integration environment with SQL Server and Tenant RLS enabled.
- Redis/distributed cache environment.
- Multi-node application environment with at least two app instances.
- OIDC sandbox tenants for Entra ID, Google, and Okta where feasible.
- SCIM test client environment.
- Security/adversarial test environment.
- Playwright UI automation environment.
- High-availability and failover test environment.

Tests for distributed session behavior must run against multiple application instances, not
only mocks.

---

# 5. Test Data

Minimum data:

- Tenant A and Tenant B.
- Active tenant, suspended tenant, and SSO-outage tenant.
- Employee, Manager, HR Admin, Tenant Admin, Platform Support, Security Reviewer, Emergency
  Operator, and unauthorized user.
- User with local auth.
- User with OIDC SSO.
- User with MFA enabled.
- User with disabled/locked account.
- User with expired password.
- User with multiple active sessions.
- Delegator and delegate.
- Impersonation target user.
- Emergency account/role.
- SCIM-provisioned user and group.
- Roles and permissions for multiple modules.
- ABAC policies for branch/office, department, location, business unit, region, and manager chain.

---

# 6. Functional Authentication Tests

## 6.1 Local Authentication

- `Login_ValidCredentials_IssuesAccessAndRefreshTokens`
- `Login_InvalidCredentials_ReturnsGeneric401`
- `Login_ClientSuppliedTenantMismatch_FailsClosed`
- `Login_TenantSuspended_ReturnsForbidden`
- `Login_DisabledUser_ReturnsForbidden`
- `Login_LocalFallbackDisabled_DoesNotAllowPasswordLogin`
- `Login_PasswordExpired_RoutesToPasswordReset`

## 6.2 OIDC / SSO

- `Sso_ValidAuthorizationCode_IssuesPlatformSession`
- `Sso_InvalidState_Rejected`
- `Sso_InvalidNonce_Rejected`
- `Sso_InvalidIssuer_Rejected`
- `Sso_InvalidAudience_Rejected`
- `Sso_TenantBindingMismatch_Rejected`
- `Sso_IdpOutage_FallsBackOnlyWhenTenantPolicyAllows`
- `Sso_IdpGroupMapping_MapsRolesCorrectly`

## 6.3 MFA and Adaptive MFA

- `Mfa_EnabledUser_ChallengeRequiredBeforeAccess`
- `Mfa_InvalidCode_ReturnsFailureAndAudit`
- `Mfa_ExpiredChallenge_Rejected`
- `AdaptiveMfa_NewDevice_RequiresStepUp`
- `AdaptiveMfa_NewGeography_RequiresStepUp`
- `AdaptiveMfa_ImpossibleTravel_RequiresStepUp`
- `AdaptiveMfa_SensitiveAdminOperation_RequiresStepUp`
- `AdaptiveMfa_LowRiskTrustedDevice_BypassesWhenPolicyAllows`

## 6.4 Password and Recovery

- `ForgotPassword_ExistingUser_ReturnsGenericResponse`
- `ForgotPassword_UnknownUser_ReturnsSameGenericResponse`
- `PasswordReset_ValidOtp_AllowsReset`
- `PasswordReset_ExpiredOtp_Rejected`
- `PasswordReset_CommonPassword_Rejected`
- `PasswordReset_PreviousPassword_RejectedWhenHistoryEnabled`
- `AccountUnlock_ValidVerification_UnlocksAccount`
- `AccountUnlock_InvalidVerification_Rejected`

---

# 7. Token, Session, and Revocation Tests

## 7.1 JWT and Refresh Token

- `AccessToken_Expired_Returns401`
- `AccessToken_TamperedSignature_Rejected`
- `AccessToken_WrongAudience_Rejected`
- `AccessToken_WrongIssuer_Rejected`
- `AccessToken_UnknownKid_TriggersKeyRefreshThenFailsClosedIfUnknown`
- `RefreshToken_Valid_RotatesAndRevokesOldToken`
- `RefreshToken_Reused_RevokeTokenFamilyAndSession`
- `RefreshToken_StoredHashed_NeverPlaintext`

## 7.2 Distributed Session and Token Revocation

- `Logout_NodeA_RevocationVisibleOnNodeB`
- `RefreshTokenRevoked_NodeA_RejectedOnNodeB`
- `DistributedSession_UpdateLastSeen_SynchronizesAcrossNodes`
- `ForcedLogout_User_AllActiveSessionsRevokedClusterWide`
- `GlobalLogout_AllDevices_RevokedAcrossInstances`
- `RevocationCache_SynchronizesUserSessionAndTokenFamily`
- `RevocationCache_RedisUnavailable_FallsBackToSqlOrFailsClosedPerPolicy`
- `TenantSuspended_AllTenantSessionsBlockedClusterWide`
- `RoleChanged_SecurityStampInvalidatesAffectedSessions`
- `AbacPolicyChanged_AuthorizationCacheInvalidatedClusterWide`

---

# 8. Break Glass Emergency Access Tests

Required scenarios:

- `BreakGlass_AuthorizedEmergencyOperator_AuthenticationSucceeds`
- `BreakGlass_UnauthorizedUser_AccessDenied`
- `BreakGlass_MissingReason_Rejected`
- `BreakGlass_MissingIncidentReference_RejectedWhenRequired`
- `BreakGlass_ApprovalRequired_BlocksUntilApproved`
- `BreakGlass_ApprovalDenied_DoesNotCreateSession`
- `BreakGlass_TimeLimitedSession_AutoExpires`
- `BreakGlass_ExpiredSession_AutomaticallyLoggedOut`
- `BreakGlass_Revocation_ImmediatelyTerminatesActiveSession`
- `BreakGlass_AdminAction_AuditedWithEmergencyReference`
- `BreakGlass_CannotGrantPermanentRole`
- `BreakGlass_DoesNotBypassTenantIsolationOrObjectAuthorization`

Exit requirement:

- Every break-glass authentication, approval, authorization decision, and administrative
  action is linked to the emergency access audit record.

---

# 9. Authorization Tests

## 9.1 RBAC

- `Access_WithoutPermission_Returns403`
- `Access_WithPermission_Allowed`
- `DenyByDefault_UnmappedAction_Returns403`
- `RolePermission_Added_TakesEffectAfterCacheInvalidation`
- `RolePermission_Removed_DeniesAccessClusterWide`

## 9.2 ABAC

- `Manager_AccessesOwnDepartmentEmployee_Allowed`
- `Manager_AccessesOtherDepartment_Returns403`
- `Manager_AccessesOwnLocationOnly_WhenLocationScopeConfigured`
- `BranchAdmin_AccessesOwnBranch_Allowed`
- `BranchAdmin_AccessesOtherBranch_Returns403`
- `AbacPolicyChange_NoCode_TakesEffect`
- `AbacPolicyVersion_DecisionTraceCapturesVersion`
- `AbacSensitiveAttributes_NotLoggedInPlaintext`

## 9.3 Object-Level Authorization

- `FetchById_OtherUsersObject_ReturnsForbiddenOrNotFoundPerPolicy`
- `UpdateById_OtherTenantObject_BlockedByTenantAndObjectChecks`
- `DeleteById_WithoutObjectScope_Returns403`
- `BulkOperation_MixedAuthorizedUnauthorized_ReturnsSafePerItemResults`

---

# 10. Delegation and Impersonation Tests

Delegation:

- `Delegation_ValidScope_AllowsDelegatedAction`
- `Delegation_Expired_NoLongerRoutes`
- `Delegation_OutsideScope_Returns403`
- `Delegation_GrantMoreThanDelegatorHas_Rejected`
- `DelegatedAction_AuditIncludesOnBehalfOf`

Impersonation:

- `Impersonation_AuthorizedSupportUser_CreatesScopedSession`
- `Impersonation_MissingReason_Rejected`
- `Impersonation_ExpiredSession_AutoTerminates`
- `Impersonation_TargetTenantScope_Enforced`
- `Impersonation_Action_AuditIncludesSupportAndTargetUser`
- `Impersonation_CannotBypassABAC`

---

# 11. SCIM Provisioning Tests

- `ScimProvision_CreateUser_CreatesTenantUser`
- `ScimProvision_UpdateUser_UpdatesAllowedAttributes`
- `ScimProvision_DeprovisionUser_DisablesUserAndRevokesSessions`
- `ScimGroup_Create_MapsToRole`
- `ScimGroup_RemoveUser_RemovesRoleAndInvalidatesSecurityStamp`
- `Scim_CrossTenantCredential_Rejected`
- `Scim_InvalidSchema_ReturnsScimError`
- `Scim_ReplayedRequest_IdempotentWhereRequired`

---

# 12. Authentication Security Attack Tests

Required attack scenarios:

- `Attack_BruteForceLogin_TriggersLockoutOrProgressiveDelay`
- `Attack_CredentialStuffing_RateLimitedAndSecurityEventRaised`
- `Attack_PasswordSpray_DetectedAcrossTenantAndIpSignals`
- `Attack_SessionFixation_NewSessionIssuedAfterLogin`
- `Attack_SessionHijacking_RevokedSessionRejected`
- `Attack_ReplayRefreshToken_TokenFamilyRevoked`
- `Attack_ReplayMfaChallenge_Rejected`
- `Attack_AuthEndpointRateLimit_Returns429OrConfiguredChallenge`
- `Attack_CaptchaOrChallenge_RequiredAfterSuspiciousActivity`
- `Attack_AdaptiveMfa_TriggeredForSuspiciousAuthentication`
- `Attack_GenericLoginErrors_PreventAccountEnumeration`
- `Attack_TokenAlgorithmConfusion_Rejected`

Security tests must verify that no passwords, MFA secrets, refresh tokens, raw ABAC rules,
provider tokens, or signing keys are exposed in UI, API responses, logs, or traces.

---

# 13. High Availability and Failover Tests

Required operational scenarios:

- `Ha_IdpOutage_LocalFallbackAllowed_LoginSucceeds`
- `Ha_IdpOutage_LocalFallbackDisabled_LoginFailsClosed`
- `Ha_DatabaseFailoverDuringLogin_LoginRetriesOrFailsSafely`
- `Ha_DatabaseFailoverDuringRefresh_NoDoubleTokenIssue`
- `Ha_RedisFailure_RevocationFallsBackOrFailsClosedPerPolicy`
- `Ha_AuthenticationServiceRestart_ActiveSessionsRemainValidIfNotRevoked`
- `Ha_JwtSigningKeyRotation_NoUserDisruptionDuringPlannedRollover`
- `Ha_JwtSigningKeyEmergencyRevocation_AffectedSessionsRevoked`
- `Ha_MultiNodeLoginConsistency_UnderLoad`
- `Ha_MultiNodeAuthorizationConsistency_UnderPolicyChange`

Failover tests must verify audit continuity and correlation ID preservation.

---

# 14. Audit, Compliance, and Traceability Tests

Required audit validation:

- `Audit_LoginSuccess_ContainsMandatoryFields`
- `Audit_LoginFailure_ContainsReasonCodeWithoutSensitiveData`
- `Audit_MfaChallengeAndResult_Recorded`
- `Audit_RefreshRotation_Recorded`
- `Audit_GlobalLogout_RecordedForAllSessions`
- `Audit_BreakGlass_FullLifecycleRecorded`
- `Audit_DelegationAction_IncludesOnBehalfOf`
- `Audit_ImpersonationAction_IncludesSupportAndTargetUser`
- `Audit_AuthorizationDecision_ContainsTenantUserPermissionPolicyVersionDecisionReasonCorrelationTimestamp`
- `Audit_CorrelationId_PropagatesAcrossAuthPdpDbAndEvent`
- `Audit_RecordIntegrity_TamperEvidenceVerified`
- `Audit_RetentionPolicy_Enforced`
- `Audit_SecurityEvents_ClassifiedBySeverityAndType`
- `Audit_CompleteAuthLifecycle_Covered`

Mandatory traceability fields:

- Tenant identifier.
- User identifier.
- Subject type.
- Requested permission.
- Resource type and ID where applicable.
- Evaluated ABAC policy and version.
- Decision: Allow or Deny.
- Decision reason.
- Correlation ID.
- Request ID.
- Timestamp.

---

# 15. UI and Accessibility Tests

Required Playwright or equivalent scenarios:

- Login with local auth.
- Login with SSO.
- MFA challenge and failure states.
- Adaptive MFA reason display.
- Forgot password and reset flow.
- Expired password flow.
- Account unlock flow.
- Security Dashboard.
- Active Sessions and Devices.
- Logout single session.
- Logout all devices.
- Roles and Permissions matrix.
- ABAC Policy Builder simulation.
- Delegation create/revoke.
- Impersonation start/exit.
- Break Glass Emergency Login and expiry countdown.
- Permission-gated navigation.
- 403 forbidden view.
- Keyboard-only operation.
- Screen-reader labels for errors, MFA, alerts, emergency mode, and countdowns.
- Responsive mobile/tablet/desktop checks.

---

# 16. Performance Tests

Required:

- Authentication overhead target: under 50 ms excluding IdP external round trip.
- Login P95 target: under 2 seconds for local auth under normal conditions.
- PDP decision latency with policy cache hit.
- PDP decision latency with policy cache miss.
- Refresh token rotation under load.
- Session revocation propagation latency.
- Role/permission/ABAC cache invalidation latency.
- SCIM bulk provisioning throughput.
- Multi-node authentication consistency under load.

---

# 17. Automation Strategy

Automation layers:

- Unit tests: password verifier, token service, signing key manager, risk engine, PDP, ABAC
  predicates, delegation, impersonation, break-glass service.
- Integration tests: SQL Server security tables, RLS enabled, Redis revocation cache,
  distributed session store, outbox/events.
- API tests: OpenAPI conformance, auth success/failure, authorization, SCIM, session APIs.
- Security tests: attack suite, token replay, session fixation, brute force, credential
  stuffing.
- UI tests: Playwright for user/admin/emergency flows.
- Performance tests: login, refresh, policy decision, revocation propagation.
- HA/failover tests: IdP, SQL, Redis, app restart, signing key rotation.

CI must fail on any critical identity security regression.

---

# 18. Exit Criteria

Identity and Access implementation cannot be accepted until:

- All FEAT, TECH, DB, UI, and TEST acceptance criteria pass.
- Authentication and authorization bypass tests show zero critical/high unresolved issues.
- Break-glass access tests pass with complete audit and automatic expiry.
- Distributed session/revocation tests pass across multiple app nodes.
- Attack tests for brute force, credential stuffing, fixation, hijacking, replay, rate limit,
  and adaptive MFA pass.
- HA/failover tests pass or documented fail-closed behavior is accepted by Security.
- Audit, traceability, retention, and integrity tests pass.
- OpenAPI contract tests pass.
- UI accessibility and E2E tests pass.
- Coverage meets project thresholds.

---

# 19. Official and Primary References

- NIST SP 800-63B Digital Identity Guidelines:
  `https://pages.nist.gov/800-63-4/sp800-63b.html`
- OWASP Authentication Cheat Sheet:
  `https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html`
- OWASP Session Management Cheat Sheet:
  `https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html`
- Microsoft Entra emergency access admin accounts:
  `https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access`
- Microsoft Entra emergency user access revocation:
  `https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access`
- RFC 8725 - JSON Web Token Best Current Practices:
  `https://datatracker.ietf.org/doc/html/rfc8725`

References last validated: 2026-06-28.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-28  
QA Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  
Security Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  
Solution Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  
Database Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  
Platform/Operations Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28

(Status: Approved - owner approved 2026-06-28)
