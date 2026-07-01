# UI Design - Tenant Catalog and Administration

Feature Name: Tenant Catalog and Isolation
Requirement ID: FR-015
Module: Platform / Core
Owner: UI Architect
Created Date: 2026-06-14
Last Updated: 2026-06-27
Version: 1.1
Status: Approved

> Doc 4 of 5 required before implementation. Companion docs:
> FEAT-TENANT-001, TECH-TENANT-001, DB-DESIGN-TENANT-001, TEST-TENANT-001.
> No Tenant Catalog or RLS implementation may start until all five documents are Approved.

---

# 1. Purpose

This document defines the tenant administration and platform-owner screens for FR-015.
Most tenant isolation enforcement happens server-side and in the database. The UI must
surface the configuration, lifecycle, and evidence needed to operate tenant isolation
safely without making the experience noisy for normal tenant users.

The UI is operational, dense, permission-gated, and audit-aware.

---

# 2. Design Inputs

- `DESIGN-SYSTEM-001-foundations.md`
- `DESIGN-SPEC-002-people-ops-platform.md`
- `FEAT-TENANT-001-business-requirements.md`
- `TECH-TENANT-001-technical-design.md`
- `DB-DESIGN-TENANT-001.md`
- `TEST-TENANT-001-test-plan.md`
- `SEC-DESIGN-001-threat-model.md`

---

# 3. Personas

| Persona | Primary Need |
|---|---|
| Platform Owner | Provision, suspend, activate, offboard, and monitor tenants. |
| Platform Operator | Inspect tenant placement, health, and isolation evidence. |
| Security Reviewer | Review tenant lifecycle actions, audit, and isolation proof. |
| Tenant Administrator | Manage company profile, locations, localization, and allowed setup. |
| Employee/Manager | See only their tenant experience; no tenant-switching noise unless authorized. |

---

# 4. Navigation

Platform-owner area:

- Tenants
- Provision Tenant
- Tenant Details
- Placement
- Entitlements
- Branding and Domains
- Lifecycle and Audit
- Isolation Evidence

Tenant-admin area:

- Company Profile
- Branches / Offices
- Locations
- Localization
- Working Calendar
- Branding where permitted
- Feature Availability where permitted

Normal tenant users do not see platform tenant registry or tenant lifecycle controls.

---

# 5. Screen A - Platform Tenant Registry

Purpose: list and monitor all tenants for platform-owner users.

Users:

- Platform Owner
- Platform Operator
- Security Reviewer with read-only permission

Required UI elements:

- Tenant table with name, code, tenant ID, status, plan, region, placement, shard,
  primary domain, last activity, and health indicator.
- Filters for status, region, placement, plan, and entitlement group.
- Search by tenant name, tenant code, custom domain, and tenant ID.
- Actions: View, Provision, Suspend, Activate, Offboard, Change Placement.
- Export list action only for authorized platform roles.

States:

- Loading.
- Empty.
- No permission.
- Partial catalog health degraded.
- Suspended tenant.
- Offboarding tenant.

Rules:

- Dangerous actions are not table-row one-click actions; they open governed workflows.
- Tenant IDs can be copied only by authorized roles.
- Raw connection strings and secrets are never displayed.

---

# 6. Screen B - Tenant Provisioning Wizard

Purpose: create a tenant in a controlled, auditable flow.

Steps:

1. Tenant identity: legal name, display name, code, primary country, admin contact.
2. Region and placement: region, shard, pooled/dedicated, data residency note.
3. Plan and entitlements: module groups, feature flags, quotas.
4. Branding and domains: company logo reference, custom domain, email domain status.
5. Provider defaults: provider references only, no raw secrets.
6. Review and submit: summary, validation errors, audit reason.

Required states:

- Draft.
- Validating.
- Provisioning.
- Provisioned.
- Failed with retry.
- Requires approval.

Rules:

- Tenant code must be immutable after activation unless a separate approved migration
  workflow exists.
- The wizard must show that placement is configuration and does not require deployment.
- Provisioning cannot activate until required database, identity, and catalog checks pass.

---

# 7. Screen C - Tenant Detail

Purpose: show the trusted tenant profile and operational state.

Required panels:

- Profile: tenant name, code, tenant ID, status, plan, country, locale, currency, timezone.
- Placement: region, shard, placement type, database reference, storage/search/cache scope.
- Entitlements: enabled/disabled modules and feature groups.
- Branding: logo reference, theme, custom domains, email domain verification.
- Provider configuration summary.
- Lifecycle timeline.
- Audit trail summary.

Rules:

- Secret references may be visible only as masked references to authorized platform users.
- Tenant-admin view hides platform-only placement and provider details unless explicitly
  permitted.

---

# 8. Screen D - Tenant Administration

Purpose: tenant admin manages company setup inside their own tenant.

Users:

- Tenant Administrator

Required UI elements:

- Company profile.
- Business units.
- Departments.
- Branches/offices.
- Locations.
- Working days and holidays entry point.
- Fiscal year.
- Country, language, timezone, currency.
- Contact details.

States:

- Loading.
- Saved.
- Validation failed.
- No permission.
- Tenant suspended.

Rules:

- Tenant admins cannot change tenant ID, placement, shard, region, platform plan, or
  platform provider configuration.
- All changes are audited and tenant-scoped.

---

# 9. Screen E - Entitlements and Feature Flags

Purpose: configure which modules/features are available to a tenant.

Users:

- Platform Owner
- Tenant Administrator where delegated by platform policy

## Phase 7A Branch / Office Addendum

Tenant Administration UI must comply with `docs/07-ui-ux/UI-BRANCH-001-screens.md`.
Complete tenant administrators can see all branches/offices; branch administrators see
only assigned branch/office scope.

Required UI elements:

- Feature/module list grouped by platform area.
- Status: Enabled, Disabled, Beta, ReadOnly, Hidden.
- Effective date.
- Dependency warnings.
- Impact preview: navigation, APIs, jobs, reports, integrations.
- Save as draft and publish controls where configuration workflow exists.

Rules:

- UI flag changes cannot override server-side authorization.
- Disabling a module must show "access blocked, data retained" messaging.
- Feature changes emit audit and invalidation events.

---

# 10. Screen F - Placement and Region

Purpose: inspect and change tenant placement safely.

Users:

- Platform Owner
- Platform Operator

Required UI elements:

- Current placement type: pooled, shard, dedicated database.
- Current region.
- Shard/database reference.
- Capacity and health summary.
- Change placement workflow.
- Required evidence checklist.
- Maintenance window.
- Rollback target.

Rules:

- Placement change is disabled until migration evidence exists.
- The UI must clearly show that code deployment is not required.
- Users must provide reason and approval reference.

---

# 11. Screen G - Lifecycle Actions

Purpose: activate, suspend, reactivate, or offboard a tenant.

Required UI elements:

- Action selector.
- Reason code.
- Effective date/time.
- Required approval status.
- Impact summary.
- Confirmation text.
- Audit evidence link.

Suspension impact summary must include:

- User login/API access.
- Background jobs.
- Integrations.
- Reports/exports.
- AI/search where applicable.

Offboarding impact summary must include:

- Export.
- Legal hold.
- Retention.
- Purge schedule.
- Final evidence.

Rules:

- Offboarding is not reversible once purge has passed the reversible window defined by
  retention policy.
- Activation after suspension requires health validation.

---

# 12. Screen H - Isolation Evidence

Purpose: show security and QA evidence that tenant isolation is active.

Users:

- Security Reviewer
- Platform Owner
- QA Reviewer

Required UI elements:

- RLS policy status.
- Latest isolation test run.
- Tenant-scoped table coverage.
- Query filter coverage.
- RLS block predicate coverage.
- Cache/search/storage namespace coverage.
- Last tenant mismatch denial count.
- Links to test evidence and audit events.

Rules:

- Evidence is read-only.
- Missing RLS coverage is a blocking red status.
- The UI does not expose another tenant's data while demonstrating isolation.

---

# 13. Suspended Tenant User Experience

When a tenant is suspended, tenant users see a clear access suspended state after login or
when refreshing an existing session.

The screen includes:

- Neutral suspension message.
- Contact instruction controlled by tenant/platform policy.
- No internal reason details unless policy allows.
- No access to tenant data.

---

# 14. Accessibility and Responsiveness

Requirements:

- WCAG 2.2 AA target.
- Keyboard support for tables, filters, dialogs, wizard steps, confirmations, and tabs.
- Focus states and semantic headings.
- Non-color-only status indicators.
- Screen-reader labels for status, placement, and dangerous action warnings.
- Responsive layouts for desktop and tablet; platform registry may require horizontal
  table behavior but must remain usable.
- No text overflow in buttons, chips, status labels, or table cells.

---

# 15. Audit and Trust UX

Show:

- Who initiated lifecycle change.
- Reason code.
- Approval status.
- Effective date/time.
- Impact summary.
- Evidence reference.

Do not show:

- Raw connection strings.
- Raw provider secrets.
- Cross-tenant data.
- Internal database credentials.
- Unauthorized tenant IDs or domains.

---

# 16. Acceptance Criteria

| ID | Criterion |
|---|---|
| UI-TENANT-AC-001 | Platform Tenant Registry supports filtering, searching, and viewing tenant status, region, placement, and health. |
| UI-TENANT-AC-002 | Provisioning wizard captures tenant identity, region, placement, entitlements, branding, provider references, and review summary. |
| UI-TENANT-AC-003 | Tenant Detail separates tenant-admin-safe information from platform-only placement/provider details. |
| UI-TENANT-AC-004 | Tenant admins can manage company setup but cannot modify platform placement, shard, or tenant ID. |
| UI-TENANT-AC-005 | Entitlement screen shows module impact across navigation, APIs, jobs, reports, and integrations. |
| UI-TENANT-AC-006 | Placement changes require evidence, reason, approval reference, maintenance window, and rollback target. |
| UI-TENANT-AC-007 | Suspension/offboarding flows show impact summary and require confirmation, reason, and audit. |
| UI-TENANT-AC-008 | Isolation Evidence screen shows RLS, query-filter, table-coverage, and namespace evidence without exposing tenant data. |
| UI-TENANT-AC-009 | Suspended tenant users see a safe blocked-access state with no data exposure. |
| UI-TENANT-AC-010 | All screens meet accessibility, responsiveness, permission gating, and audit UX requirements. |

---

# 17. Official and Primary References

- Microsoft Azure Architecture Center - tenancy models:
  `https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models`
- Microsoft Azure Architecture Center - map requests to tenants:
  `https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/map-requests`
- OWASP API1:2023 Broken Object Level Authorization:
  `https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/`
- WCAG 2.2:
  `https://www.w3.org/TR/WCAG22/`

References last validated: 2026-06-27.

---

# Approval

Product Owner: Approved by Bhajan Lal 2026-06-27  
UI Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Security Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Accessibility Reviewer: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
Solution Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27  
QA Architect: Approved as part of owner-approved Tenant Catalog + RLS package 2026-06-27

(Status: Approved - owner approved 2026-06-27)
