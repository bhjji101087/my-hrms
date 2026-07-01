# UI Design - Identity and Access

Feature Name: Identity and Access
Requirement ID: FR-002
Module: Platform / Security
Owner: UI Architect
Created Date: 2026-06-14
Last Updated: 2026-06-28
Version: 1.1
Status: Approved

> Doc 4 of 5 required before implementation. Companion docs:
> FEAT-IDENTITY-001, TECH-IDENTITY-001, DB-DESIGN-IDENTITY-001, TEST-IDENTITY-001.
> No Identity, Authentication, RBAC, or ABAC implementation may start until all five
> documents are Approved.

---

# 1. Purpose

This document defines the user interface for Identity and Access Management: login,
SSO, MFA, password recovery, session/device management, role and permission management,
ABAC scope configuration, delegation, impersonation, break-glass emergency access, and
security self-service.

The UI must be secure, clear, accessible, and suitable for non-technical users while still
supporting enterprise administration and operational resilience.

---

# 2. Design Inputs

- `DESIGN-SYSTEM-001-foundations.md`
- `DESIGN-SPEC-002-people-ops-platform.md`
- `FEAT-IDENTITY-001-business-requirements.md`
- `TECH-IDENTITY-001-technical-design.md`
- `DB-DESIGN-IDENTITY-001.md`
- `SEC-DESIGN-001-threat-model.md`
- `UI_STANDARDS.md`

---

# 3. Personas

| Persona | Primary Need |
|---|---|
| Employee | Sign in, recover account, manage sessions, respond to MFA. |
| Manager | Sign in securely and use delegated access where permitted. |
| Tenant Admin | Manage users, roles, permissions, ABAC scopes, sessions, and security settings. |
| Platform Support | Use scoped impersonation and support workflows with full audit. |
| Emergency Operator | Use controlled break-glass access during approved emergencies. |
| Security Reviewer | Review login history, suspicious activity, and access evidence. |

---

# 4. Navigation

User-facing security area:

- Security Dashboard
- Active Sessions and Devices
- Password and Recovery
- MFA Settings
- Login History

Tenant-admin identity area:

- Users
- Roles and Permissions
- ABAC Policies
- Delegation
- Security Policies
- Sessions

Platform support/security area:

- Impersonation
- Break Glass Emergency Access
- Identity Audit

Navigation is permission-gated. Users see only the identity surfaces allowed by their role,
tenant entitlements, and ABAC scope.

---

# 5. Screen A - Login and Tenant Resolution

Purpose: authenticate users through local login or tenant SSO and resolve tenant context.

APIs:

- `/auth/login`
- `/auth/sso/{tenant}`
- `/auth/mfa/*`
- `/me`

Required UI elements:

- Tenant logo and tenant name after tenant/domain resolution.
- Email/username input.
- Password input with show/hide control for local login.
- Continue with SSO action.
- Forgot password link.
- MFA challenge area when required.
- Generic invalid credential messaging.
- Tenant suspended state.
- SSO unavailable/local fallback state where tenant policy allows it.

States:

- Loading tenant.
- Tenant not found.
- Bad credentials.
- MFA required.
- Account locked.
- Password expired.
- SSO failure.
- Tenant suspended.
- Access denied.

Rules:

- Error messages must not reveal whether the email, tenant, or password is valid.
- Login UI must be white-label/theme driven.
- Tenant ID from user input is not treated as authorization proof.

---

# 6. Screen B - Adaptive MFA Challenge

Purpose: ask for additional verification when risk or tenant policy requires it.

Required UI elements:

- MFA challenge title.
- Plain-language reason for step-up verification, such as:
  - New device detected.
  - New location detected.
  - High-risk login.
  - Sensitive administrative operation.
  - Suspicious authentication behavior.
- Verification input for approved factor.
- Recovery or help link where tenant policy allows it.
- Trusted device option where tenant policy permits.
- Retry and cancellation controls.

States:

- Challenge pending.
- Challenge failed.
- Challenge expired.
- Too many attempts.
- Trusted device saved.
- MFA service unavailable.

Rules:

- Risk explanation must be helpful but not expose internal scoring details.
- Trusted device bypass is available only where tenant policy permits.
- Sensitive operations may require MFA even for trusted devices.

---

# 7. Screen C - Break Glass Emergency Login

Purpose: provide controlled emergency administrative access during exceptional operational
scenarios such as identity provider outage, administrator lockout, disaster recovery, or
critical security incident.

Users:

- Authorized emergency operator.
- Platform owner/security operator where approved.

Required UI elements:

- Dedicated emergency login entry point, not mixed into normal login flow.
- Strong warning banner indicating emergency mode.
- Emergency account or emergency role identifier.
- Mandatory business reason.
- Mandatory incident/change reference where applicable.
- Requested scope and duration.
- Approval status panel where maker-checker is required.
- Session expiry countdown after login.
- Persistent emergency-mode visual indicator in the app shell.
- Automatic logout warning before expiry.
- Emergency audit reference after session starts.

States:

- Emergency access disabled.
- Waiting for approval.
- Approved.
- Denied.
- Active emergency session.
- Session expiring soon.
- Session expired and logged out.

Rules:

- Emergency login cannot be hidden as a normal admin shortcut.
- Emergency mode must remain visibly marked throughout the session.
- Emergency session expiration must be visible and enforced.
- All emergency actions link to the break-glass audit record.
- UI must never imply emergency access is a permanent role.

---

# 8. Screen D - Password and Account Recovery

Purpose: provide complete local-auth account recovery flow.

Screens/states:

- Forgot password request.
- Recovery channel confirmation.
- Email or OTP verification.
- New password entry.
- Password policy checklist.
- Password reset success.
- Password reset failure.
- Expired password reset.
- Account locked message.
- Account unlock request.
- Account unlock success/failure.

Required UI elements:

- Email/username input.
- Verification code input.
- New password and confirm password fields.
- Inline password policy feedback.
- Compromised/common-password rejection message.
- Resend code with throttling indicator.
- Back to login action.

Rules:

- Recovery messages must avoid account enumeration.
- Password reset tokens/codes are not displayed after submission.
- Password policy is tenant-configurable but platform minimums must be shown clearly.
- Unlock flow must respect tenant and security policy.

---

# 9. Screen E - Security Dashboard

Purpose: give users visibility into their account security and recent activity.

Required UI elements:

- Last successful login.
- Recent login history.
- Failed login attempts.
- Active sessions summary.
- Security alerts.
- Recent password changes.
- Recent MFA enrollment or changes.
- Suspicious login notifications.
- Quick actions: manage sessions, change password, manage MFA, report suspicious activity.

States:

- No recent activity.
- Security alert present.
- Login history unavailable.
- No permission for certain details.

Rules:

- Approximate location/IP display follows tenant privacy policy.
- Security alerts use clear severity labels and action guidance.
- Dashboard must not expose sensitive internal risk scores.

---

# 10. Screen F - Active Sessions and Devices

Purpose: allow users and authorized admins to manage authenticated sessions.

Required UI elements:

- Active session list.
- Device name.
- Browser.
- Operating system.
- Approximate location where permitted.
- IP address where permitted.
- Created time.
- Last activity.
- Session expiration indicator.
- Current session highlight.
- Remote logout action for individual sessions.
- Logout from all devices action.

States:

- No other sessions.
- Session revoked.
- Revoke failed.
- Session expired.
- Current session cannot be individually revoked without full logout.

Rules:

- Current session must be visually distinguished.
- Global logout requires confirmation.
- Admin session revocation must require permission and audit reason.
- Session data must be tenant-scoped and privacy-filtered.

---

# 11. Screen G - Roles and Permissions

Purpose: let Tenant Admins manage RBAC roles and permission grants without code.

Users:

- Tenant Admin with `Roles.Manage`.

Required UI elements:

- Roles list.
- Clone role.
- Create role.
- Permission matrix.
- Search/filter permissions.
- Module grouping.
- ABAC scope per permission.
- Effective status.
- Audit preview.

Rules:

- System roles are protected from unsafe edits.
- Changes require confirmation and audit.
- Permission grants do not override ABAC policy.
- UI must show that final access is RBAC plus ABAC.

---

# 12. Screen H - ABAC Policy Builder

Purpose: configure attribute-based access scopes as data.

Required UI elements:

- Permission selector.
- Attribute scope builder for branch/office, department, location, business unit, region, manager chain,
  employment type, and custom approved attributes.
- Rule preview.
- Test user/resource simulation.
- Effective date where supported.
- Save draft and publish actions where configuration workflow exists.

Rules:

- Raw rule expressions are not shown to normal admins unless explicitly permitted.
- Policy simulation must not reveal unauthorized data.
- ABAC policy changes emit audit and invalidate authorization caches.

---

# 13. Screen I - Delegation

Purpose: allow scoped, time-boxed delegation.

Required UI elements:

- Delegate user selector.
- Scope selector.
- Valid from/to.
- Reason.
- Active delegation list.
- Revoke action.
- Delegated action visibility in approvals and audit.

Rules:

- Delegation cannot exceed policy maximum duration.
- Delegation cannot grant permissions the delegator does not have.
- Actions performed through delegation show `OnBehalfOf`.

---

# 14. Screen J - Support Impersonation

Purpose: allow platform support to assist a tenant under strict controls.

Required UI elements:

- Target tenant and user.
- Scope.
- Reason.
- Expiry.
- Approval where required.
- Explicit impersonation banner.
- Exit impersonation action.
- Audit reference.

Rules:

- Impersonation is never silent.
- The app shell must show support user, target user, tenant, and expiry.
- Impersonation cannot bypass tenant isolation or ABAC.

---

# 15. Screen K - Identity Security Policies

Purpose: tenant admins configure identity security policies where permitted.

Required UI elements:

- Password policy summary.
- Session expiration policy.
- Concurrent session limit.
- MFA policy.
- Adaptive MFA risk triggers.
- Lockout and retry delay policy.
- Trusted device policy.
- Local fallback policy.

Rules:

- Platform minimums cannot be weakened.
- Changes are audited and versioned.
- High-risk changes may require maker-checker approval.

---

# 16. Accessibility and Responsiveness

Requirements:

- WCAG 2.2 AA target.
- Full keyboard support for login, MFA, recovery, session tables, role matrix, dialogs, and
  emergency screens.
- Screen-reader labels for errors, alerts, MFA reasons, emergency warnings, and countdowns.
- Focus management after failed login, MFA challenge, dialog open/close, and session expiry.
- Non-color-only status indicators.
- Responsive mobile, tablet, and desktop layouts.
- Touch targets at least 44px.
- Localized text for English, Hindi, and Arabic-ready layout.
- No text overflow in buttons, chips, countdowns, banners, or table cells.

---

# 17. Audit and Trust UX

Visible audit/trust elements:

- Last login.
- Login history.
- Active sessions.
- MFA enrollment changes.
- Password changes.
- Delegation and impersonation indicators.
- Break-glass emergency audit reference.
- Session expiry countdown for emergency and impersonation sessions.

Hidden/protected:

- Raw risk scores.
- Password hashes.
- MFA secrets.
- Refresh/access tokens.
- Raw ABAC rule expressions unless explicitly authorized.
- Provider secrets.

---

# 18. Acceptance Criteria

| ID | Criterion |
|---|---|
| UI-IDENTITY-AC-001 | Login supports tenant resolution, local auth, SSO, MFA, password expired, account locked, tenant suspended, and SSO fallback states. |
| UI-IDENTITY-AC-002 | Break Glass Emergency Login has dedicated entry, warning banner, reason/reference, approval state, expiry countdown, emergency app-shell indicator, auto logout, and audit reference. |
| UI-IDENTITY-AC-003 | Adaptive MFA explains step-up reason without exposing internal risk scoring. |
| UI-IDENTITY-AC-004 | Password and account recovery covers forgot password, OTP/email verification, reset, expired password, account unlock, success, and failure states. |
| UI-IDENTITY-AC-005 | Security Dashboard shows last login, login history, failed attempts, sessions, alerts, password/MFA changes, and suspicious activity notifications. |
| UI-IDENTITY-AC-006 | Active Sessions and Devices supports current-session highlighting, device metadata, expiration indicators, individual remote logout, and logout from all devices. |
| UI-IDENTITY-AC-007 | Roles and Permissions supports role clone/create, permission matrix, search, module grouping, ABAC scope, and audit preview. |
| UI-IDENTITY-AC-008 | ABAC Policy Builder supports safe scope configuration, simulation, and cache-invalidating audited publish. |
| UI-IDENTITY-AC-009 | Delegation and impersonation screens enforce scope, expiry, reason, visibility, and `OnBehalfOf` audit behavior. |
| UI-IDENTITY-AC-010 | Identity Security Policies cannot weaken platform minimums and require audit/versioning. |
| UI-IDENTITY-AC-011 | All Identity screens meet accessibility, responsiveness, localization, white-label, and permission-gating requirements. |
| UI-IDENTITY-AC-012 | Branch/office scope assignment screens support complete tenant admin and branch admin use cases. |

---

# 19. Official and Primary References

- WCAG 2.2:
  `https://www.w3.org/TR/WCAG22/`
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

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-28  
UI Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  
Security Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  
Accessibility Reviewer: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  
Solution Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28  
QA Architect: Approved as part of owner-approved Identity + RBAC/ABAC package 2026-06-28

(Status: Approved - owner approved 2026-06-28)
