# UI Screen Specs — Foundational Screens (Phase 7A)

Document Owner: UI Architect (Agent 11) + Figma Designer (Agent 12)
Created Date: 2026-06-14
Version: 1.0
Status: Approved (Bhajan Lal, 2026-06-14)

> Key screens for Sprint S1–S5. Each follows `docs/19-templates/UI_SCREEN_TEMPLATE.md`
> and the design system (DESIGN-SYSTEM-001). Wireframes are low-fi ASCII; high-fidelity
> Figma follows after approval. All screens are PermissionGate/FeatureFlag aware,
> responsive, WCAG-AA, localized, theme-driven.

---

# Screen 1 — Login + Tenant Resolution

**Purpose:** authenticate; resolve tenant (by domain or selection); SSO or local.
**Users:** all. **APIs:** `POST /auth/login`, `GET /auth/sso/{tenant}` (ADR-008).

```
        ┌──────────────────────────────────┐
        │            [Tenant Logo*]         │
        │        Sign in to {TenantName}    │
        │  ┌────────────────────────────┐   │
        │  │ Email                      │   │
        │  └────────────────────────────┘   │
        │  ┌────────────────────────────┐   │
        │  │ Password            [show] │   │
        │  └────────────────────────────┘   │
        │  [ Sign in ]                       │
        │  ──────────  or  ──────────        │
        │  [ Continue with SSO ]             │
        │  Forgot password?   MFA if enabled │
        └──────────────────────────────────┘
```
**Validations:** email format; lockout after N attempts; MFA challenge.
**Errors:** invalid creds (generic msg), tenant suspended, SSO failure → local fallback.
**States:** loading, error, MFA-required, account-locked.

---

# Screen 2 — Employee Directory (People)

**Purpose:** browse/search employees; entry to profile.
**Users:** HR, Manager (ABAC-scoped to their org). **Permissions:** People.View.
**APIs:** `GET /employees?search&filter&sort&page` (effective-dated, as-of today).

```
 People ▸ Directory                                   [ + Add Employee ]
 ┌───────────────────────────────────────────────────────────────────┐
 │ [search…]  Dept ▾  Location ▾  Status ▾        [columns] [export]  │
 ├──────┬───────────────┬────────────┬────────────┬──────────┬───────┤
 │ Photo│ Name (ID)     │ Designation│ Department │ Manager  │ Status│
 ├──────┼───────────────┼────────────┼────────────┼──────────┼───────┤
 │  ◐   │ Anita R (1042)│ Engineer   │ Platform   │ Rohan K  │ Active│
 │  ◐   │ …             │ …          │ …          │ …        │ …     │
 ├──────┴───────────────┴────────────┴────────────┴──────────┴───────┤
 │              ◀ 1 2 3 … ▶     rows: 25 ▾     1–25 of 612            │
 └───────────────────────────────────────────────────────────────────┘
```
**Manager view:** ABAC filters to their department only (no toggle).
**Mobile:** rows collapse to cards. **States:** loading skeleton, empty, no-permission.

---

# Screen 3 — Apply Leave (ESS, mobile-first)

**Purpose:** employee submits leave; triggers Workflow approval.
**Users:** Employee. **APIs:** `GET /leave/balances`, `POST /leave/requests`
(rules via Rule Engine FR-013; routing via Workflow FR-007).

```
 ┌─────────────────────────────┐
 │  Apply Leave                │
 │  Balance: Casual 6 · Sick 4 │
 │  Type   [ Sick ▾ ]          │
 │  From   [ 16 Jun ]  ½?[ ]   │
 │  To     [ 18 Jun ]          │
 │  Days   3   (auto)          │
 │  Reason [____________]      │
 │  ⚠ Sick > 5d needs HR (rule)│  ← live Rule Engine feedback
 │  [ Save draft ] [ Submit ]  │
 └─────────────────────────────┘
```
**Validations:** balance check, overlap check, min-notice — all **rules-as-data**.
**On submit:** workflow instance starts; show approval chain preview.
**States:** insufficient-balance, overlap-error, submitted (with tracker).

---

# Screen 4 — Approvals Inbox (Manager/HR)

**Purpose:** act on pending approvals (leave, regularization, etc.) from any module.
**Users:** approvers + delegates. **APIs:** `GET /workflow/tasks?assignee=me`,
`POST /workflow/tasks/{id}/decision`. Delegation + SLA per ADR-010.

```
 Approvals  (3 pending)                         acting as: [Me ▾ / Delegate]
 ┌───────────────────────────────────────────────────────────────────┐
 │ ⏳ Leave · Anita R · Sick 3d (16–18 Jun)        SLA: 6h  [▼]        │
 │     Balance ok · Step 1/2 (you) → HR            [Approve] [Reject] │
 │     [ comment… ]                                                   │
 ├───────────────────────────────────────────────────────────────────┤
 │ ⏳ Regularization · …                            SLA: ⚠ 1h         │
 └───────────────────────────────────────────────────────────────────┘
```
**Delegation:** if acting as delegate, banner + audit `OnBehalfOf`.
**SLA:** color indicator; breach → escalation (config).
**Bulk:** select-all approve (with confirm). **States:** empty ("all caught up").

---

# Screen 5 — Workflow Studio (Tenant Admin) ⭐ differentiator

**Purpose:** no-code builder for approval chains/conditions/SLAs. **Users:** Tenant Admin
(Workflows.Manage). **APIs:** `GET/POST /workflow/definitions` (versioned, ADR-010);
conditions reference Rule Engine (ADR-011). **Sandbox→prod** promotion (ARCH-REVIEW §1B).

```
 Workflows ▸ Leave Approval            v3 (draft)   [Validate] [Save] [Publish ▾]
 ┌─────────────┬───────────────────────────────────────┬──────────────────────┐
 │ Palette     │            Canvas                      │  Properties          │
 │ • Approval  │   ┌─────┐   cond:days>5   ┌────────┐   │  Step: HR Approval   │
 │ • Decision  │   │Start│──────────────►──│Manager │   │  Approver: Role ▾    │
 │ • Parallel  │   └─────┘                 └───┬────┘   │  SLA: [ 8h ]         │
 │ • Notify    │                  ┌───────┐    ▼        │  Escalation: Notify+ │
 │ • Wait/SLA  │                  │  HR    │──►(End)     │   reassign ▾         │
 │ • Action    │                  └───────┘             │  Condition: [rule…]  │
 └─────────────┴───────────────────────────────────────┴──────────────────────┘
   Env: [ Sandbox ]   Test with sample data ▶        Versions: v1 v2 ●v3
```
**Validate:** connected graph, reachable End, resolvable rules (publish-time, ADR-010).
**Publish:** creates immutable v+1; running instances stay on their version; live-migrate
requires approval. **States:** invalid-graph (inline markers), unsaved-changes guard.

---

# Cross-cutting (all screens)

- **Permission/flag gating:** hidden if not entitled; 403 view if deep-linked.
- **Audit:** every mutating action emits audit (FR-008) + may emit an event (FR-009).
- **Responsive/A11y/i18n/theme:** per DESIGN-SYSTEM-001.
- **Empty/loading/error/no-permission** states defined for each.

---

## Approval

UI Architect: ____ · UX Researcher: ____ · Product Owner: ____ · .NET Architect (API): ____
(Status: Draft → Approved)
