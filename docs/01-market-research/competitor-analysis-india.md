# Market Research — HRMS Competitor Analysis (India-First)

Document Owner: HR Domain Expert (Agent 1)
Created Date: 2026-06-14
Version: 1.3 (Phase 1 refresh)
Status: Approved

> Scope: India-first analysis of the major HRMS/HCM/payroll platforms our product
> will compete with, plus the leading global players we must benchmark against.
> Figures (pricing, customer counts) are indicative and should be verified with live
> web research before this document is marked Approved.
>
> 2026-06-16 refresh: folded in `PHASE-1-REVIEW-001-market-research-refresh.md` findings
> from vendor portals and review sources. This changed the document status from Approved
> to Review; human owner approval is required again.

---

## 1. Purpose

Understand the competitive landscape so the Product Owner can define phased product scope
and a differentiated roadmap. India is the primary launch market; the architecture must
also support multi-country expansion (UAE, USA, UK).

## 2. Market Segmentation (India)

| Segment | Employees | Buying priorities | Typical incumbents |
|---|---|---|---|
| Micro / Startup | 1–50 | Cheap, fast payroll, compliance, self-serve | Kredily, RazorpayX Payroll, Zoho People |
| SMB | 50–500 | Payroll + compliance + attendance + leave, ease of use | greytHR, Keka, HROne, factoHR, Zimyo |
| Mid-Market | 500–2,000 | Configurable workflows, performance, integrations | Keka, Darwinbox, HROne, Qandle |
| Enterprise | 2,000+ | Multi-entity, global compliance, deep config, security | Darwinbox, SAP SuccessFactors, Workday, UKG |

**Insight:** the SMB + mid-market band (50–2,000) is the most contested and most
underserved on *configurability without code* — our core differentiator.

---

## 3. India-Focused Competitors

### greytHR
- **Segment:** SMB, strong in payroll + statutory compliance.
- **Strengths:** Deep, reliable India payroll & compliance (PF, ESI, PT, LWF, TDS,
  Form 16); large customer base; trusted brand; good ESS portal.
- **Weaknesses:** Dated UX in places; performance/recruitment modules weaker; limited
  deep configurability ("config ceiling" — simple changes need vendor tickets); mobile
  app glitches; post-update regressions; enterprise scale and global payroll limited.
- **Pricing:** Free up to 25 employees; affordable PEPM tiers above (see §11).

### Keka
- **Segment:** SMB to mid-market; strong product-led growth.
- **Strengths:** Modern UX; strong all-in-one (core HR, payroll, PMS, hiring);
  good analytics; popular with tech/services firms.
- **Weaknesses:** Configurability still partly hardcoded; large-enterprise depth and
  multi-country payroll limited; support scaling complaints.
- **Pricing:** PEPM, module-based tiers.

### HROne
- **Segment:** SMB to mid-market.
- **Strengths:** Broad module coverage; mobile-first; workflow automation; competitive
  pricing.
- **Weaknesses:** Perceived as feature-broad but shallow in spots; UX consistency;
  enterprise governance/security depth.

### factoHR / Zimyo / Qandle / Pocket HRMS / sumHR
- **Segment:** SMB challengers.
- **Strengths:** Aggressive pricing, attendance/biometric integrations, mobile,
  India compliance, niche differentiators (e.g. factoHR payroll, Zimyo engagement).
- **Weaknesses:** Smaller scale, thinner enterprise governance, limited true
  no-code extensibility, variable support.

### Kredily / RazorpayX Payroll
- **Segment:** Micro/startup; freemium and fintech-led.
- **Strengths:** Free/low-cost payroll, fast onboarding, payments integration.
- **Weaknesses:** Shallow HR breadth beyond payroll; not built for mid-market+ config.

### Darwinbox
- **Segment:** Indian-origin **enterprise** HCM, expanding across Asia/MEA.
- **Strengths:** Enterprise-grade, highly configurable, strong mobile, rapid feature
  velocity, AI features; serves large conglomerates.
- **Weaknesses:** Cost; implementation complexity; SMB over-served; payroll depth
  varies by country.
- **Why it matters:** The closest "configurable enterprise from India" benchmark —
  our most important strategic reference.

---

## 4. Global Benchmarks

| Product | Segment | Strengths | Weaknesses vs. India needs |
|---|---|---|---|
| **BambooHR** | SMB (US-centric) | Excellent UX, simple core HR, ATS | Weak India payroll/statutory; limited deep config |
| **Workday** | Large enterprise | Best-in-class HCM + finance, analytics, global | Very expensive; long implementations; overkill for SMB; India payroll often via partners |
| **SAP SuccessFactors** | Large enterprise | Deep modules, global compliance, ecosystem | Complex, costly, dated UX in parts; heavy to configure |
| **UKG** | Mid–large (US/EU) | Workforce mgmt, time & attendance, payroll | Limited India footprint; not India-compliance native |

**Insight:** Global leaders win on breadth and global compliance but lose on India
statutory depth, cost, speed of implementation, and no-code configurability for SMB/mid.

---

## 5. India Compliance Bar (table stakes)

Any credible India HRMS must natively handle: **PF, ESI, PT (state-wise), LWF, TDS,
Form 16, Gratuity, and Full & Final Settlement**, with statutory report formats and
returns. This is a hard entry barrier and a key reason global products underperform
in India. Our Compliance Layer + country plugins must match greytHR-level depth at
launch.

---

## 6. Common Customer Pain Points (to validate in /docs/03-gap-analysis)

- Customizations require vendor involvement / code (not true no-code).
- Payroll accuracy and statutory updates lag at scale.
- Poor support responsiveness as customers grow.
- Rigid workflows/forms; limited self-service configuration.
- Weak multi-entity / multi-country handling for expanding Indian companies.
- Reporting requires exports; limited ad-hoc report building.
- Integration friction with biometric devices and third-party tools.
- Mobile and attendance reliability issues: login friction, punch sync failures,
  geolocation/facial-recognition errors, and unclear regularization status.
- Implementation drag: setup, migration, policy configuration, and payroll readiness take
  too long unless the vendor is heavily involved.
- Payroll edge-case irritation: FBP, mid-cycle CTC changes, retro corrections, arrears,
  proration, variable pay, and corrections after payroll lock often create manual work.
- Pricing and add-on confusion: customers dislike hidden limits, unclear module
  entitlements, and surprise add-on costs.

---

## 7. Strategic Opportunities for Our Platform

1. **True no-code configurability** — dynamic forms, workflows, rules, reports, feature
   flags — as a first-class platform, not bolt-ons. This is the central wedge.
2. **greytHR-grade India compliance** + a clean **country-plugin** path to UAE/USA/UK.
3. **Modern UX + mobile-first** matching Keka/Darwinbox, usable by non-technical HR.
4. **Multi-tenant + white-label** to serve consultants/payroll bureaus reselling to SMBs.
5. **Affordable RAG AI assistant** for HR/policy/payroll queries — enterprise tier
   now has AI (Darwinbox Agentic AI, Zoho Zia), but a deep, affordable RAG assistant
   for the SMB/mid-market remains an open gap (see §11 Appendix).
6. **Connector framework** for attendance devices (ZKTeco, eSSL, Matrix, Suprema) with
   plug-and-play, no per-customer code.
7. **Configuration operations** — sandbox, diff, approval, promotion, rollback, and audit
   for tenant configuration, so HR can change safely without vendor tickets.
8. **Implementation success tooling** — setup wizard, migration validators, templates,
   readiness score, and sample payroll dry runs to reduce onboarding drag.
9. **Mobile reliability as a product capability** — offline/retry, clear sync status,
   punch reconciliation, and fast approval flows.
10. **Full-suite phase plan** — document table-stakes modules such as ATS, onboarding,
    offboarding, documents, service desk, engagement, expenses, assets, and workforce
    scheduling even when they are delivered in later phases.

---

## 8. Strategic Positioning Hypothesis (HIGH IMPORTANCE - Product Owner)

> **Priority:** Critical strategic input. This hypothesis must be reviewed by the Product
> Owner before finalizing PRD, roadmap, phase priorities, sales/demo narrative, and
> buyer-interview scripts. Expanded research is captured in
> `docs/01-market-research/POSITIONING-HYPOTHESIS-001-product-owner.md`.

> "An enterprise-grade, configurable, multi-tenant HRMS with greytHR-level India
> compliance and Darwinbox-level configurability — at a price and implementation speed
> that wins the underserved 50–2,000 employee mid-market — extensible to global payroll
> via plugins, and AI-native from day one."

This is more than a marketing line. It is the Product Owner's product strategy filter:

- If a feature does not strengthen payroll/compliance trust, no-code configurability,
  mid-market usability, extensibility, or AI-native self-service, it should not enter an
  early phase.
- If a customer-specific request requires core code changes, it must be redesigned as
  configuration, extension, plugin, provider adapter, or event/API integration.
- If a module is table-stakes but not differentiating, it should be delivered in the
  right later phase rather than overloading Phase 7A.
- If the hypothesis is not validated by buyer interviews, the PRD and roadmap must be
  revised before development.

Validation target: 10-15 HR/payroll/IT buyer interviews in the 50-2,000 employee segment
before this positioning is treated as final.

---

## 9. Hidden Gaps in Existing HRMS Solutions (The Real Opportunity)

Most vendors compete on *features*. Customers actually churn because of **friction,
complexity, poor support, and rigidity** — not because a leave module is missing. The
gaps below are largely unsolved today and form our strongest moat, especially in the
100–2,000 employee band. Each maps to a platform engine already named in `HRMS_Plan.md`,
so this expands *depth*, not scope.

> These are market-observation **hypotheses**. The Competitor Gap Analyst must validate
> each against real complaints (G2, Capterra, Reddit, Quora) in `docs/03-gap-analysis`
> before they drive the PRD.

| # | Gap (existing problem) | Our opportunity | Signature capability | Plan engine |
|---|---|---|---|---|
| A | "No-code" is not truly no-code — conditional fields, dynamic validations, multi-level/complex approvals still need vendor tickets | HR configures forms, workflows, policies, reports, notifications, dashboards without code | **Workflow Studio** (Power Automate / Zapier inside HRMS) | Workflow + Rules + Form Builder |
| B | Reporting is broken — everything exports to Excel; attrition, salary trends, leave-abuse, hiring efficiency built by hand | Natural-language reporting | **AI Report Builder** — "employees with attendance < 85% in last 3 months" → report auto-generated | Report Builder + AI |
| C | Employees can't self-serve policy answers; HR repeats the same questions | RAG over policies, SOPs, handbook; instant NL answers (deep RAG still rare below the enterprise tier) | **AI HR Assistant** | AI Engine (RAG) |
| D | Multi-company structures painful — parent/subsidiary/branch/franchise treated as separate instances | One platform, many legal entities, shared employees, inter-company transfers, consolidated reporting | **Organization Graph** | Identity + Employee |
| E | Attendance integration is custom, manual, vendor-dependent (ZKTeco, eSSL, Matrix, Suprema) | Plug-and-play device drivers | **Attendance Connector Marketplace** (Add Device → ZKTeco → IP → Save) | Integration Engine |
| F | HRMS built for HR, not managers — no view of who's overloaded / likely to resign | Decision support for line managers | **Manager Intelligence Dashboard** — burnout risk, flight risk, engagement, workload heatmap | AI + Analytics |
| G | Poor employee experience — login only for leave/payslips | Daily-use destination | **Employee Super App** — attendance, payslips, learning, recognition, internal jobs, surveys, AI assistant | Multiple |
| H | Contingent workforce unsupported — only full-time handled well | One platform for all worker types | **Unified Workforce Management** — employees, vendors, contractors, interns, freelancers | Employee |
| I | Compliance is reactive — issues found after filing deadlines | Proactive prevention | **Compliance Intelligence Engine** — "14 employees missing PF eligibility", "ESI filing due in 3 days" | Compliance + Rules |
| J | Onboarding is manual — users, forms, documents, tracking all by hand | Event-driven automation | **Zero-Touch Onboarding** — offer letter triggers portal, docs, policy ack, IT requests, manager tasks | Workflow + Event Bus |
| K | HRMS become isolated systems | Ecosystem | **Integration Marketplace** — M365, Google Workspace, Slack, Teams, Jira, Azure AD, SAP, Tally, QuickBooks | Integration Engine |
| L | Systems track employees but don't plan workforce | Forecasting | **Workforce Planning** — simulate "hire 100", "attrition +10%", "salaries +15%"; budget forecasting | Analytics + AI |
| M | Weak auditability — who changed salary / approved leave / what changed | Full forensic history | **Time Machine Audit Trail** — before/after value, who, when, reason | Audit Engine |
| N | Internal HR requests scattered across email/WhatsApp/calls/Teams | Structured intake | **HR Service Desk** — payroll/leave/reimbursement/ID-card tickets with SLA tracking | Workflow |
| O | Category framing is "HRMS" | Reposition the category | **People Operations Platform / HR Operating System** — HR + Payroll + Compliance + Service Desk + AI + Workflow + Analytics + Planning | Whole platform |

## 10. Roadmap Positioning Recommendation

**Positioning statement:** "Darwinbox-level configurability + greytHR-level compliance +
Workday-style analytics + AI-first employee experience" — for the underserved
100–2,000 employee mid-market.

The moat is **not** another Leave or Payroll module. Priority differentiators:

1. No-Code Workflow Engine (Workflow Studio)
2. AI Knowledge Assistant (RAG)
3. Compliance Intelligence
4. Workforce Analytics
5. Multi-Tenant White-Label Platform
6. Integration Marketplace
7. Employee Super App
8. Workforce Planning & Forecasting

> **Handoff note for the Product Owner:** treat items 1–3 as Phase 7A defining
> differentiators and 4–8 as later phases. Solution Architect to confirm feasibility against the
> Modular Monolith design (ADR-004) before they enter the roadmap.

---

## 11. Appendix A — Web-Verified Module & Feature Coverage (June 2026)

Compiled from vendor sites, Gartner/Capterra/G2 and comparison sources (see §13).
Legend: ✓ native/strong · ~ partial, add-on, or weak · ✗ absent/not evident · ? unverified.

| Capability | greytHR | Keka | HROne | Darwinbox | Zoho People | Our target |
|---|---|---|---|---|---|---|
| Core HR + ESS | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Payroll + India statutory (PF/ESI/PT/LWF/TDS/Form16) | ✓ strong | ✓ (FBP & mid-cycle CTC ~ manual) | ✓ (multi-state, wage-code, FFS) | ✓ (varies by country) | ~ (via Zoho Payroll) | ✓✓ |
| Attendance / time + biometric | ✓ | ✓ (geo) | ✓ (Time Office) | ~ (reviews flag gaps) | ✓ (geofence, facial) | ✓✓ connector marketplace |
| Leave | ✓ | ✓ | ✓ | ~ | ✓ | ✓ |
| Shifts / roster | ~ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Recruitment / ATS | ~ weak | ✓ | ✓ | ✓ | ✓ (Zoho Recruit) | ✓ |
| Onboarding | ✓ | ✓ | ✓ | ✓ | ✓ | ✓✓ zero-touch |
| Performance / talent | ✓ add-on | ✓ | ✓ | ✓ strong | ✓ | ✓ |
| LMS / learning | ✗ | ? | ✓ | ✓ | ✓ | ✓ |
| Engagement / surveys | ✓ add-on | ✓ (pulse, social) | ✓ | ✓ | ~ | ✓ |
| Helpdesk / HR service desk | ~ | ✓ | ✓ | ✓ | ✓ (cases) | ✓ (table stakes, not a moat) |
| Expenses / loans | ~ | ✓ | ✓ | ✓ | ~ (Zoho Expense) | ✓ |
| IT / asset management | ✓ add-on | ? | ✓ | ? | ? | ✓ |
| People analytics / dashboards | ~ reports | ✓ | ~ | ✓ (50+, drag-drop) | ~ (Zoho Analytics) | ✓✓ |
| AI assistant / agentic AI | ~ limited | ~ | ~ ("Inbox for HR") | ✓ (Agentic AI, skills ontology) | ~ (Zia) | ✓✓ RAG-native |
| Workforce planning / forecasting | ✗ | ~ | ✗ | ~ (skills/talent) | ✗ | ✓✓ |
| Multi-entity / org graph | ~ | ~ | ~ | ✓ (45+ countries) | ~ | ✓✓ |
| True no-code configurability | ~ "config ceiling" | ~ "partly hardcoded" | ~ (engine updates) | ✓ (but "config drag" at scale) | ✓ (Zoho workflow) | ✓✓ Workflow Studio |
| PSA / project + billing | ✗ | ✓ (unique) | ~ | ~ | ✓ (timesheets) | ~ later |

**SMB challengers** (factoHR, Zimyo, Qandle, Pocket HRMS): all cover payroll + India
compliance + attendance + leave + onboarding + performance; factoHR adds face-recognition
& chatbots; Zimyo has configurable multi-step approval workflows; Qandle is modular
(hire-to-retire, 2,500+ clients) but charges add-ons for timesheet/roster. None show
deep workforce planning, org-graph, or RAG-grade AI assistants.

### Additional Module Findings (Phase 1 Refresh)

The refreshed review shows several modules are now table-stakes in modern HR suites and
should be documented in the full-product phase plan, even if delivered after Phase 7A.

| Module / Capability | Market signal | Customer happiness when done well | Customer irritation when weak | Product direction |
|---|---|---|---|---|
| Recruitment / ATS | Common in Keka, HROne, Darwinbox, Zoho/BambooHR ecosystem | One hiring-to-onboarding flow | Hiring data disconnected from employee master | Later phase; must reuse Workflow, Forms, Documents, AI screening |
| Onboarding | Common across full suites | New joiner tasks, documents, IT/manager actions are tracked | Manual email/WhatsApp chasing | Phase 7B/7D; event-driven onboarding templates |
| Offboarding / exit / FNF | Common in stronger suites | Exit tasks and FNF are controlled | Missed assets, documents, payroll holds | Phase 7B; workflow + payroll + asset integration |
| Performance / goals / OKRs | Common | Structured review cycles and manager visibility | Rigid cycles, poor calibration | Phase 7D; configurable cycles, forms, calibration |
| LMS / learning | Common in enterprise and some Indian suites | Training assignment and completion tracking | Learning sits outside HRMS | Phase 7D; integrate with skills and compliance training |
| Engagement / surveys / recognition | Increasingly common | Pulse feedback and recognition improve adoption | HRMS used only for payslips/leave | Phase 7D; lightweight surveys, eNPS, recognition |
| HR service desk / cases | Common enough to be table-stakes | Employees track requests with SLA | HR requests lost in email/chat | Phase 7B; not a differentiator, but required |
| Document / letter / e-sign | Common | Offer letters, salary letters, policies, acknowledgements in one place | Manual letter generation and missing acknowledgements | Phase 7B; template engine + e-sign provider adapter |
| Shift foundation + advanced roster/workforce scheduling | Important for attendance-heavy employers | Shift definitions, assignments, swaps, overtime, and week-offs are controlled | Attendance exceptions explode | Phase 7A includes Shift Foundation; Phase 7E keeps advanced roster/workforce scheduling |
| Expense / travel / reimbursements | Common in broader suites | Claims flow into payroll/reimbursements | Separate tools and manual policy checks | Phase 7E; policy-as-rules + workflow approvals |
| Asset and IT requests | Present in several suites or adjacent systems | Onboarding/offboarding assets tracked | Missed returns and manual IT handoff | Phase 7E; workflow + extension module |
| Compensation review | Common in enterprise | Salary revision cycles and letters controlled | Spreadsheet-driven increments | Phase 7E; effective-dated compensation + approvals |
| Provider / integration health | Rare as a polished HRMS feature | Admin knows connector/provider health | Silent sync failures and support tickets | Phase 7B/7C; health center for devices, email/SMS, webhooks |
| Workforce planning / forecasting | Rare below enterprise | Budget and hiring scenarios are visible | HRMS records history but cannot plan | Later enterprise phase; analytics + AI |

### Customer Irritation -> Feature Refinement Map

| Irritation | Refined feature requirement |
|---|---|
| Slow support and unclear escalation | In-app support status, SLA timer, escalation path, product status page |
| Vendor ticket needed for config | No-code config with sandbox, diff, approval, promote, rollback |
| Mobile/punch sync issues | Offline capture, retry, duplicate detection, connector health, visible sync status |
| Payroll edge cases go manual | Payroll simulation, dry run, exception queue, effective-dated corrections, lock/unlock workflow |
| Implementation complexity | Tenant setup wizard, migration validator, templates, readiness score |
| Reporting falls back to Excel | Saved views, scheduled reports, semantic data layer, permission-safe exports |
| Hidden add-ons/limits | Tenant entitlement dashboard, usage limits, billing drivers, renewal impact |

### Full-Product Phase Priority Recommendation

| Phase | Module priority |
|---|---|
| Phase 7A | Foundation group first: Tenant Catalog/RLS, Branch/Office Hierarchy, Identity/RBAC/ABAC, Effective Dating, Audit/Time Machine, Event Bus, Rule Engine, Workflow Studio, Configuration-as-Data; then Core HR, Leave, Attendance with Shift Foundation, Payroll/Compliance, standard reports |
| Phase 7B | White-label, SSO, notification preferences, config sandbox/promotion, documents/letters/e-sign, HR service desk, onboarding/offboarding basics, provider health, implementation tooling |
| Phase 7C | RAG HR assistant, richer reporting/BI, compliance intelligence, mobile reliability hardening, attendance connector expansion |
| Phase 7D | Recruitment/ATS, advanced onboarding, performance/goals/OKRs, LMS, engagement/surveys/recognition |
| Phase 7E | Advanced roster/workforce scheduling, shift swap, expense/travel/reimbursements, assets/IT requests, compensation review, multi-entity org graph UI |
| Later phases | Workforce planning, integration marketplace, contingent workforce, multi-country payroll plugins, advanced manager intelligence |

### Pricing (indicative, June 2026)

India HRMS typically runs **₹40–₹500 per employee/month** by feature depth and size.
- **greytHR:** free up to 25 employees; affordable PEPM tiers above.
- **Zoho People:** from ~₹48/user/month (cheapest enterprise-grade).
- **Keka:** module-based PEPM tiers (mid-range).
- **Darwinbox / HROne:** custom/enterprise quotes (no public PEPM).

> Caveat: exact tier pricing for Keka/Darwinbox/HROne is quote-based; treat the band
> as directional, not contractual.

---

## 12. Open Questions / To Verify (before Approved)

- Exact current PEPM tier pricing for Keka, Darwinbox, HROne (quote-based).
- Latest customer counts and funding/market-share data.
- ⚠️ **Nuance confirmed:** AI is **no longer "nascent" at the enterprise tier** —
  Darwinbox ships Agentic AI + skills ontology; factoHR has chatbots; Zoho has Zia.
  Our AI edge is an **affordable, RAG-native assistant for the SMB/mid-market**, not
  "incumbents have no AI." Positioning language updated accordingly (§7, §9C).

## 13. Sources

Vendor & analyst (accessed June 2026):
- greytHR — [Gartner Peer Insights](https://www.gartner.com/reviews/product/greythr),
  [Capterra reviews](https://www.capterra.com/p/150850/greytHR/reviews/),
  [2025 release notes](https://admin-help.greythr.com/admin/answers/wrjoimkurjakuffae-1ifq/)
- Keka — [GetApp](https://www.getapp.com/hr-employee-management-software/a/keka/),
  [Research.com review](https://research.com/software/reviews/keka)
- HROne — [SoftwareSuggest](https://www.softwaresuggest.com/hrone),
  [HROne payroll-vs-HRMS](https://hrone.cloud/blog/payroll-software-vs-full-hrms-india/)
- Darwinbox — [Gartner Voice of Customer 2025](https://darwinbox.com/en-us/blog/gartner-voice-of-customer-2025),
  [SoftwareFinder](https://softwarefinder.com/hr/darwinbox)
- Zoho People — [Features](https://www.zoho.com/people/features.html),
  [What's New](https://www.zoho.com/people/whats-new.html)
- SMB challengers — [factoHR](https://factohr.com/hr-software/),
  [Qandle top-20 list](https://www.qandle.com/blog/top-20-hr-softwares-in-india/),
  [PocketHRMS comparison](https://www.pockethrms.com/best-hrms-software-in-india/)
- Complaints/gaps — [Keka vs greytHR (HRSuggest)](https://www.hrsuggest.com/resources/greythr-vs-keka-india-march-2026),
  [Outgrowing Keka/Darwinbox/greytHR](https://hrone.cloud/blog/outgrowing-keka-darwinbox-greythr-india),
  [Keka vs Darwinbox (G2)](https://www.g2.com/compare/darwinbox-vs-keka)

> Note: several comparison/complaint sources are vendor-published (e.g. hrone.cloud) and
> may carry bias; treated as directional and cross-checked against Gartner/Capterra/G2.

---

## Approval

Product Owner: ____ · Project Manager: ____ · HR Expert: ____  (Status: Draft → Approved)
