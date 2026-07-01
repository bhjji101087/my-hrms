# Design Spec — AI-Native People Operations Platform (v2)

Document Owner: Sr. Product Designer / Enterprise UX Architect (Agents 10–12)
Created Date: 2026-06-14
Version: 2.1
Status: Approved (Bhajan Lal, 2026-06-14; Phase 4 alignment refresh 2026-06-18)

> Evolves DESIGN-SYSTEM-001 + SCREENS-001 into a platform-grade experience that reads as
> **"AI-powered People Operations Platform"**, not "an HRMS with modules". Preserves the
> existing visual identity (indigo/violet, spacing, Inter, rounded cards). The interactive
> reference is `prototype/index.html`. Benchmarks: Darwinbox, Keka, BambooHR, Linear,
> Notion, Atlassian. Implements ARCH-REVIEW-001 + the approved engines (Workflow/Rules/
> Audit/Tenant). Phase 4 alignment refresh adds explicit provider-management UX for
> ADR-027. Nothing in the UI is hardcoded — nav, dashboards, modules, integrations, and
> provider settings are **metadata-driven**.

---

## 0. Component Hierarchy (information architecture)

```
AppShell
├── Sidebar (metadata-driven: role × tenant × feature-flag)
│   ├── BrandBlock (white-label)
│   ├── NavGroup[] → NavItem[] (icon, label, badge, AI-tag, entitlement)
│   └── ContextFooter
├── TopBar
│   ├── TenantSwitcher           ├── CommandTrigger (⌘K)
│   ├── DensitySegmented          ├── ThemeToggle (light/dark)
│   ├── NotificationBell→Center   ├── RoleContext   └── UserMenu
├── ScreenRouter
│   ├── Dashboard (WidgetGrid → Widget[] : configurable/reorder/hide/role-driven)
│   ├── People · Leave · Approvals
│   ├── WorkflowStudio2 (Palette · Canvas · Inspector · Tabs)
│   ├── RuleBuilder (ConditionTree · TestSandbox · ImpactPanel)
│   ├── AuditCenter (Timeline · DiffView · Filters)
│   ├── ActivityCenter (UnifiedFeed · Filters)
│   ├── ComplianceCenter · PayrollControlTower · OrgChart
├── CommandPalette (overlay, fuzzy, actions + AI)
├── AIAssistant (FAB + SlidePanel, persistent)
└── Overlays (NotificationCenter, Dialogs, Toasts)
```
Every list/grid/form is rendered from **metadata** (definition objects), enabling no-code
tenant configuration — the prototype demonstrates this with `ROLES`, `W` (widgets), and
`CMDS` maps.

---

## 1. Role-Based Dynamic Dashboard

A **widget grid** (12-col) populated from `role → widgets[]` metadata. Widgets are
**configurable, reorderable, hideable, role-driven, tenant-configurable**. "Customize"
mode reveals drag handles + hide controls; "Add widget" opens a catalog.

| Role | Widgets |
|---|---|
| Employee | Leave balance · Attendance · Holidays · Payslip · Announcements · AI |
| Manager | Team attendance · Approvals · Team leave calendar · SLA alerts · Birthdays · AI |
| HR | Headcount · Joiners/Exits · Approval queue · Compliance · Attendance trend · AI |
| Payroll | Payroll health · Statutory · Exceptions · Attendance trend |
| Admin | Tenant health · User activity · Workflow failures · Integrations · Audit · AI |

```
┌ Greeting + [Customize][+ Add widget] ───────────────────────────┐
│ [KPI][KPI][KPI][KPI]                                            │
│ [ Approval queue        s6 ][ Compliance gauge s3 ][ Trend s3 ] │
│ [ ✨ AI insight (full-width, actionable)            s12       ] │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Dynamic Navigation System

Sidebar is generated from metadata: **modules × feature flags × role visibility ×
tenant entitlement × white-label**. Tenant A sees {Dashboard, People, Leave, Payroll};
Tenant B sees {Dashboard, People, Assets, Recruitment, Learning} — **no deployment**.
AI-enabled modules carry an `AI` tag. (Prototype: `renderNav()` from `ROLES[role].nav`.)

## 3. Global Command Center (⌘K)

Linear/Notion-style palette: fuzzy **search** (employee, workflow, report, policy, leave),
**quick actions** (create employee, apply leave, run payroll, create workflow, generate
report), and **AI commands** ("show employees absent today", "generate attrition report").
Keyboard-first; every action reachable in ≤2 keystrokes. (Prototype: ⌘K works.)

## 4. AI-Native Experience

Persistent **"Ask HR AI"** FAB + slide-in panel everywhere — a built-in coworker, not a
buried feature. Capabilities: leave/payroll/policy Q&A (RAG with **source citations**),
employee lookup, report generation, workflow generation. AI also surfaces **proactively**
as dashboard insight cards and payroll anomaly detection. Guardrails: tenant-scoped RAG,
respects RBAC/ABAC, no cross-tenant data, actions are audited.

## 5. Dashboard Insights Layer

Every chart answers a business question (no decorative charts): **Payroll Health**,
**Compliance Health** (gauge/score), **Approval SLA status**, **Workforce trends**,
**Attendance heatmap**. KPI cards show trend deltas, not vanity numbers.

## 6. Workflow Studio 2.0

```
[Design | Versions | History | Usage analytics]
┌ Nodes ─┬─ Canvas (pan/zoom/minimap, dotted grid) ─┬─ Inspector ─┐
│Approval│   ●Start →⎇cond→ Manager → HR → ■End     │ Approver    │
│Decision│            ↘ ⏱SLA→↥escalate              │ SLA / breach│
│Condition│  [minimap]                  [− ⊡ +]     │ Condition→  │
│Parallel│                                          │  Rule Engine│
│Notify/Wait/Escalation/Action/API Call/Sub-workflow│ Version pin │
└────────┴──────────────────────────────────────────┴─────────────┘
```
Node types: Approval, Decision, Condition, Parallel, Notify, Wait, Escalation, Timer,
Action, **API Call**, **Sub-workflow**. Canvas: zoom, pan, **minimap**, publish-time
**validation**, **draft/publish**, **version pinning** of running instances (ADR-010).
Tabs expose **versions, history, usage analytics**. HR-friendly but Power-Automate-grade.

## 7. Rule Builder

Dedicated visual IF/THEN builder with **rule groups + nested conditions** (ALL/ANY),
a **test sandbox** (run sample input → see outcome), **versioning**, and **impact
analysis** ("applies to 312 employees · referenced by 4 workflows"). Examples: leave
routing, location→PT rule, salary→PF optional. Backed by ADR-011 (JSON-AST, no code).

## 8. Audit & Time Machine

Audit Center with **Timeline view** + **Diff view** (old vs new value, side-by-side) +
filters (entity/actor/date/action). Each entry: who, what, old→new, when, why, correlation
ID. Tamper-evident (ADR-024). Example rendered: Salary ₹50,000 → ₹60,000 by Priya,
reason "Promotion".

## 9. Enterprise Activity Center

Unified, filterable, exportable feed across Approvals, Payroll, Compliance, Workflow,
Employee events — the single "what happened" stream.

## 10. Compliance Command Center

**Compliance score (0–100)** gauge + per-statute status (PF/ESI/PT/LWF/TDS) + **proactive
warnings** (upcoming deadlines, failed filings, missing employee data). Predictive, not
reactive — the validated differentiator.

## 11. Payroll Control Tower

Run-progress stepper (Inputs→Calc→Validation→Approval→Disburse), exceptions/warnings
counters, and **AI anomaly detection** (e.g., "salary ₹50,000 → ₹5,00,000 — likely error";
"₹0 net pay — missing bank details"). A cockpit, not a form.

## 12. Data Density Modes

Instant **Comfortable / Compact / Dense** toggle (token-driven: `--pad/--gap/--fs/--rowpad`).
Enterprise users get dense tables without losing the friendly aesthetic. (Prototype: works.)

## 13. Organization Visualization

Interactive **org chart / reporting hierarchy / department tree** with drill-down. Built on
the effective-dated org model (ADR-007) and multi-legal-entity reservation.

## 14. Notification Center

Unified panel, categorized (Approvals/Payroll/Compliance/Workflow/System), with
**read/unread, pin, snooze**. Driven by the event backbone (ADR-009).

## 15. Delegation Framework

First-class **acting-manager / proxy approver / temporary delegation**. The approvals
surface shows an "acting as" context; every delegated action is audited as `OnBehalfOf`
(security schema + ADR-008).

## 16. Modern Visual Improvements

Keep spacing/typography/palette; improve **data density, visual hierarchy, enterprise
depth**. Replace empty whitespace with meaningful business info (insight cards, mini-charts,
status). Cards gain subtle depth; headers use the brand gradient sparingly.

## 17. Accessibility

WCAG 2.1 AA: full keyboard nav (⌘K, focus rings, logical order), screen-reader roles/
labels/live-regions, contrast ≥ 4.5:1, never color-only signaling, **high-contrast** option,
reduced-motion respected.

## 18. Dark Mode

Enterprise dark theme via token override (`[data-theme="dark"]`) — **not** an inversion:
re-tuned surfaces (#161A24/#1B2030), borders, soft accent, and shadow values for depth and
comfort. (Prototype: toggle works.)

## 19. Responsive Design (purpose-built per breakpoint)

- **Desktop:** full shell, 12-col widget grid, three-pane Workflow Studio.
- **Tablet:** collapsible sidebar (icons), 2-col widgets, stacked inspector.
- **Mobile:** bottom nav, single-column cards (tables→cards), sticky primary action,
  full-screen Apply-Leave/Approve flows, AI as full-screen sheet. **Not** mere stacking —
  flows are redesigned for touch.

## 20. Final Objective — measured

The product should read as an **AI-powered People Operations Platform** with Workflow
Automation, Compliance Intelligence, Payroll Control, and Enterprise Configurability.
UX success checks: (a) a non-technical admin reconfigures a dashboard/nav/workflow with no
code; (b) AI is reachable on every screen; (c) every chart answers a business question;
(d) dense + dark modes available; (e) nothing hardcoded.

---

## 21. Configurability Screens (Phase-1 vision proof)

To make "configurable, no-code, multi-tenant" *visible* to a CHRO/CIO/investor, the
prototype adds a **Configuration Center** (the heart) linking to admin-configured surfaces.
All are no-code, per-tenant, no deployment. **No future modules** (no ATS/PMS/LMS/etc.).

| Screen | Proves | Key UX |
|---|---|---|
| **Configuration Center** | "Configured by admin, no developer" | Tile grid → Forms/Workflows/Rules/Roles/Flags/Nav/Branding/Tenant/Integrations |
| **Form Builder** | Form engine / no-code | Field-type palette → drag canvas → field properties + required toggle |
| **Role & Permission Builder** | RBAC + ABAC | Role list · permission matrix (✓/✗) · ABAC scope · clone/create |
| **Tenant Administration** | Multi-tenant SaaS | Profile (ID/plan/status/region) · BU/Dept/Location · working days/fiscal · localization/country |
| **Feature Management** | Modular architecture | Enabled/Disabled/Beta toggles; future modules shown disabled |
| **Integration Hub** | Enterprise connectivity | Connector cards w/ Connected/Pending/Disconnected + last sync/health |
| **Provider Management** | Provider-abstraction framework | Category tabs (Storage/Cache/Messaging/Email/SMS/Push/Identity/Search/Reporting/LLM), primary/fallback provider, capability flags, health, test connection, sandbox→prod promotion |
| **Navigation Builder** | Dynamic nav | Drag/hide/rename per role & tenant; Tenant A vs B example |
| **Branding & White-Label** | Reseller/enterprise | Logo, colors, theme, custom domain, email branding + live preview |
| **Global Search results** | Discoverability | Grouped results (Employee/Leave/Workflow/Report) |
| **Widget Catalog** | Metadata dashboards | Toggle widgets on/off, reorder, per role & tenant |
| **AI Settings (admin-only)** | Model-agnostic AI | Provider registry selection + model-per-use-case + fallback; `AI.ManageModels` only (ADR-019 / AI-STRATEGY-001 §8) |

Provider Management is admin-only, permission-gated, and audited. Secrets are entered only
through secure references or guided connection setup; raw secrets are never shown after
save. Every provider change must support validate/test-connection, health status,
fallback visibility, effective date, and promotion from sandbox to production.

Plus enhancements: **Workflow Studio** now renders connected execution paths (branch /
success / SLA-escalation arrows, version + draft badge); **Org Chart** is an interactive
expand/collapse tree with search, count badges, and a detail panel; **AI Copilot**
responses now include a *Recommended Actions* row.

---

## UX Recommendations (priorities for build)

1. **Metadata-first**: ship the widget/nav/command registries before module screens — they
   are the configurability moat.
2. **AI as a layer, not a page**: one assistant service surfaced via FAB + insight cards +
   palette, all RBAC/RAG-scoped.
3. **Workflow Studio is the hero** — invest in canvas UX (pan/zoom/minimap/validation).
4. **Performance budget**: P95 < 2s; virtualize dense tables; lazy-load heavy canvases.
5. **Design tokens own theming/density/dark** — no component hardcodes values (white-label).

---

## Approval

UX Architect: ____ · UI Architect: ____ · Product Owner: ____ · Solution Architect: ____
· Accessibility: ____  (Status: Draft → Approved)
