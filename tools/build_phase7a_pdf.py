from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "11-release"
ASSET_DIR = OUT_DIR / "assets" / "phase-7a"
PDF_PATH = OUT_DIR / "PHASE-7A-approved-development-brief.pdf"

BLUE = colors.HexColor("#2E74B5")
DARK = colors.HexColor("#1F4D78")
INK = colors.HexColor("#1E232A")
MUTED = colors.HexColor("#555555")
LIGHT = colors.HexColor("#F2F4F7")
PALE = colors.HexColor("#E8EEF5")


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        "TitleLarge",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        textColor=DARK,
        alignment=TA_LEFT,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12.5,
        leading=16,
        textColor=MUTED,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        "H1Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=BLUE,
        spaceBefore=8,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        "H2Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=BLUE,
        spaceBefore=8,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        "BodyCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.2,
        leading=13.2,
        textColor=INK,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        "BulletCustom",
        parent=styles["BodyCustom"],
        leftIndent=14,
        firstLineIndent=-8,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        "CalloutTitle",
        parent=styles["BodyCustom"],
        fontName="Helvetica-Bold",
        textColor=DARK,
        spaceAfter=2,
    )
)


def p(text, style="BodyCustom"):
    return Paragraph(escape(text), styles[style])


def bullet(text):
    return Paragraph("- " + escape(text), styles["BulletCustom"])


def h1(text):
    return p(text, "H1Custom")


def h2(text):
    return p(text, "H2Custom")


def callout(title, text):
    tbl = Table(
        [[p(title, "CalloutTitle"), p(text)]],
        colWidths=[1.5 * inch, 4.75 * inch],
        hAlign="LEFT",
    )
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#C9D6E2")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return [tbl, Spacer(1, 7)]


def make_table(headers, rows, col_widths):
    data = [[p(h, "CalloutTitle") for h in headers]]
    for row in rows:
        data.append([p(str(cell)) for cell in row])
    tbl = Table(data, colWidths=col_widths, hAlign="LEFT", repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8BCC4")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return [tbl, Spacer(1, 8)]


def image_block(filename, caption):
    path = ASSET_DIR / filename
    img = Image(str(path), width=6.25 * inch, height=4.16 * inch)
    img.hAlign = "CENTER"
    return [img, p(caption, "Small"), Spacer(1, 8)]


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75 * inch, 0.45 * inch, "HRMS Platform | Phase 7A Approved Development Brief")
    canvas.drawRightString(7.75 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.72 * inch,
        title="Phase 7A Approved Development Brief",
        author="Codex",
    )
    story = []

    story.append(p("PHASE 7A APPROVED DEVELOPMENT BRIEF", "TitleLarge"))
    story.append(
        p(
            "What we are going to build, who it serves, and how the approved HRMS platform will work",
            "Subtitle",
        )
    )
    story.extend(image_block("team-meeting-clean.jpg", "Web image: Wikimedia Commons team meeting photo, used as a collaboration visual."))
    story.extend(
        callout(
            "Conclusion",
            "Phase 7A is the first full development phase of the HRMS platform. It builds the secure SaaS foundation first, adds Branch/Office Hierarchy and Shift Foundation, then delivers Core HR, Leave, Attendance, Payroll with India compliance, and Standard Reports. The approved design is built for configuration, audit, tenant safety, branch-scoped operations, shift-aware time data, and future modules without changing core code.",
        )
    )
    story.extend(
        make_table(
            ["Approved package", "Status"],
            [
                ["75 implementation documents", "Approved"],
                ["5 hardening standard/backlog documents", "Approved"],
                ["Total Phase 7A development documentation", "80/80 Approved"],
            ],
            [4.25 * inch, 1.6 * inch],
        )
    )

    story.append(PageBreak())
    story.append(h1("1. What Phase 7A Is"))
    story.append(
        p(
            "Phase 7A is the foundation and first working product phase for the HRMS platform. It is not only a set of HR screens. It is the base that allows the product to become a configurable, multi-tenant, enterprise-grade HRMS."
        )
    )
    for item in [
        "It creates a secure tenant-aware platform where each customer is isolated.",
        "It allows one tenant to operate child branches/offices with separate branch admins and scoped employee access.",
        "It gives HR teams configurable rules, workflows, policies, reports, and approvals.",
        "It delivers everyday HR operations: employee records, self-service, branch assignment, leave, shift-aware attendance, payroll, payslips, and reports.",
        "It creates the architecture needed to add later modules without rebuilding the core.",
    ]:
        story.append(bullet(item))
    story.extend(callout("Simple meaning", "Phase 7A is the platform proof: first build the strong base, then build the core HR workflows on top of that base."))

    story.append(h1("2. Who This Phase Is For"))
    story.extend(
        make_table(
            ["User group", "What they will use"],
            [
                ["Employees", "View profile, request leave, see attendance, access payslips, use self-service changes."],
                ["Managers", "Approve leave and attendance changes, view team data, track pending work, and see shift-aware attendance context."],
                ["HR Admins", "Manage employees, policies, leave setup, attendance rules, workflows, and reports."],
                ["Payroll Teams", "Run payroll, validate exceptions, approve results, publish payslips, manage India compliance."],
                ["Tenant Admins", "Manage configuration, branch/office hierarchy, feature flags, module settings, security, and approvals."],
                ["Auditors and Security Teams", "Review audit trails, time-machine history, access evidence, and export controls."],
            ],
            [1.55 * inch, 4.75 * inch],
        )
    )

    story.append(PageBreak())
    story.append(h1("3. What We Are Going To Develop"))
    story.append(p("The approved scope is split into platform foundations and business modules."))
    story.extend(
        make_table(
            ["Area", "Approved delivery"],
            [
                ["Tenant Catalog + RLS", "Customer isolation, tenant context, and row-level security."],
                ["Branch / Office Hierarchy", "Child branches/offices, branch admin scope, employee branch assignment, and branch-aware reporting."],
                ["Identity + RBAC/ABAC", "Login, roles, permissions, policy-based access, sessions, and emergency access controls."],
                ["Effective Dating", "History-aware records so the system knows what was true on any date."],
                ["Audit / Time Machine", "Every important action is traceable, searchable, and reconstructable."],
                ["Event Bus + Outbox", "Reliable module-to-module communication without tight coupling."],
                ["Rule Engine", "No hardcoded HR or payroll policies; rules are configurable, versioned, and testable."],
                ["Workflow Studio", "Approvals, delegation, SLA, escalation, versioned workflow definitions."],
                ["Configuration-as-Data", "Feature flags, forms, policies, rules, reports, navigation, and settings as governed data."],
                ["Core HR + ESS", "Employee master, assignments, org data, and self-service requests."],
                ["Leave", "Leave types, accruals, balances, approvals, calendars, and payroll impact."],
                ["Attendance + First Connector", "Punch capture, regularization, one connector framework, payroll attendance feed."],
                ["Shift Foundation", "Basic shift templates, employee shift assignment, overrides, shift resolver, and shift-aware attendance/payroll."],
                ["Payroll + India Compliance", "Salary structures, payroll runs, payslips, PF/ESI/PT/LWF/TDS/Form 16 foundation."],
                ["Standard Reports", "Operational and statutory reports with security, filters, exports, and audit."],
            ],
            [1.85 * inch, 4.45 * inch],
        )
    )

    story.append(PageBreak())
    story.append(h1("4. How The Product Will Work For Users"))
    story.extend(
        make_table(
            ["Workflow", "Simple operating flow"],
            [
                ["Employee self-service", "Employee requests a profile change or leave; workflow routes approval; result updates record and audit."],
                ["Leave", "Employee applies; rules check balance/calendar; manager approves; balance ledger updates; payroll/report events fire."],
                ["Branch operations", "Tenant admin creates offices; branch admins work only within approved branch scope; reports and exports respect that boundary."],
                ["Attendance", "Punches arrive from web/manual/connector; effective shift is resolved; daily summary calculated; corrections approved; payroll receives payable-day data."],
                ["Payroll", "Payroll team runs dry run from Core HR, Leave, and shift-aware Attendance; resolves exceptions; approval locks results; payslips published; reports generated."],
                ["Configuration", "Admin drafts policy/workflow/rule; system validates impact; approval; publish; rollback available."],
                ["Audit and reports", "Authorized users search history, view as-of data, export evidence, and track who changed what."],
            ],
            [1.7 * inch, 4.6 * inch],
        )
    )
    story.extend(callout("Operating principle", "Every important change is approved where required, audited, evented, tenant-safe, and explainable."))

    story.append(h1("5. What Is Not Being Built In Phase 7A"))
    for item in [
        "Recruitment, performance, LMS, engagement, expenses, assets, service desk, and advanced onboarding are later phases.",
        "Multi-country payroll packs are later; Phase 7A is India-first payroll and compliance foundation.",
        "Advanced roster planning, shift swaps, and workforce demand planning are later phases. Phase 7A includes the basic Shift Foundation needed for attendance and payroll.",
        "Advanced BI, marketplace, and full AI assistant capabilities are not part of the Phase 7A development scope.",
        "Customer-specific changes must not be hardcoded into core logic.",
    ]:
        story.append(bullet(item))

    story.append(PageBreak())
    story.append(h1("6. Architecture In Simple Language"))
    story.extend(image_block("server-racks-clean.jpg", "Web image: Wikimedia Commons server infrastructure photo, used as a platform architecture visual."))
    for item in [
        "Multi-tenant SaaS: many customers can use the platform, but their data stays isolated.",
        "Branch-scoped SaaS: a tenant can have child branches/offices; tenant admins see all, while branch admins see only approved branches.",
        "Security first: every API checks tenant, user identity, role, permissions, and policy.",
        "Rules-as-data: HR and payroll policies live in configurable rule sets, not in code.",
        "Workflow-as-data: approval flows are versioned definitions, not hardcoded paths.",
        "Event-driven backbone: modules communicate through reliable events such as BranchScopeAssigned, LeaveApproved, ShiftDefinitionPublished, or PayrollRunPublished.",
        "Effective dating and time machine: changes are historical, explainable, and usable for payroll and reporting.",
        "Open for extension: new modules connect through manifests, APIs, events, providers, and configuration.",
    ]:
        story.append(bullet(item))

    story.append(PageBreak())
    story.append(h1("7. Development Order"))
    story.append(p("The approved order is dependency-led. Business modules come only after the platform foundations they need."))
    story.extend(
        make_table(
            ["Sprint", "Theme", "Expected result"],
            [
                ["S1", "Tenant + Identity + Branch Scope", "Every request is tenant-safe, branch-aware, and permission-aware."],
                ["S2", "Effective Dating + Audit + Events", "History, audit, and events work across the platform."],
                ["S3", "Rule + Workflow + Configuration", "Rules, approvals, and configuration are data-driven."],
                ["S4", "Core HR + ESS", "Employee master, branch assignment, and self-service are usable."],
                ["S5", "Leave", "Leave policies, applications, approvals, and balances work."],
                ["S6", "Attendance + Shift Foundation + Connector", "Shift-aware attendance capture and first connector feed payroll."],
                ["S7", "Payroll Engine", "Payroll run, components, calculations, and payslips work."],
                ["S8", "India Compliance", "PF, ESI, PT, LWF, TDS, Form 16 foundation, FBP, revisions."],
                ["S9", "Workflow Hardening", "Delegation, SLA, escalation, and migration are hardened."],
                ["S10", "Reports + Hardening", "Reports, exports, performance, security, and release readiness."],
            ],
            [0.55 * inch, 1.65 * inch, 4.1 * inch],
        )
    )

    story.append(h1("8. Security, Audit, and Quality Controls"))
    for item in [
        "Every table is tenant-scoped and every query must be tenant-filtered.",
        "Every module supports RBAC, ABAC, audit logging, and OpenAPI documentation.",
        "Critical operations need idempotency so retries do not duplicate payroll, leave, attendance, or workflow actions.",
        "PII and payroll-sensitive data require classification, masking, encryption, retention, and export controls.",
        "Tests include tenant-abuse cases, cross-tenant export attempts, role changes, impersonation audit, and security checks.",
        "Target coverage is at least 85%, with higher focus on payroll calculations, rules, ledger, and security paths.",
    ]:
        story.append(bullet(item))

    story.append(PageBreak())
    story.append(h1("9. What Has Been Approved"))
    story.extend(
        make_table(
            ["Document set", "Count", "Status"],
            [
                ["Business Requirements", "15", "Approved"],
                ["Technical Designs", "15", "Approved"],
                ["Database Designs", "15", "Approved"],
                ["UI Designs", "15", "Approved"],
                ["Test Plans", "15", "Approved"],
                ["Phase 7A Hardening Standards / Backlog", "5", "Approved"],
                ["Total Phase 7A development documentation", "80", "Approved"],
            ],
            [3.45 * inch, 0.75 * inch, 1.4 * inch],
        )
    )
    story.append(h1("10. How To Operate Phase 7A After Build"))
    for item in [
        "Admins configure tenants, branches/offices, roles, features, rules, workflows, calendars, shifts, payroll policies, and reports.",
        "Employees and managers use the portal for self-service, leave, attendance, approvals, and payslips.",
        "Payroll teams run dry runs first, resolve exceptions, seek approval, lock payroll, and publish payslips.",
        "Support and auditors use audit search, time-machine views, event trace, report history, and export evidence.",
        "Every change should be made through configuration, workflow, rule versions, or provider adapters, not direct code changes.",
    ]:
        story.append(bullet(item))

    story.append(PageBreak())
    story.append(h1("11. Implementation Guardrails"))
    story.extend(
        make_table(
            ["Guardrail", "Meaning"],
            [
                ["No code before approved docs", "This gate is now complete for Phase 7A documentation."],
                ["No hardcoded business rules", "Leave, attendance, payroll, workflow routing, and eligibility use Rule Engine/configuration."],
                ["No customer-specific core changes", "Customer behavior must be delivered through configuration, extensions, feature flags, providers, and plugins."],
                ["OpenAPI mandatory", "Every API must be versioned and documented before implementation is complete."],
                ["Event-driven where possible", "Approved events connect modules without direct database coupling."],
                ["Tenant isolation always", "Every module must enforce tenant context and prevent cross-tenant access."],
            ],
            [2.0 * inch, 4.3 * inch],
        )
    )
    story.append(h1("12. Source and Image Credits"))
    for item in [
        "Approved internal documents: Phase 7A business requirements, technical designs, database designs, UI designs, test plans, and hardening standards under the project docs folder.",
        "Roadmap source: ROADMAP-001 phased delivery, approved roadmap.",
        "Web image: WLM international team meeting Vienna 2023-05-27 12, Wikimedia Commons, used as a collaboration visual.",
        "Web image: Wikimedia Servers-0051 19, Wikimedia Commons, used as an infrastructure visual.",
        "Web reference themes used in approved docs: Microsoft SQL Server temporal/RLS documentation, OpenAPI Specification, CloudEvents, RabbitMQ reliability, OpenFeature, OWASP API Security, WCAG 2.2, EPFO, ESIC, Income Tax India, and market references including Zoho People, Keka, greytHR, BambooHR, and Darwinbox.",
    ]:
        story.append(bullet(item))

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
