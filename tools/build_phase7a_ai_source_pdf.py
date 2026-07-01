from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "docs" / "11-release" / "PHASE-7A-approved-ai-source-reference.pdf"
OUT_MD = ROOT / "docs" / "11-release" / "PHASE-7A-approved-ai-source-reference.md"
ASSET_DIR = ROOT / "docs" / "11-release" / "assets" / "phase-7a"
TEAM_IMAGE = ASSET_DIR / "team-meeting-clean.jpg"
SERVER_IMAGE = ASSET_DIR / "server-racks-clean.jpg"


MODULES = [
    {
        "key": "TENANT",
        "title": "Tenant Catalog + Row-Level Security",
        "phase": "S1 foundation",
        "schema": "catalog plus security RLS",
        "conclusion": (
            "This module is the foundation of the SaaS platform. It defines every customer, "
            "their status, placement, feature entitlements, branding, provider choices, and "
            "the tenant context required before any business data can be accessed. The approved "
            "design makes tenant isolation a platform rule, not a developer preference."
        ),
        "deliverables": [
            "Tenant catalog with tenant, shard, branding, feature flag, provider, provider config, and provider health records.",
            "Server-side tenant resolution from host, token-safe hints, or platform-owner context.",
            "SQL Server Row-Level Security for every tenant-scoped table.",
            "Tenant lifecycle controls for provision, activate, suspend, offboard, and placement change.",
            "Tenant-safe namespaces for cache, search, storage, events, logs, telemetry, and providers.",
        ],
        "architecture": [
            "The request pipeline resolves tenant context before application services run.",
            "Application services receive an immutable tenant context; repositories cannot run without it.",
            "Entitlements are checked across API, UI, jobs, reports, integrations, events, and AI.",
            "Provider abstraction reads tenant provider configuration without exposing secrets to business code.",
        ],
        "tables": [
            "catalog.Tenant",
            "catalog.TenantShard",
            "catalog.TenantBranding",
            "catalog.TenantFeatureFlag",
            "catalog.TenantConfigVersion",
            "catalog.ProviderType",
            "catalog.Provider",
            "catalog.TenantProviderConfig",
            "catalog.ProviderHealth",
            "security.fn_tenant_predicate",
            "security.TenantIsolation policy",
        ],
        "apis": [
            "GET /api/v1/tenants/{id}",
            "POST /api/v1/tenants",
            "POST /api/v1/tenants/{id}/suspend",
            "GET /api/v1/tenants/{id}/features",
            "PUT /api/v1/tenants/{id}/providers/{providerType}",
        ],
        "events": [
            "TenantProvisioned",
            "TenantActivated",
            "TenantSuspended",
            "TenantOffboardingStarted",
            "TenantFeatureFlagsChanged",
            "TenantProviderConfigChanged",
        ],
        "example": (
            "Tenant A and Tenant B can both use the same People table. Every row has TenantId. "
            "When Tenant A's request reaches SQL Server, SESSION_CONTEXT contains Tenant A's id, "
            "so RLS hides Tenant B rows and blocks wrong-tenant writes even if a query is written incorrectly."
        ),
        "test_focus": [
            "Cross-tenant reads and writes are blocked at service, EF filter, and SQL RLS layers.",
            "Suspended tenants cannot use APIs, jobs, reports, events, or integrations.",
            "Provider config and tenant lifecycle changes are audited and invalidate caches.",
        ],
    },
    {
        "key": "BRANCH",
        "title": "Branch / Office Hierarchy and Scoped Administration",
        "phase": "S1-S4 foundation",
        "schema": "org plus security",
        "conclusion": (
            "Branch and office hierarchy lets one tenant operate many offices, branches, sites, "
            "or regional units while preserving scoped administration. A complete tenant admin can "
            "see the whole tenant, while branch admins and branch-scoped users can only see or act "
            "inside their approved branch scope."
        ),
        "deliverables": [
            "Tenant branch and office tree with parent-child hierarchy, effective dates, status, timezone, country, state, and address metadata.",
            "Scoped administration model for tenant-wide admins, branch admins, HR operators, payroll operators, managers, and employees.",
            "Employee branch assignment with effective dating so historical reports and payroll remain correct.",
            "Branch-aware RBAC and ABAC enforcement across Core HR, Leave, Attendance, Payroll, Reports, exports, jobs, and events.",
            "Branch hierarchy events and audit evidence for branch changes, scope assignment, and employee branch movement.",
        ],
        "architecture": [
            "Branch hierarchy is modeled as tenant-owned organization data and exposed through shared scope resolvers.",
            "Authorization combines tenant context, RBAC permissions, ABAC attributes, and branch scope.",
            "Branch-scoped users cannot access sibling branch data unless a higher scope is explicitly granted.",
            "Downstream modules consume branch assignment through Core HR APIs/events and do not duplicate branch ownership logic.",
        ],
        "tables": [
            "org.BranchOffice",
            "org.BranchOfficeHierarchyClosure",
            "org.EmployeeBranchAssignment",
            "security.BranchScopeAssignment",
            "security.BranchScopeDecisionLog",
        ],
        "apis": [
            "GET /api/v1/branches",
            "POST /api/v1/branches",
            "GET /api/v1/branches/{id}/tree",
            "POST /api/v1/branches/{id}/scope-assignments",
            "GET /api/v1/security/branch-scopes",
        ],
        "events": [
            "BranchCreated",
            "BranchUpdated",
            "BranchHierarchyChanged",
            "BranchScopeAssigned",
            "BranchScopeRevoked",
            "EmployeeBranchAssignmentChanged",
        ],
        "example": (
            "Tenant A has a head office, Mumbai branch, Delhi branch, and Pune branch. A tenant admin can "
            "review all offices. The Mumbai branch admin can manage only Mumbai employees, approvals, "
            "attendance, reports, and exports. They cannot open Delhi employee details or payroll reports."
        ),
        "test_focus": [
            "Branch admin cannot read, export, approve, or update sibling branch data.",
            "Tenant admin can view all branches inside the same tenant but never another tenant.",
            "Historical employee branch assignment works for as-of reports, payroll evidence, and audit.",
        ],
    },
    {
        "key": "IDENTITY",
        "title": "Identity, Authentication, RBAC, and ABAC",
        "phase": "S1 foundation",
        "schema": "security",
        "conclusion": (
            "Identity is the central security module. It handles authentication, sessions, roles, "
            "permissions, policies, delegation, impersonation, emergency access, and authorization "
            "decision traceability. The approved design combines RBAC for role permissions and ABAC "
            "for contextual rules."
        ),
        "deliverables": [
            "Local login, OIDC/SSO, MFA, adaptive risk checks, and refresh token rotation.",
            "RBAC permissions, ABAC policies, deny-by-default authorization, and policy decision tracing.",
            "SCIM user and group provisioning for enterprise identity integration.",
            "Device/session management, global logout, remote session termination, and distributed revocation.",
            "Break Glass emergency access with reason, expiry, approval option, revocation, and audit.",
        ],
        "architecture": [
            "Client requests pass through API Gateway, Authentication Service, Token Service, PEP, and PDP.",
            "The PEP enforces permissions at API, handler, job, report, and UI capability boundaries.",
            "The PDP evaluates role, resource, tenant, user, delegation, impersonation, and ABAC policy context.",
            "Distributed session and revocation state keep multiple app instances consistent.",
        ],
        "tables": [
            "security.UserAccount",
            "security.Role",
            "security.Permission",
            "security.RolePermission",
            "security.UserRole",
            "security.AbacPolicy",
            "security.Session",
            "security.RefreshToken",
            "security.Delegation",
            "security.PasswordPolicy",
            "security.PasswordHistory",
            "security.AuthSecurityEvent",
            "security.BreakGlassAccess",
            "security.BreakGlassSession",
        ],
        "apis": [
            "POST /api/v1/auth/login",
            "POST /api/v1/auth/sso/start",
            "POST /api/v1/auth/mfa/verify",
            "POST /api/v1/auth/refresh",
            "GET /api/v1/security/sessions",
            "POST /api/v1/security/break-glass",
            "GET /api/v1/security/authorization-trace/{correlationId}",
        ],
        "events": [
            "UserLoggedIn",
            "MfaChallengeCompleted",
            "SessionRevoked",
            "RoleAssignmentChanged",
            "TenantRoleMatrixChanged",
            "BreakGlassActivated",
            "AuthSecurityEventRecorded",
        ],
        "example": (
            "A manager can approve a leave request only when RBAC grants Leave.Approve and ABAC confirms "
            "the employee belongs to the manager's allowed team, legal entity, or delegated scope. The "
            "decision record stores tenant, user, permission, policy version, result, reason, and correlation id."
        ),
        "test_focus": [
            "Unauthorized users cannot access secured endpoints or emergency access.",
            "Refresh token reuse is detected and revokes the session family.",
            "Distributed logout and role change invalidation work across all app instances.",
            "Brute-force, credential stuffing, adaptive MFA, and lockout controls are verified.",
        ],
    },
    {
        "key": "EFFECTIVE-DATING",
        "title": "Effective Dating and Bitemporal Core",
        "phase": "S2 foundation",
        "schema": "core and temporal history",
        "conclusion": (
            "Effective dating is a platform pattern for any business fact that changes over time. "
            "It allows the system to answer what was true on a business date, what the system knew "
            "at a system time, and why a change happened. This is essential for payroll, assignments, "
            "policies, workflow versions, compliance, and reporting."
        ),
        "deliverables": [
            "Shared effective dating service, period validator, as-of query service, change request flow, and history explanation.",
            "Mandatory valid-time columns for time-changing facts.",
            "SQL Server temporal table support for high-value history plus approved fallback patterns.",
            "Backdated, current, future-dated, supersede, cancel, and bulk effective-dated operations.",
            "Event publication through the outbox for every approved effective-dated change.",
        ],
        "architecture": [
            "Business APIs call application services, which call the Effective Dating Service before repositories.",
            "The Period Validator prevents invalid periods, overlaps, duplicate open-ended rows, and unsafe backdating.",
            "As-of reads are consistent across API, reporting, rules, workflow, and payroll.",
            "Sensitive corrections can be routed through Workflow Studio before activation.",
        ],
        "tables": [
            "core.EffectiveDatedEntityRegistration",
            "core.EffectiveDatedChangeRequest",
            "core.EffectivePeriodConflict",
            "EffectiveFrom",
            "EffectiveTo",
            "EffectiveStatus",
            "ChangeReason",
            "ApprovalReferenceId",
            "SupersededById",
            "VersionNumber or rowversion",
        ],
        "apis": [
            "GET /api/v1/{module}/{resource}?asOfDate=YYYY-MM-DD",
            "POST /api/v1/{module}/{resource}/future-change",
            "POST /api/v1/{module}/{resource}/backdated-correction",
            "GET /api/v1/{module}/{resource}/{id}/history/explain",
        ],
        "events": [
            "EffectiveDatedRecordChanged",
            "EffectiveDatedChangeApproved",
            "EffectiveDatedChangeRejected",
            "EffectiveDatedConflictDetected",
        ],
        "example": (
            "If an employee's department changes from Sales to Finance effective 1 July, reports for 30 June "
            "still show Sales, payroll from July uses Finance, and the history screen explains who approved "
            "the change, when it was entered, and which old row was superseded."
        ),
        "test_focus": [
            "Overlap prevention works for employee assignment, salary assignment, policy version, and workflow/rule versions.",
            "As-of API, report, and payroll results agree for the same business date.",
            "Backdated changes produce audit entries, outbox events, and explain-history evidence.",
        ],
    },
    {
        "key": "AUDIT",
        "title": "Audit and Time Machine",
        "phase": "S2 foundation",
        "schema": "audit",
        "conclusion": (
            "Audit and Time Machine provide evidence. Every important change, authorization decision, "
            "security event, workflow decision, export, and sensitive read is traceable. Time Machine "
            "reconstructs business state using effective dating, temporal history, audit records, workflow "
            "evidence, and events."
        ),
        "deliverables": [
            "Shared audit capture services consumed by all Phase 7A modules.",
            "Append-only audit records and field changes with masking, classification, retention, and legal hold.",
            "Security event collection for login, MFA, ABAC, emergency access, and suspicious activity.",
            "Time-machine snapshots and explain-history views.",
            "Controlled audit exports with purpose, approval, expiry, and access tracking.",
        ],
        "architecture": [
            "Modules write audit through shared middleware, domain-event handlers, and approved capture points.",
            "Modules do not create private audit tables.",
            "High-risk audit classes can use hash chaining or ledger-like tamper evidence.",
            "Audit reads are themselves audited.",
        ],
        "tables": [
            "audit.AuditRecord",
            "audit.AuditFieldChange",
            "audit.SecurityEvent",
            "audit.TimeMachineSnapshot",
            "audit.AuditExportRequest",
        ],
        "apis": [
            "GET /api/v1/audit/search",
            "GET /api/v1/audit/entities/{entityName}/{entityId}/history",
            "GET /api/v1/audit/security-events",
            "POST /api/v1/audit/exports",
            "POST /api/v1/audit/time-machine/reconstruct",
        ],
        "events": [
            "AuditRecordCreated",
            "SecurityEventRecorded",
            "TimeMachineSnapshotGenerated",
            "AuditExportRequested",
            "AuditExportDownloaded",
        ],
        "example": (
            "When payroll is published, the audit trail can show the run, source snapshot hash, rule versions, "
            "approver, exceptions, generated payslips, and every user who downloaded payroll evidence."
        ),
        "test_focus": [
            "Sensitive values are masked or encrypted and passwords/secrets are never stored.",
            "Entity history lookup is tenant-filtered and performant.",
            "Legal hold blocks purge and exports expire correctly.",
        ],
    },
    {
        "key": "EVENT-BUS",
        "title": "Event Bus and Transactional Outbox",
        "phase": "S2 foundation",
        "schema": "integration",
        "conclusion": (
            "The event backbone allows modules to communicate without direct database coupling. "
            "Phase 7A uses RabbitMQ first behind an event bus abstraction, with Azure Service Bus "
            "available later through adapter replacement."
        ),
        "deliverables": [
            "Event contract registry with versioned schemas and compatibility status.",
            "Transactional outbox so business change and event creation are atomic.",
            "Outbox publisher worker with retry, backoff, dead-letter handling, and replay approval.",
            "Inbox store for idempotent consumers.",
            "Tenant-scoped event metadata, classification, correlation, and causation ids.",
        ],
        "architecture": [
            "A module command writes domain data and OutboxEvent in the same database transaction.",
            "The publisher worker sends events to RabbitMQ through IEventBus.",
            "Consumers record InboxMessage before side effects to prevent duplicate processing.",
            "Event contracts are versioned; renaming or removing events needs deprecation planning.",
        ],
        "tables": [
            "integration.EventContract",
            "integration.OutboxEvent",
            "integration.InboxMessage",
            "integration.DeadLetterEvent",
            "integration.EventReplayRequest",
        ],
        "apis": [
            "GET /api/v1/integration/events/contracts",
            "GET /api/v1/integration/outbox",
            "GET /api/v1/integration/dead-letter",
            "POST /api/v1/integration/events/replay",
        ],
        "events": [
            "EmployeeCreated",
            "EmployeeAssignmentChanged",
            "LeaveApproved",
            "AttendanceSummaryApproved",
            "PayrollRunPublished",
            "ReportExportCreated",
        ],
        "example": (
            "When LeaveApproved is committed, the outbox event is committed with it. Payroll can consume "
            "the event later to update loss-of-pay input. If RabbitMQ is temporarily down, the outbox "
            "keeps the event pending until the worker retries."
        ),
        "test_focus": [
            "Business data and outbox event are atomic.",
            "Duplicate events are rejected by EventId and duplicate consumer work is blocked by InboxMessage.",
            "Dead-letter replay requires approval and preserves reason and audit trail.",
        ],
    },
    {
        "key": "RULE-ENGINE",
        "title": "Rule Engine",
        "phase": "S3 foundation",
        "schema": "rules",
        "conclusion": (
            "The Rule Engine prevents hardcoded business rules. Leave eligibility, attendance penalties, "
            "workflow routing, payroll formulas, statutory rules, feature flag evaluation, and compliance "
            "conditions are represented as versioned, effective-dated, testable configuration."
        ),
        "deliverables": [
            "Rule set and rule version lifecycle: draft, validate, simulate, approve, publish, rollback, deprecate.",
            "Decision tables, expression rules, JSON schema validation, and safe deterministic evaluation.",
            "Simulation workspace with explanations before publish.",
            "Runtime evaluation service for modules with tenant, version, correlation, and trace metadata.",
            "Evaluation logs with hashes and summaries for audit and troubleshooting.",
        ],
        "architecture": [
            "Modules call the shared Rule Evaluation API; they do not embed business thresholds in code.",
            "Rule Resolver selects the effective published version for tenant, module, date, and context.",
            "Evaluator returns outputs plus explanation metadata.",
            "Payroll and compliance rule versions are retained while referenced by payroll runs.",
        ],
        "tables": [
            "rules.RuleSet",
            "rules.RuleSetVersion",
            "rules.DecisionTable",
            "rules.RuleSimulation",
            "rules.RuleEvaluationLog",
        ],
        "apis": [
            "POST /api/v1/rules/rule-sets",
            "POST /api/v1/rules/{ruleSetId}/versions/{versionId}/simulate",
            "POST /api/v1/rules/{ruleSetId}/versions/{versionId}/submit",
            "POST /api/v1/rules/{ruleSetId}/versions/{versionId}/publish",
            "GET /api/v1/rules/evaluations/{correlationId}",
        ],
        "events": [
            "RuleSetVersionPublished",
            "RuleSetVersionDeprecated",
            "RuleSimulationCompleted",
            "RuleEvaluationFailed",
        ],
        "example": (
            "Instead of coding 'leave days greater than 5 needs HR approval', the tenant config can define "
            "a rule: if leave type is annual and duration exceeds the configured threshold, route to HR after "
            "manager approval. Changing the threshold is a rule version change, not a code change."
        ),
        "test_focus": [
            "Rule simulation produces deterministic outputs and explanations.",
            "Invalid JSON/schema payloads cannot be published.",
            "Runtime modules evaluate the intended effective version for date and tenant.",
        ],
    },
    {
        "key": "WORKFLOW",
        "title": "Workflow Studio",
        "phase": "S3 foundation and S9 hardening",
        "schema": "workflow",
        "conclusion": (
            "Workflow Studio is the approval and process engine for Phase 7A and future modules. "
            "It handles routed approvals, tasks, delegation, escalation, SLA timers, comments, decisions, "
            "versioned definitions, and outcome events."
        ),
        "deliverables": [
            "Workflow definition and published version lifecycle.",
            "Runtime workflow instances pinned to exact published version.",
            "Task inbox, decisions, delegation, reassignment, escalation, and SLA events.",
            "Workflow UI for designers, reviewers, task owners, and auditors.",
            "Outcome events that business modules can consume without direct coupling.",
        ],
        "architecture": [
            "Modules request workflow start and receive task/outcome callbacks or events.",
            "Workflow uses Rule Engine for routing, eligibility, and dynamic approver decisions.",
            "Workflow history links back to the source business entity.",
            "Published definitions are immutable; running instances do not change silently when a new version is published.",
        ],
        "tables": [
            "workflow.WorkflowDefinition",
            "workflow.WorkflowDefinitionVersion",
            "workflow.WorkflowInstance",
            "workflow.WorkflowTask",
            "workflow.WorkflowDecision",
            "workflow.WorkflowSlaEvent",
        ],
        "apis": [
            "POST /api/v1/workflows/definitions",
            "POST /api/v1/workflows/definitions/{id}/publish",
            "POST /api/v1/workflows/instances",
            "GET /api/v1/workflows/tasks",
            "POST /api/v1/workflows/tasks/{taskId}/decision",
        ],
        "events": [
            "WorkflowInstanceStarted",
            "WorkflowTaskAssigned",
            "WorkflowTaskDecided",
            "WorkflowSlaBreached",
            "WorkflowInstanceCompleted",
        ],
        "example": (
            "A payroll structure change can require maker-checker approval. Workflow creates a task for "
            "Payroll Reviewer, uses SLA rules for reminders, records the decision, and only then allows "
            "the salary structure version to be published."
        ),
        "test_focus": [
            "Running instance remains pinned to original workflow version.",
            "Delegation and escalation create correct task ownership and audit evidence.",
            "Task inbox respects assignee, role, delegate, tenant, and ABAC filters.",
        ],
    },
    {
        "key": "CONFIGURATION",
        "title": "Configuration-as-Data",
        "phase": "S3 foundation",
        "schema": "config",
        "conclusion": (
            "Configuration-as-Data makes tenant behavior changeable without core code edits. "
            "Forms, feature flags, module manifests, policy payloads, provider settings, UI slots, "
            "navigation, rules, and workflow references become governed data with schema validation "
            "and published versions."
        ),
        "deliverables": [
            "Module manifest registry for dependencies, features, APIs, events, and UI extension slots.",
            "Configuration schema registry using JSON Schema.",
            "Versioned configuration items with effective dates, approval, publish, rollback, export, and import.",
            "Tenant-aware feature flags aligned to OpenFeature concepts.",
            "Promotion path between sandbox and production with traceability.",
        ],
        "architecture": [
            "Runtime services resolve the effective published configuration through shared providers.",
            "Secrets are references to approved secret storage, never payload values.",
            "Configuration publish invalidates cache and emits events.",
            "Customer customization happens through configuration, feature flags, extensions, and plugins.",
        ],
        "tables": [
            "config.ModuleManifest",
            "config.ConfigurationSchema",
            "config.ConfigurationItem",
            "config.ConfigurationVersion",
            "config.FeatureFlag",
            "config.ConfigurationImportExport",
        ],
        "apis": [
            "GET /api/v1/configuration/schemas",
            "POST /api/v1/configuration/items",
            "POST /api/v1/configuration/versions/{id}/validate",
            "POST /api/v1/configuration/versions/{id}/publish",
            "POST /api/v1/configuration/import-export",
        ],
        "events": [
            "ConfigurationVersionPublished",
            "ConfigurationRollbackCompleted",
            "FeatureFlagChanged",
            "ModuleManifestRegistered",
            "ConfigurationImportCompleted",
        ],
        "example": (
            "A tenant can add a new onboarding form field or change leave policy display text by publishing "
            "a validated configuration version. Core HRMS code does not change."
        ),
        "test_focus": [
            "Published versions are immutable and schema-validated.",
            "Feature flags are tenant-scoped and audited.",
            "Import/export has approval, rollback, and no secret leakage.",
        ],
    },
    {
        "key": "CORE-HR",
        "title": "Core HR and Employee Self-Service",
        "phase": "S4 business module",
        "schema": "hr",
        "conclusion": (
            "Core HR is the employee master data module. It owns person, employee, assignment, organization, "
            "location, document metadata, and self-service change requests. Leave, attendance, payroll, "
            "workflow, rules, reports, and integrations consume Core HR through APIs/events, not direct ownership."
        ),
        "deliverables": [
            "Employee and person records with protected personal information.",
            "Effective-dated assignments, manager hierarchy, departments, designations, grades, locations, and legal entities.",
            "Employee self-service change requests routed through Workflow Studio.",
            "Employee document metadata with secure file references.",
            "Events for employee creation, update, assignment change, and lifecycle status.",
        ],
        "architecture": [
            "Core HR APIs call the Effective Dating Service for assignment and org history.",
            "Manager hierarchy queries use ABAC and hierarchy service, not unrestricted employee reads.",
            "Other modules consume Core HR APIs/events and do not duplicate master data.",
            "Search/report projections can be rebuilt from Core HR source plus events.",
        ],
        "tables": [
            "hr.Person",
            "hr.Employee",
            "hr.EmployeeAssignment",
            "hr.OrganizationUnit",
            "hr.Location",
            "hr.EssChangeRequest",
            "hr.EmployeeDocumentMetadata",
        ],
        "apis": [
            "GET /api/v1/hr/employees",
            "GET /api/v1/hr/employees/{id}?asOfDate=YYYY-MM-DD",
            "POST /api/v1/hr/ess/change-requests",
            "GET /api/v1/hr/organization-units",
            "GET /api/v1/hr/locations",
        ],
        "events": [
            "EmployeeCreated",
            "EmployeeUpdated",
            "EmployeeAssignmentChanged",
            "EmployeeStatusChanged",
            "EssChangeRequestApproved",
        ],
        "example": (
            "When an employee transfers to a new manager from next month, Core HR creates an effective-dated "
            "assignment change. Leave approvals before that date still route to the old manager; approvals "
            "after that date route to the new manager."
        ),
        "test_focus": [
            "Employee number is unique per tenant.",
            "Manager hierarchy and as-of assignment queries return correct historical state.",
            "Sensitive personal fields are encrypted, masked, and access controlled.",
        ],
    },
    {
        "key": "LEAVE",
        "title": "Leave Management",
        "phase": "S5 business module",
        "schema": "leave",
        "conclusion": (
            "Leave Management delivers the first end-to-end HR business workflow: policies, balances, "
            "applications, approvals, cancellation, adjustment, holiday calendars, payroll impact, and audit. "
            "It proves the platform foundations work together."
        ),
        "deliverables": [
            "Tenant-specific leave types, policy versions, eligibility, accrual, day-count, carry-forward, and approval workflow references.",
            "Leave request lifecycle: apply, validate, reserve, approve, reject, withdraw, cancel, and correct.",
            "Ledger-based leave transactions with rebuildable balance projections.",
            "Holiday calendars scoped by tenant and location.",
            "Payroll-impact events for unpaid leave, corrections, and balance-affecting decisions.",
        ],
        "architecture": [
            "Leave consumes Tenant, Identity, Effective Dating, Audit, Event Bus, Rule Engine, Workflow, Configuration, and Core HR.",
            "Balances are derived from immutable transactions, not manually overwritten totals.",
            "Rule Engine handles eligibility, accrual, day count, and carry-forward logic.",
            "Workflow handles approval routing; Event Bus publishes payroll and reporting impacts.",
        ],
        "tables": [
            "leave.LeaveType",
            "leave.LeavePolicyVersion",
            "leave.HolidayCalendar",
            "leave.Holiday",
            "leave.LeaveRequest",
            "leave.LeaveTransaction",
            "leave.LeaveBalanceProjection",
        ],
        "apis": [
            "GET /api/v1/leave/types",
            "GET /api/v1/leave/balances",
            "POST /api/v1/leave/requests",
            "POST /api/v1/leave/requests/{id}/withdraw",
            "GET /api/v1/leave/requests/{id}/history",
            "POST /api/v1/leave/policies/{id}/preview",
        ],
        "events": [
            "LeaveRequested",
            "LeaveApproved",
            "LeaveRejected",
            "LeaveCancelled",
            "LeaveBalanceChanged",
            "LeavePayrollImpactReady",
        ],
        "example": (
            "An employee applies for 3 days annual leave. The system checks eligibility and calendar, reserves "
            "3 days in the ledger, starts workflow, and after approval debits the ledger. If the request is "
            "cancelled before payroll cutoff, a reversing ledger transaction and payroll-impact event are created."
        ),
        "test_focus": [
            "Duplicate requests cannot double-reserve or double-debit balance.",
            "Ledger can rebuild projections exactly.",
            "Policy versions support historical and future-dated rules.",
        ],
    },
    {
        "key": "ATTENDANCE",
        "title": "Attendance and First Connector",
        "phase": "S6 business module",
        "schema": "attendance",
        "conclusion": (
            "Attendance captures raw punches, reconciles daily attendance summaries, supports regularization "
            "requests, and feeds payroll. The first connector framework proves how future devices or providers "
            "can be added through adapters and configuration."
        ),
        "deliverables": [
            "Attendance policy versions linked to rules and calendars.",
            "Device and connector configuration with secret references.",
            "Raw punch ingestion with deduplication and immutability.",
            "Daily summary calculation for present, absent, late, early leave, work minutes, and payroll impact.",
            "Regularization workflow for employee corrections and manager/HR approval.",
        ],
        "architecture": [
            "Connector/Web/API input flows into Punch Ingestion, Raw Punch Store, Attendance Engine, Rules, and Payroll Events.",
            "Raw punches are immutable; corrections are approved regularization records.",
            "Daily summaries are rebuildable from raw punches plus approved adjustments.",
            "Connector adapters are provider-specific; business logic stays provider-neutral.",
        ],
        "tables": [
            "attendance.AttendancePolicyVersion",
            "attendance.AttendanceDevice",
            "attendance.RawPunch",
            "attendance.AttendanceDaySummary",
            "attendance.RegularizationRequest",
            "attendance.ConnectorSyncRun",
        ],
        "apis": [
            "POST /api/v1/attendance/punches",
            "GET /api/v1/attendance/summaries",
            "POST /api/v1/attendance/regularization-requests",
            "GET /api/v1/attendance/connectors/sync-runs",
            "POST /api/v1/attendance/reconciliation/run",
        ],
        "events": [
            "RawPunchReceived",
            "AttendanceSummaryCalculated",
            "RegularizationRequested",
            "RegularizationApproved",
            "AttendancePayrollImpactReady",
            "ConnectorSyncCompleted",
        ],
        "example": (
            "A biometric device sends the same punch twice. The unique external punch key marks the duplicate "
            "without double-counting work time. If the employee forgot checkout, they submit regularization, "
            "workflow approves it, and the daily summary is recalculated for payroll."
        ),
        "test_focus": [
            "Duplicate external punches are detected and do not double count.",
            "Summary rebuild produces consistent payroll-impact results.",
            "Connector failures and sync gaps are auditable and recoverable.",
        ],
    },
    {
        "key": "SHIFT-FOUNDATION",
        "title": "Shift Foundation",
        "phase": "S6-S8 foundation",
        "schema": "attendance",
        "conclusion": (
            "Shift Foundation defines basic shift templates, employee shift assignments, exceptions, "
            "and shift resolution. It is intentionally included in Phase 7A because attendance and "
            "payroll cannot be reliable without knowing which shift applied to an employee on a date. "
            "Advanced roster planning, workforce demand planning, and shift swaps remain later-phase work."
        ),
        "deliverables": [
            "Configurable shift definitions with start/end time, grace rules, break handling, night shift flag, timezone, and effective versions.",
            "Effective-dated employee shift assignments linked to branch, department, role, or employee where permitted.",
            "Controlled one-day or temporary shift overrides routed through workflow when tenant policy requires approval.",
            "Shift resolver service used by attendance summary calculation, regularization, reports, and payroll source snapshots.",
            "Audit, events, and explainability for which shift was used in a daily attendance or payroll result.",
        ],
        "architecture": [
            "Attendance asks the Shift Resolver for the effective shift before calculating late, early, absent, night, overtime, or payroll-impact values.",
            "Shift definitions are versioned and effective-dated so past attendance and payroll results remain reproducible.",
            "Branch and role defaults can be overridden by employee-specific assignments when allowed by tenant policy.",
            "Payroll consumes shift-aware attendance summaries, not raw shift rules, so published payroll stays explainable.",
        ],
        "tables": [
            "attendance.ShiftDefinition",
            "attendance.ShiftDefinitionVersion",
            "attendance.EmployeeShiftAssignment",
            "attendance.EmployeeShiftOverride",
            "attendance.ShiftResolutionLog",
        ],
        "apis": [
            "GET /api/v1/attendance/shifts",
            "POST /api/v1/attendance/shifts",
            "POST /api/v1/attendance/shifts/{id}/publish",
            "POST /api/v1/attendance/shift-assignments",
            "POST /api/v1/attendance/shift-overrides",
            "GET /api/v1/attendance/employees/{employeeId}/shift?date=YYYY-MM-DD",
        ],
        "events": [
            "ShiftDefinitionPublished",
            "ShiftDefinitionRetired",
            "EmployeeShiftAssigned",
            "EmployeeShiftAssignmentChanged",
            "ShiftOverrideApproved",
            "ShiftPayrollImpactChanged",
        ],
        "example": (
            "An employee is assigned to a 10:00 to 19:00 shift for July. If they punch in at 10:20, "
            "attendance applies that shift's grace rule. If the employee is temporarily assigned to a night "
            "shift for one day, the approved override is used only for that date and payroll can explain the result."
        ),
        "test_focus": [
            "Effective shift resolution chooses employee override, employee assignment, branch default, and tenant default in the approved priority order.",
            "Overnight shifts calculate work date, late arrival, early exit, and payable minutes correctly.",
            "Payroll snapshots reference the shift-aware attendance summary and remain reproducible after shift rules change.",
        ],
    },
    {
        "key": "PAYROLL",
        "title": "Payroll and India Compliance",
        "phase": "S7-S8 business module",
        "schema": "payroll",
        "conclusion": (
            "Payroll is the highest-risk Phase 7A business module. It calculates employee payroll from Core HR, "
            "Leave, Attendance, salary structures, declarations, and effective-dated statutory rules. "
            "Published payroll must be reproducible, explainable, immutable, and compliant with the India-first foundation."
        ),
        "deliverables": [
            "Payroll calendars, periods, cutoff, dry run, approval, lock, publish, and correction flow.",
            "Salary components, salary structure versions, and effective-dated employee salary assignments.",
            "Source snapshot for Core HR, Leave, Attendance, and component inputs.",
            "Calculation engine for earnings, deductions, arrears, LOP, statutory components, and exceptions.",
            "India compliance foundation: PF, ESI, PT, LWF, TDS, Form 16, FBP, and revisions where applicable.",
            "Payslip generation and employee access controls.",
        ],
        "architecture": [
            "Payroll consumes Core HR, Leave, Attendance, Rule Engine, Workflow, Audit, and Event Bus.",
            "The run captures source snapshot hash and rule-version snapshot before calculation.",
            "Rule Engine evaluates salary, eligibility, statutory, and tax logic.",
            "Workflow approves sensitive configuration and payroll run publish.",
            "Published runs are immutable; corrections create adjustment runs or controlled correction records.",
        ],
        "tables": [
            "payroll.PayrollCalendar",
            "payroll.PayPeriod",
            "payroll.SalaryComponent",
            "payroll.SalaryStructureVersion",
            "payroll.EmployeeSalaryAssignment",
            "payroll.PayrollRun",
            "payroll.PayrollRunEmployee",
            "payroll.PayrollRunComponent",
            "payroll.StatutoryRuleVersion",
            "payroll.Payslip",
        ],
        "apis": [
            "POST /api/v1/payroll/runs/dry-run",
            "POST /api/v1/payroll/runs/{id}/approve",
            "POST /api/v1/payroll/runs/{id}/publish",
            "GET /api/v1/payroll/runs/{id}/employees/{employeeId}/explain",
            "GET /api/v1/payroll/payslips",
            "POST /api/v1/payroll/statutory-rule-versions",
        ],
        "events": [
            "PayrollRunStarted",
            "PayrollRunCalculated",
            "PayrollRunExceptionRaised",
            "PayrollRunApproved",
            "PayrollRunPublished",
            "PayslipPublished",
        ],
        "example": (
            "For June payroll, the run snapshots employee assignments, approved leave loss-of-pay, attendance "
            "summaries, salary assignments, declarations, and statutory rule versions. A future salary change "
            "effective July does not change June results. After publish, June payroll is locked; corrections go "
            "through a revision or adjustment process."
        ),
        "test_focus": [
            "Published payroll can be reproduced from source and rule snapshots.",
            "Unauthorized users cannot see payroll data outside legal entity, payroll group, or employee-self scope.",
            "Statutory rule versions are effective-dated and cannot be purged while referenced.",
            "Explain-calculation returns lineage for each component.",
        ],
    },
    {
        "key": "REPORTING",
        "title": "Standard Reports",
        "phase": "S10 business module",
        "schema": "reporting",
        "conclusion": (
            "Standard Reports provide the first governed reporting layer. Reports are versioned, permissioned, "
            "tenant-scoped, export-controlled, and supported by rebuildable projections. Reporting uses approved "
            "APIs, events, and read models rather than unsafe direct cross-module coupling."
        ),
        "deliverables": [
            "Report catalog with definitions, parameters, classifications, permissions, and versions.",
            "Report run and export flow with status, purpose, expiry, and audit.",
            "Employee and payroll projections for common operational/statutory reports.",
            "As-of reporting using Effective Dating.",
            "Export controls for sensitive data, approvals where required, download limits, and expiration.",
        ],
        "architecture": [
            "Module events and approved APIs feed reporting projections.",
            "Report Query Service applies tenant, RBAC, ABAC, filters, pagination, and masking.",
            "Export Service is asynchronous and audited.",
            "Projection Builder can rebuild read models from source modules/events.",
        ],
        "tables": [
            "reporting.ReportDefinition",
            "reporting.ReportDefinitionVersion",
            "reporting.ReportRun",
            "reporting.ReportExport",
            "reporting.EmployeeReportProjection",
            "reporting.PayrollReportProjection",
        ],
        "apis": [
            "GET /api/v1/reports/catalog",
            "POST /api/v1/reports/{reportCode}/run",
            "GET /api/v1/reports/runs/{runId}",
            "POST /api/v1/reports/runs/{runId}/export",
            "GET /api/v1/reports/exports/{exportId}/download",
        ],
        "events": [
            "ReportRunRequested",
            "ReportRunCompleted",
            "ReportExportCreated",
            "ReportExportDownloaded",
            "ReportProjectionRebuilt",
        ],
        "example": (
            "A payroll summary report uses the payroll projection linked to the exact payroll run and rule snapshot. "
            "An HR admin with the correct legal-entity scope can export it with a purpose and expiry; the export "
            "download is audited."
        ),
        "test_focus": [
            "Report results are tenant-scoped, paginated, masked, and permission-filtered.",
            "As-of report dates match Effective Dating service results.",
            "Exports expire and access logs are complete.",
        ],
    },
]


HARDENING_DOCS = [
    (
        "API, Event, NFR, and Runbook Standard",
        "docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md",
        "Every module must define versioned APIs, event contracts, error responses, non-functional targets, observability, and runbook expectations.",
    ),
    (
        "Database Classification, Migration, and Rollback Standard",
        "docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md",
        "Every database design must classify data, protect PII/payroll data, define migrations, rollback, verification, retention, and legal-hold behavior.",
    ),
    (
        "UI Accessibility and States Standard",
        "docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md",
        "Every UI must handle loading, empty, error, permission-denied, approval, audit, responsive, and accessibility states.",
    ),
    (
        "Testing Traceability and Abuse Standard",
        "docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md",
        "Tests must trace requirements to scenarios and include tenant isolation, abuse, negative, security, performance, and recovery cases.",
    ),
    (
        "Phase 7A Hardening Backlog",
        "docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md",
        "Module-specific hardening items are tracked without blocking the approval gate, but they must be considered during implementation planning.",
    ),
]


EXTERNAL_REFERENCES = [
    "Microsoft SQL Server Row-Level Security - https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security",
    "Microsoft SQL Server Temporal Tables - https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables",
    "Microsoft SQL Server Ledger - https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview",
    "OpenAPI Specification - https://spec.openapis.org/oas/latest.html",
    "CloudEvents - https://cloudevents.io/",
    "RabbitMQ Reliability Guide - https://www.rabbitmq.com/docs/reliability",
    "JSON Schema - https://json-schema.org/",
    "OpenFeature Specification - https://openfeature.dev/specification/",
    "OWASP API Security Top 10 - https://owasp.org/API-Security/editions/2023/en/0x11-t10/",
    "WCAG 2.2 - https://www.w3.org/TR/WCAG22/",
    "EPFO India - https://www.epfindia.gov.in/site_en/index.php",
    "Income Tax Department India - https://www.incometax.gov.in/iec/foportal/",
    "Web visual: Wikimedia Commons team meeting photo - WLM international team meeting Vienna 2023-05-27",
    "Web visual: Wikimedia Commons server infrastructure photo - Wikimedia Servers-0051 19",
]


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#12395b"),
            alignment=TA_CENTER,
            spaceAfter=16,
        )
    )
    base.add(
        ParagraphStyle(
            "CoverSub",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=17,
            textColor=colors.HexColor("#4b5563"),
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    base.add(
        ParagraphStyle(
            "H1x",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#0b5cad"),
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "H2x",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13.5,
            leading=17,
            textColor=colors.HexColor("#12395b"),
            spaceBefore=8,
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            "H3x",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=6,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            "Bodyx",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=12.3,
            textColor=colors.HexColor("#20242a"),
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            "Smallx",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9.5,
            textColor=colors.HexColor("#374151"),
            spaceAfter=3,
        )
    )
    base.add(
        ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=12.4,
            textColor=colors.HexColor("#0f172a"),
            backColor=colors.HexColor("#eaf2fb"),
            borderColor=colors.HexColor("#c9d9eb"),
            borderWidth=0.5,
            borderPadding=7,
            spaceBefore=4,
            spaceAfter=7,
        )
    )
    base.add(
        ParagraphStyle(
            "CodexCode",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.2,
            leading=8.8,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#f3f4f6"),
            borderColor=colors.HexColor("#d1d5db"),
            borderWidth=0.5,
            borderPadding=5,
        )
    )
    return base


S = styles()


def p(text, style="Bodyx"):
    return Paragraph(text.replace("&", "&amp;"), S[style])


def bullets(items):
    return [p("- " + item, "Bodyx") for item in items]


def small_bullets(items):
    return [p("- " + item, "Smallx") for item in items]


def table(rows, widths=None, header=True, small=True):
    cell_style = S["Smallx"] if small else S["Bodyx"]
    converted = []
    for row in rows:
        converted.append([Paragraph(str(cell).replace("&", "&amp;"), cell_style) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5edf6")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#12395b")),
            ]
        )
    t.setStyle(TableStyle(commands))
    return t


def code(text):
    return Preformatted(text, S["CodexCode"])


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(0.62 * inch, 0.42 * inch, "HRMS Platform - Phase 7A Approved AI Source Reference")
    canvas.drawRightString(width - 0.62 * inch, 0.42 * inch, f"Page {doc.page}")
    canvas.restoreState()


def source_paths_for(module_key):
    return [
        f"docs/02-product-requirements/FEAT-{module_key}-001-business-requirements.md",
        f"docs/09-development/TECH-{module_key}-001-technical-design.md",
        f"docs/06-database/DB-DESIGN-{module_key}-001.md",
        f"docs/07-ui-ux/UI-{module_key}-001-screens.md",
        f"docs/10-testing/TEST-{module_key}-001-test-plan.md",
    ]


def add_cover(story):
    story.append(Spacer(1, 0.45 * inch))
    story.append(p("Phase 7A Approved AI Source Reference", "CoverTitle"))
    story.append(
        p(
            "Complete consolidated conclusion of the approved Phase 7A HRMS module documents, written for AI retrieval and human review.",
            "CoverSub",
        )
    )
    story.append(
        p(
            "Covers approved delivery scope, architecture, database model, APIs, events, user operations, examples, controls, and implementation guardrails.",
            "CoverSub",
        )
    )
    if TEAM_IMAGE.exists():
        img = Image(str(TEAM_IMAGE), width=5.45 * inch, height=2.75 * inch)
        img.hAlign = "CENTER"
        story.append(Spacer(1, 0.15 * inch))
        story.append(img)
        story.append(p("Web visual: Wikimedia Commons team meeting photo, used as a collaboration visual.", "Smallx"))
    story.append(Spacer(1, 0.2 * inch))
    story.append(
        table(
            [
                ["Document role", "AI source reference and stakeholder reference"],
                ["Status basis", "Summarizes approved Phase 7A documentation"],
                ["Module packs covered", "15 module packs x 5 approved docs = 75 module documents"],
                ["Shared hardening covered", "5 approved standards/backlog documents"],
                ["Language style", "Simple, explicit, searchable, and implementation-oriented"],
            ],
            widths=[1.75 * inch, 4.55 * inch],
            header=False,
            small=False,
        )
    )
    story.append(PageBreak())


def add_intro(story):
    story.append(p("1. Executive Conclusion", "H1x"))
    story.append(
        p(
            "Phase 7A is the first development phase that turns the HRMS platform from approved design into a working enterprise foundation. It is not only a set of HR screens. It delivers the platform base required for a configurable, multi-tenant, auditable HRMS, and then builds the first business modules on top of that base."
        )
    )
    story.append(
        p(
            "The approved outcome is: build Tenant Catalog and RLS, Branch / Office Hierarchy, Identity and Access, Effective Dating, Audit and Time Machine, Event Bus and Outbox, Rule Engine, Workflow Studio, Configuration-as-Data, Core HR and ESS, Leave, Attendance, Shift Foundation, Payroll with India compliance foundation, and Standard Reports."
        )
    )
    story.append(
        p(
            "This PDF is intentionally more detailed than the presentation brief. It is suitable as an AI source because each module section uses consistent labels: conclusion, approved delivery, architecture, database, API, events, UI operation, example, and test focus."
        )
    )
    story.append(
        p(
            "Canonical rule: if this PDF conflicts with an approved source document, the approved source document remains the legal design authority. This PDF is a consolidated reference, not a replacement for the source files."
        , "Callout")
    )

    story.append(p("2. Who Phase 7A Serves", "H1x"))
    story.append(
        table(
            [
                ["User group", "What Phase 7A gives them"],
                ["Employees", "Self-service profile changes, leave requests, attendance visibility, payslips, and request status."],
                ["Managers", "Team approvals, leave and attendance decisions, shift-aware attendance visibility, team information, and task inbox."],
                ["HR admins", "Employee master data, policies, workflows, configuration, calendars, reports, and evidence."],
                ["Payroll teams", "Payroll setup, dry runs, exception review, approvals, publish, payslips, and compliance evidence."],
                ["Tenant admins", "Tenant setup, branch/office hierarchy, feature flags, provider configuration, branding, security, and controlled changes."],
                ["Auditors and security teams", "Audit trails, time-machine reconstruction, access evidence, exports, and investigation support."],
            ],
            widths=[1.6 * inch, 4.8 * inch],
        )
    )

    story.append(p("3. Phase 7A Development Order", "H1x"))
    story.append(
        table(
            [
                ["Sprint", "Theme", "Reason"],
                ["S1", "Tenant + Identity + Branch scope", "No business module can be safely built without tenant context, RLS, branch scope, authentication, RBAC, and ABAC."],
                ["S2", "Effective Dating + Audit + Events", "History, evidence, and event reliability must exist before modules create important business records."],
                ["S3", "Rule Engine + Workflow + Configuration", "Business behavior must be configurable and approval-driven before Leave, Attendance, and Payroll depend on it."],
                ["S4", "Core HR + ESS", "Employee master data, branch assignments, and job assignments are required by downstream modules."],
                ["S5", "Leave", "First complete HR workflow using rules, workflow, balances, payroll impact, and audit."],
                ["S6", "Attendance + Shift Foundation + first connector", "Shift-aware time input and summaries are needed for reliable payroll."],
                ["S7", "Payroll engine", "Calculates payroll using Core HR, Leave, Attendance, rules, and snapshots."],
                ["S8", "India compliance foundation", "Adds statutory packs and compliance outputs on top of payroll engine."],
                ["S9", "Workflow hardening", "Strengthens delegation, SLA, escalation, migration, and process resilience."],
                ["S10", "Reports + release hardening", "Delivers standard reports, exports, performance, security, and release readiness."],
            ],
            widths=[0.55 * inch, 1.6 * inch, 4.25 * inch],
        )
    )


def add_inventory(story):
    story.append(PageBreak())
    story.append(p("4. Approved Source Document Inventory", "H1x"))
    story.append(
        p(
            "Each Phase 7A module pack has five approved documents: Business Requirements, Technical Design, Database Design, UI Design, and Test Plan. The PDF summarizes their conclusions; the paths below identify the source documents used."
        )
    )
    rows = [["Module", "Business", "Technical", "Database", "UI", "Test"]]
    for module in MODULES:
        key = module["key"]
        rows.append(
            [
                module["title"],
                f"FEAT-{key}-001",
                f"TECH-{key}-001",
                f"DB-DESIGN-{key}-001",
                f"UI-{key}-001",
                f"TEST-{key}-001",
            ]
        )
    story.append(table(rows, widths=[1.8 * inch, 0.92 * inch, 0.92 * inch, 1.0 * inch, 0.75 * inch, 0.75 * inch]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(p("Shared hardening documents approved for Phase 7A:", "H2x"))
    story.append(
        table(
            [["Document", "Path", "Purpose"]]
            + [[title, path, purpose] for title, path, purpose in HARDENING_DOCS],
            widths=[1.5 * inch, 2.1 * inch, 2.9 * inch],
        )
    )


def add_architecture(story):
    story.append(PageBreak())
    story.append(p("5. Platform Architecture Conclusion", "H1x"))
    if SERVER_IMAGE.exists():
        img = Image(str(SERVER_IMAGE), width=5.9 * inch, height=2.45 * inch)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(p("Web visual: Wikimedia Commons server infrastructure photo, used as a platform architecture visual.", "Smallx"))
    story.append(
        p(
            "The approved architecture is a modular, configurable, event-aware HRMS platform. The backend is .NET-first, the frontend is React/Next.js/TypeScript, the primary database is SQL Server, cache is Redis, messaging is RabbitMQ first with Azure Service Bus optional later, storage uses Azure Blob Storage, search uses Elasticsearch, and OpenAPI documentation is mandatory for every API."
        )
    )
    story.append(p("5.1 Simple Architecture View", "H2x"))
    story.append(
        code(
            "User / Browser / API Client\n"
            "  -> Next.js / React UI and API Gateway\n"
            "  -> .NET Application Services and Module APIs\n"
            "  -> Shared Platform Services\n"
            "       Tenant Context + RLS\n"
            "       Identity + RBAC + ABAC\n"
            "       Effective Dating\n"
            "       Audit + Time Machine\n"
            "       Event Bus + Outbox\n"
            "       Rule Engine\n"
            "       Workflow Studio\n"
            "       Configuration-as-Data\n"
            "  -> Business Modules\n"
            "       Core HR, Branch/Office, Leave, Attendance, Shift Foundation, Payroll, Reports\n"
            "  -> SQL Server, Redis, RabbitMQ, Blob Storage, Search, Observability\n"
        )
    )
    story.append(p("5.2 Architectural Principles Approved", "H2x"))
    story.extend(
        bullets(
            [
                "Tenant isolation is mandatory at request, service, database, cache, event, storage, search, job, report, and telemetry levels.",
                "Customer customization uses configuration, feature flags, extensions, plugins, provider adapters, and manifests; core logic must not be changed per customer.",
                "Business rules are stored and versioned in the Rule Engine or configuration; no hardcoded policy thresholds in product code.",
                "Workflow is a platform service used by many modules, not a feature hidden inside Leave or Payroll.",
                "Published rules, workflow definitions, payroll runs, and high-risk configuration versions are immutable.",
                "Effective dating and time-machine capability are required from the beginning because adding them later is costly and risky.",
                "Every module must expose versioned OpenAPI contracts, support RBAC/ABAC, create audit records, and participate in test traceability.",
            ]
        )
    )
    story.append(p("5.3 Plug-and-Play Extension Model", "H2x"))
    story.append(
        p(
            "Future modules can be ingested by registering a module manifest, defining API and event contracts, adding tenant-scoped schema tables, using shared authorization/audit/effective-dating services, and publishing UI extension slots. Existing core services should be extended through interfaces and configuration rather than edited for a customer-specific requirement."
        )
    )


def add_database_architecture(story):
    story.append(PageBreak())
    story.append(p("6. Database Architecture Conclusion", "H1x"))
    story.append(
        p(
            "The database design is SQL Server-first and enterprise-oriented. It uses schemas to separate platform foundations and business modules. Every tenant-scoped table includes TenantId and is protected by RLS. Important time-changing facts use effective dating and, where approved, SQL Server temporal history. Published business results are immutable or corrected through controlled adjustment records."
        )
    )
    story.append(p("6.1 Approved Schema Map", "H2x"))
    story.append(
        table(
            [
                ["Schema", "Purpose"],
                ["catalog", "Tenant catalog, placement, feature flags, branding, provider config, provider health."],
                ["security", "Users, roles, permissions, ABAC policies, branch scopes, sessions, delegation, impersonation, break glass."],
                ["org", "Branch and office hierarchy, hierarchy closure, employee branch assignment, scoped administration evidence."],
                ["core", "Effective-dated entity registration, change requests, conflicts, shared platform facts."],
                ["audit", "Audit records, field changes, security events, time-machine snapshots, export requests."],
                ["integration", "Event contracts, outbox, inbox, dead letters, replay requests."],
                ["rules", "Rule sets, rule versions, decision tables, simulations, evaluation logs."],
                ["workflow", "Workflow definitions, versions, instances, tasks, decisions, SLA events."],
                ["config", "Module manifests, schemas, configuration items/versions, feature flags, import/export."],
                ["hr", "Person, employee, assignment, org units, locations, ESS requests, document metadata."],
                ["leave", "Leave types, policies, calendars, requests, transactions, balance projections."],
                ["attendance", "Attendance policies, shifts, shift assignments, devices, raw punches, day summaries, regularization, sync runs."],
                ["payroll", "Calendars, periods, components, structures, salary assignments, runs, components, payslips."],
                ["reporting", "Report definitions, runs, exports, employee and payroll projections."],
            ],
            widths=[1.15 * inch, 5.25 * inch],
        )
    )
    story.append(p("6.2 Tenant Isolation Example", "H2x"))
    story.append(
        code(
            "Request resolves TenantId on the server.\n"
            "Database connection sets SESSION_CONTEXT('TenantId').\n"
            "Every tenant table has TenantId.\n"
            "RLS FILTER predicate hides other tenants' rows.\n"
            "RLS BLOCK predicate prevents wrong-tenant inserts/updates.\n"
            "EF query filters and service checks are additional defense, not replacement.\n"
        )
    )
    story.append(p("6.3 Effective Dating Example", "H2x"))
    story.append(
        code(
            "hr.EmployeeAssignment\n"
            "  EmployeeId = E100\n"
            "  Department = Sales\n"
            "  EffectiveFrom = 2026-01-01\n"
            "  EffectiveTo = 2026-06-30\n\n"
            "hr.EmployeeAssignment\n"
            "  EmployeeId = E100\n"
            "  Department = Finance\n"
            "  EffectiveFrom = 2026-07-01\n"
            "  EffectiveTo = NULL\n\n"
            "As-of 2026-06-30 -> Sales\n"
            "As-of 2026-07-01 -> Finance\n"
            "History explains approval, reason, old row, new row, and audit trail.\n"
        )
    )
    story.append(p("6.4 Leave Ledger Example", "H2x"))
    story.append(
        code(
            "Leave balance is not overwritten.\n"
            "Opening balance transaction: +12.0\n"
            "Approved leave request: -3.0\n"
            "Cancellation or correction: +3.0 or adjustment transaction\n"
            "Projection = sum of ledger transactions by employee, leave type, and as-of date.\n"
            "If projection is wrong, rebuild it from leave.LeaveTransaction.\n"
        )
    )
    story.append(p("6.5 Payroll Reproducibility Example", "H2x"))
    story.append(
        code(
            "PayrollRun stores:\n"
            "  PayPeriodId\n"
            "  SourceSnapshotHash\n"
            "  RuleVersionSnapshotJson\n"
            "  Status and approval evidence\n\n"
            "PayrollRunEmployee stores employee totals.\n"
            "PayrollRunComponent stores exact component amounts.\n"
            "Published payroll is immutable.\n"
            "Corrections use adjustment runs or controlled correction records.\n"
        )
    )


def add_common_operation(story):
    story.append(PageBreak())
    story.append(p("7. Common Operating Model", "H1x"))
    story.append(
        p(
            "Phase 7A uses a repeatable business pattern so users see simple actions while the platform enforces governance behind the scenes."
        )
    )
    story.append(
        code(
            "Configure -> Request -> Validate -> Approve -> Calculate -> Publish -> Audit\n\n"
            "Configure: admin publishes tenant policy, form, rule, workflow, feature, or provider settings.\n"
            "Request: employee, manager, HR, payroll, connector, or job submits a business action.\n"
            "Validate: tenant, RBAC, ABAC, rule engine, dates, schema, and idempotency are checked.\n"
            "Approve: workflow routes tasks, delegation, SLA, and maker-checker decisions.\n"
            "Calculate: leave balance, attendance summary, payroll result, or report projection is produced.\n"
            "Publish: approved output becomes visible or exportable.\n"
            "Audit: every important step is traceable with tenant and correlation id.\n"
        )
    )
    story.append(p("7.1 End-to-End Example: Leave to Payroll", "H2x"))
    story.extend(
        bullets(
            [
                "Employee submits leave request from UI.",
                "Tenant, identity, role, ABAC, leave policy, day-count rules, and calendar are validated.",
                "Leave ledger reserves requested days and workflow assigns approval task.",
                "Manager approves; leave ledger debits balance and LeaveApproved event is written to outbox.",
                "Payroll consumes the approved event and treats unpaid or loss-of-pay impact during the payroll source snapshot.",
                "Reports can show leave history and payroll impact with audit evidence.",
            ]
        )
    )
    story.append(p("7.2 End-to-End Example: Attendance to Payroll", "H2x"))
    story.extend(
        bullets(
            [
                "Connector imports raw punches from a configured device.",
                "Duplicate punch detection prevents double counting.",
                "Attendance engine resolves the employee's effective shift and calculates day summary using tenant rules.",
                "Employee regularization requests follow workflow if correction is needed.",
                "Approved day summary produces payroll-impact event.",
                "Payroll snapshots shift-aware attendance data at cutoff and can explain late/absence impact.",
            ]
        )
    )


def add_module(story, index, module):
    story.append(PageBreak())
    story.append(p(f"{8 + index}. {module['title']}", "H1x"))
    story.append(p(f"Phase: {module['phase']} | Schema: {module['schema']} | Approved source key: {module['key']}", "Smallx"))
    story.append(p("Approved conclusion", "H2x"))
    story.append(p(module["conclusion"]))
    story.append(p("Approved delivery", "H2x"))
    story.extend(bullets(module["deliverables"]))
    story.append(p("Architecture and dependencies", "H2x"))
    story.extend(bullets(module["architecture"]))
    story.append(p("Database model", "H2x"))
    story.append(table([["Key tables / records"]] + [[item] for item in module["tables"]], widths=[6.4 * inch]))
    story.append(p("API and OpenAPI examples", "H2x"))
    story.extend(small_bullets(module["apis"]))
    story.append(p("Event examples", "H2x"))
    story.extend(small_bullets(module["events"]))
    story.append(p("Example scenario", "H2x"))
    story.append(p(module["example"], "Callout"))
    story.append(p("Test and quality focus", "H2x"))
    story.extend(bullets(module["test_focus"]))
    story.append(p("Source document paths", "H2x"))
    story.extend(small_bullets(source_paths_for(module["key"])))


def add_quality_and_ai_source_guidance(story, section_start):
    story.append(PageBreak())
    story.append(p(f"{section_start}. Security, Quality, and Hardening Rules", "H1x"))
    story.extend(
        bullets(
            [
                "Every API must be versioned, documented in OpenAPI, tested, and protected by tenant, RBAC, ABAC, and audit controls.",
                "Unit test coverage target is at least 85 percent, with higher scrutiny for payroll, security, RLS, rules, workflow, effective dating, and audit.",
                "Integration tests must verify cross-module flows such as leave to payroll, attendance to payroll, workflow outcome to business state, and event retries.",
                "End-to-end tests must cover user workflows for employee, manager, HR admin, payroll, tenant admin, and auditor roles.",
                "Security tests must cover cross-tenant abuse, privilege escalation, IDOR, brute force, session misuse, export misuse, and sensitive data masking.",
                "Performance tests must cover tenant lookup, RLS queries, rule evaluation, workflow inbox, event lag, report exports, and payroll runs.",
                "Runbooks are required for provider outage, database failover, event backlog, dead-letter replay, payroll publish issue, export incident, and tenant suspension.",
            ]
        )
    )
    story.append(p(f"{section_start + 1}. What Is Not Part of Phase 7A", "H1x"))
    story.extend(
        bullets(
            [
                "Recruitment, applicant tracking, advanced onboarding, performance, LMS, engagement, expenses, assets, service desk, advanced BI, advanced roster planning, shift swaps, workforce demand planning, and marketplace are later modules.",
                "Multi-country payroll packs are later; Phase 7A establishes India-first payroll and compliance foundation.",
                "Advanced autonomous AI agents and AI-driven HR decisions are not part of Phase 7A business module delivery.",
                "Customer-specific code changes are not allowed; customization must use configuration, extensions, feature flags, providers, or plugins.",
            ]
        )
    )
    story.append(p(f"{section_start + 2}. How AI Should Use This PDF", "H1x"))
    story.extend(
        bullets(
            [
                "Treat this as a consolidated approved Phase 7A reference, not as raw implementation code.",
                "When answering about scope, use the 15 module names in this document.",
                "When answering about database, mention schemas, TenantId, RLS, effective dating, audit, and immutability where relevant.",
                "When answering about architecture, explain shared platform services before business modules.",
                "When answering about customization, say configuration, feature flags, extensions, providers, and plugins are preferred; core code changes are prohibited for customer-specific behavior.",
                "When answering about sequencing, say foundations come before business modules and phase gates cannot be skipped.",
                "Do not use old launch-scope language. Use Phase 7A, later phases, or approved phase terminology.",
                "If asked for exact legal wording, source paths, or full requirements, refer back to the approved source documents.",
            ]
        )
    )
    story.append(p(f"{section_start + 3}. External and Web References", "H1x"))
    story.extend(small_bullets(EXTERNAL_REFERENCES))


def build_markdown():
    lines = [
        "# Phase 7A Approved AI Source Reference",
        "",
        "This Markdown mirrors the generated PDF and is provided for reliable AI ingestion.",
        "",
        "## Executive Conclusion",
        "Phase 7A delivers the enterprise HRMS platform foundation plus branch/office hierarchy, shift foundation, and the first business operations: Core HR, Leave, Attendance, Payroll, and Standard Reports.",
        "",
        "## Modules",
    ]
    for module in MODULES:
        lines.extend(
            [
                "",
                f"### {module['title']}",
                f"Phase: {module['phase']}",
                f"Schema: {module['schema']}",
                "",
                f"Conclusion: {module['conclusion']}",
                "",
                "Approved delivery:",
                *[f"- {item}" for item in module["deliverables"]],
                "",
                "Architecture:",
                *[f"- {item}" for item in module["architecture"]],
                "",
                "Database model:",
                *[f"- {item}" for item in module["tables"]],
                "",
                "API examples:",
                *[f"- {item}" for item in module["apis"]],
                "",
                "Event examples:",
                *[f"- {item}" for item in module["events"]],
                "",
                f"Example: {module['example']}",
                "",
                "Test focus:",
                *[f"- {item}" for item in module["test_focus"]],
                "",
                "Source documents:",
                *[f"- {item}" for item in source_paths_for(module["key"])],
            ]
        )
    lines.extend(["", "## Shared hardening documents"])
    for title, path, purpose in HARDENING_DOCS:
        lines.append(f"- {title}: {path} - {purpose}")
    lines.extend(["", "## External references"])
    lines.extend(f"- {ref}" for ref in EXTERNAL_REFERENCES)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        rightMargin=0.58 * inch,
        leftMargin=0.58 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.65 * inch,
        title="Phase 7A Approved AI Source Reference",
        author="Codex Release Documentation",
    )
    story = []
    add_cover(story)
    add_intro(story)
    add_inventory(story)
    add_architecture(story)
    add_database_architecture(story)
    add_common_operation(story)
    for index, module in enumerate(MODULES):
        add_module(story, index, module)
    add_quality_and_ai_source_guidance(story, 8 + len(MODULES))
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


if __name__ == "__main__":
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    build_markdown()
    build_pdf()
    print(OUT_PDF)
    print(OUT_MD)
