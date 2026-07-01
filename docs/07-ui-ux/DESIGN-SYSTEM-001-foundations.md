# Design System — Foundations

Document Owner: UI Architect (Agent 11) + UX Researcher (Agent 10)
Created Date: 2026-06-14
Version: 1.0
Status: Approved (Bhajan Lal, 2026-06-14)

> The shared design language for every screen. Implements `UI_STANDARDS.md`
> (mobile-first, WCAG, theme-driven, white-label, localization) and
> `CODING_STANDARDS_REACT.md` (React/Next/TS, MUI, design-system-based). Per-screen specs
> reference these tokens/components instead of redefining them.

---

# 1. Design Principles

1. **One screen, one purpose** — avoid clutter (UI_STANDARDS).
2. **Mobile-first, responsive** — Mobile / Tablet / Desktop all mandatory.
3. **≤ 3 clicks** to any major function.
4. **Theme-driven, zero hardcoded colors** — every color/logo/brand is a token (white-label).
5. **Accessible by default** — WCAG 2.1 AA, keyboard + screen reader.
6. **Localized by default** — EN / HI at launch, AR (RTL) ready; no hardcoded text.
7. **Config-driven UI** — lists, forms, dashboards are rendered from metadata where
   possible (supports the no-code platform).

---

# 2. Personas → UX priorities

| Persona | Primary surface | UX priority |
|---|---|---|
| Priya (HR Ops) | Desktop console | Density, bulk actions, accuracy, audit |
| Rohan (Manager) | Mobile + desktop | Fast approvals, team insight, minimal taps |
| Anita (Employee) | Mobile-first ESS | Simplicity, self-serve, AI assistant |
| Sameer (Tenant Admin) | Desktop config | Power tools (Workflow Studio), safe sandbox |

---

# 3. Design Tokens — "Modern & Friendly" default theme

Approved visual direction (2026-06-14): **Modern & friendly** — airy whitespace, vibrant
indigo accent, rounded cards, soft shadows. See the live prototype in `prototype/index.html`.
These are the **default** values; every one is per-tenant overridable for white-label.

```
-- Color (default theme) --
accent          #6366F1   accent-600  #4F46E5   accent-soft #EEF1FF
brand-gradient  linear-gradient(135deg,#6366F1 → #8B5CF6)
success #10B981 / soft #E7FBF3     warning #F59E0B / soft #FEF4E2
danger  #EF4444 / soft #FDECEC     info = accent
text    #0F172A   muted #667085   faint #94A3B8   inverse #FFFFFF
surface #FFFFFF   canvas #F6F7FB   border #ECEEF3

-- Type --   font: Inter, system-ui fallback (locale-aware, RTL-safe)
             scale h1 23 / h3 15 / body 14 / caption 12, tight letter-spacing on headings

-- Space --  8pt grid: 4 8 12 16 20 24 32 48
-- Radius -- sm 10 · md 12 · lg/card 16 · pill 20
-- Elevation -- shadow 0 6px 20px rgba(16,24,40,.06) ; shadow-lg for modals/phone
-- Breakpoints -- xs<600 · sm 600 · md 900 · lg 1200 · xl 1536
-- Motion -- fast 150ms / normal 250ms, ease-out; respect reduced-motion
```
Tokens resolve from **tenant theme → default theme**; components never hardcode values.

**Density modes** (token-driven, instant switch): `--pad / --gap / --fs / --rowpad` shift
across **Comfortable · Compact · Dense** (`[data-density]`).
**Dark theme** (`[data-theme="dark"]`): re-tuned, not inverted — surface #161A24, card
#1B2030, border #262C3B, soft accent #22264A, depth-adjusted shadows.
See `DESIGN-SPEC-002` for the AI-native platform components (widget grid, command palette,
AI panel, workflow canvas, rule builder, audit diff, compliance/payroll cockpits).

---

# 4. Core Components (MUI-based, design-system wrapped)

- **Navigation:** AppShell (top bar + collapsible side nav), TenantSwitcher, Breadcrumbs,
  CommandPalette (power users).
- **Data:** DataTable (sort, filter, pagination, column-select, export — per UI_STANDARDS),
  KpiCard, Chart, EmptyState, Skeleton/Loader.
- **Forms:** Form (React Hook Form + Zod), Field set (Text/Select/Date/Toggle/File),
  inline validation, helpful errors, Save-as-draft.
- **Feedback:** Toast, Dialog/Confirm, Banner, InlineError, ProgressStepper.
- **Workflow:** ApprovalCard, Timeline/AuditTrail, StatusChip, SLAIndicator.
- **Platform:** FeatureFlagGate, PermissionGate (RBAC/ABAC-aware), LocaleProvider,
  ThemeProvider.

All components: keyboard-navigable, ARIA-labeled, RTL-safe, token-styled.

---

# 5. Navigation Model

```
 Top bar:  [Logo*]  [TenantSwitcher]  [Global search]      [Locale] [Notifications] [Profile]
 Side nav: Dashboard · My Stuff (ESS) · People · Leave · Attendance · Payroll
           · Workflows* · Reports · Admin/Settings*   (*permission/flag gated)
 Content:  Breadcrumb ▸ Page title ▸ One primary action (top-right) ▸ Body
```
Nav items render from **entitlements + permissions** (a tenant only sees enabled modules).

---

# 6. Accessibility (WCAG 2.1 AA)

- Full keyboard operation; visible focus; logical tab order.
- Screen-reader labels, roles, live regions for async updates.
- Color contrast ≥ 4.5:1; never color-only signaling (pair with icon/text).
- Forms: label + description + error association (`aria-describedby`).
- Respect reduced-motion.

---

# 7. White-Label & Theming

- Per-tenant: logo, brand colors, font, custom domain, email templates.
- Resolved at load from tenant config; falls back to platform default.
- No tenant CSS injection (security) — theming is token-based only.

---

# 8. Localization & Formatting

- i18n message catalogs (EN/HI now, AR-ready); **no hardcoded strings**.
- Locale-aware dates/numbers/currency; **RTL layout** mirroring for Arabic.
- Per-user locale + per-tenant default; time-zone-aware display (ARCH-REVIEW §5).

---

# 9. Responsive Patterns

- Tables → cards on mobile; side nav → bottom nav / drawer.
- Primary actions stay reachable (sticky action bar on mobile).
- Touch targets ≥ 44px.

---

# 10. UX Writing & States

Every screen defines: **loading**, **empty**, **error**, **no-permission**, and
**success** states. Messages are plain, action-oriented, and localized.

---

## Approval

UI Architect: ____ · UX Researcher: ____ · Product Owner: ____ · Accessibility: ____
(Status: Draft → Approved)
