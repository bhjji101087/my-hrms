# Phase 7A Approved AI Source Reference

This Markdown mirrors the generated PDF and is provided for reliable AI ingestion.

## Executive Conclusion
Phase 7A delivers the enterprise HRMS platform foundation plus branch/office hierarchy, shift foundation, and the first business operations: Core HR, Leave, Attendance, Payroll, and Standard Reports.

## Modules

### Tenant Catalog + Row-Level Security
Phase: S1 foundation
Schema: catalog plus security RLS

Conclusion: This module is the foundation of the SaaS platform. It defines every customer, their status, placement, feature entitlements, branding, provider choices, and the tenant context required before any business data can be accessed. The approved design makes tenant isolation a platform rule, not a developer preference.

Approved delivery:
- Tenant catalog with tenant, shard, branding, feature flag, provider, provider config, and provider health records.
- Server-side tenant resolution from host, token-safe hints, or platform-owner context.
- SQL Server Row-Level Security for every tenant-scoped table.
- Tenant lifecycle controls for provision, activate, suspend, offboard, and placement change.
- Tenant-safe namespaces for cache, search, storage, events, logs, telemetry, and providers.

Architecture:
- The request pipeline resolves tenant context before application services run.
- Application services receive an immutable tenant context; repositories cannot run without it.
- Entitlements are checked across API, UI, jobs, reports, integrations, events, and AI.
- Provider abstraction reads tenant provider configuration without exposing secrets to business code.

Database model:
- catalog.Tenant
- catalog.TenantShard
- catalog.TenantBranding
- catalog.TenantFeatureFlag
- catalog.TenantConfigVersion
- catalog.ProviderType
- catalog.Provider
- catalog.TenantProviderConfig
- catalog.ProviderHealth
- security.fn_tenant_predicate
- security.TenantIsolation policy

API examples:
- GET /api/v1/tenants/{id}
- POST /api/v1/tenants
- POST /api/v1/tenants/{id}/suspend
- GET /api/v1/tenants/{id}/features
- PUT /api/v1/tenants/{id}/providers/{providerType}

Event examples:
- TenantProvisioned
- TenantActivated
- TenantSuspended
- TenantOffboardingStarted
- TenantFeatureFlagsChanged
- TenantProviderConfigChanged

Example: Tenant A and Tenant B can both use the same People table. Every row has TenantId. When Tenant A's request reaches SQL Server, SESSION_CONTEXT contains Tenant A's id, so RLS hides Tenant B rows and blocks wrong-tenant writes even if a query is written incorrectly.

Test focus:
- Cross-tenant reads and writes are blocked at service, EF filter, and SQL RLS layers.
- Suspended tenants cannot use APIs, jobs, reports, events, or integrations.
- Provider config and tenant lifecycle changes are audited and invalidate caches.

Source documents:
- docs/02-product-requirements/FEAT-TENANT-001-business-requirements.md
- docs/09-development/TECH-TENANT-001-technical-design.md
- docs/06-database/DB-DESIGN-TENANT-001.md
- docs/07-ui-ux/UI-TENANT-001-screens.md
- docs/10-testing/TEST-TENANT-001-test-plan.md

### Branch / Office Hierarchy and Scoped Administration
Phase: S1-S4 foundation
Schema: org plus security

Conclusion: Branch and office hierarchy lets one tenant operate many offices, branches, sites, or regional units while preserving scoped administration. A complete tenant admin can see the whole tenant, while branch admins and branch-scoped users can only see or act inside their approved branch scope.

Approved delivery:
- Tenant branch and office tree with parent-child hierarchy, effective dates, status, timezone, country, state, and address metadata.
- Scoped administration model for tenant-wide admins, branch admins, HR operators, payroll operators, managers, and employees.
- Employee branch assignment with effective dating so historical reports and payroll remain correct.
- Branch-aware RBAC and ABAC enforcement across Core HR, Leave, Attendance, Payroll, Reports, exports, jobs, and events.
- Branch hierarchy events and audit evidence for branch changes, scope assignment, and employee branch movement.

Architecture:
- Branch hierarchy is modeled as tenant-owned organization data and exposed through shared scope resolvers.
- Authorization combines tenant context, RBAC permissions, ABAC attributes, and branch scope.
- Branch-scoped users cannot access sibling branch data unless a higher scope is explicitly granted.
- Downstream modules consume branch assignment through Core HR APIs/events and do not duplicate branch ownership logic.

Database model:
- org.BranchOffice
- org.BranchOfficeHierarchyClosure
- org.EmployeeBranchAssignment
- security.BranchScopeAssignment
- security.BranchScopeDecisionLog

API examples:
- GET /api/v1/branches
- POST /api/v1/branches
- GET /api/v1/branches/{id}/tree
- POST /api/v1/branches/{id}/scope-assignments
- GET /api/v1/security/branch-scopes

Event examples:
- BranchCreated
- BranchUpdated
- BranchHierarchyChanged
- BranchScopeAssigned
- BranchScopeRevoked
- EmployeeBranchAssignmentChanged

Example: Tenant A has a head office, Mumbai branch, Delhi branch, and Pune branch. A tenant admin can review all offices. The Mumbai branch admin can manage only Mumbai employees, approvals, attendance, reports, and exports. They cannot open Delhi employee details or payroll reports.

Test focus:
- Branch admin cannot read, export, approve, or update sibling branch data.
- Tenant admin can view all branches inside the same tenant but never another tenant.
- Historical employee branch assignment works for as-of reports, payroll evidence, and audit.

Source documents:
- docs/02-product-requirements/FEAT-BRANCH-001-business-requirements.md
- docs/09-development/TECH-BRANCH-001-technical-design.md
- docs/06-database/DB-DESIGN-BRANCH-001.md
- docs/07-ui-ux/UI-BRANCH-001-screens.md
- docs/10-testing/TEST-BRANCH-001-test-plan.md

### Identity, Authentication, RBAC, and ABAC
Phase: S1 foundation
Schema: security

Conclusion: Identity is the central security module. It handles authentication, sessions, roles, permissions, policies, delegation, impersonation, emergency access, and authorization decision traceability. The approved design combines RBAC for role permissions and ABAC for contextual rules.

Approved delivery:
- Local login, OIDC/SSO, MFA, adaptive risk checks, and refresh token rotation.
- RBAC permissions, ABAC policies, deny-by-default authorization, and policy decision tracing.
- SCIM user and group provisioning for enterprise identity integration.
- Device/session management, global logout, remote session termination, and distributed revocation.
- Break Glass emergency access with reason, expiry, approval option, revocation, and audit.

Architecture:
- Client requests pass through API Gateway, Authentication Service, Token Service, PEP, and PDP.
- The PEP enforces permissions at API, handler, job, report, and UI capability boundaries.
- The PDP evaluates role, resource, tenant, user, delegation, impersonation, and ABAC policy context.
- Distributed session and revocation state keep multiple app instances consistent.

Database model:
- security.UserAccount
- security.Role
- security.Permission
- security.RolePermission
- security.UserRole
- security.AbacPolicy
- security.Session
- security.RefreshToken
- security.Delegation
- security.PasswordPolicy
- security.PasswordHistory
- security.AuthSecurityEvent
- security.BreakGlassAccess
- security.BreakGlassSession

API examples:
- POST /api/v1/auth/login
- POST /api/v1/auth/sso/start
- POST /api/v1/auth/mfa/verify
- POST /api/v1/auth/refresh
- GET /api/v1/security/sessions
- POST /api/v1/security/break-glass
- GET /api/v1/security/authorization-trace/{correlationId}

Event examples:
- UserLoggedIn
- MfaChallengeCompleted
- SessionRevoked
- RoleAssignmentChanged
- TenantRoleMatrixChanged
- BreakGlassActivated
- AuthSecurityEventRecorded

Example: A manager can approve a leave request only when RBAC grants Leave.Approve and ABAC confirms the employee belongs to the manager's allowed team, legal entity, or delegated scope. The decision record stores tenant, user, permission, policy version, result, reason, and correlation id.

Test focus:
- Unauthorized users cannot access secured endpoints or emergency access.
- Refresh token reuse is detected and revokes the session family.
- Distributed logout and role change invalidation work across all app instances.
- Brute-force, credential stuffing, adaptive MFA, and lockout controls are verified.

Source documents:
- docs/02-product-requirements/FEAT-IDENTITY-001-business-requirements.md
- docs/09-development/TECH-IDENTITY-001-technical-design.md
- docs/06-database/DB-DESIGN-IDENTITY-001.md
- docs/07-ui-ux/UI-IDENTITY-001-screens.md
- docs/10-testing/TEST-IDENTITY-001-test-plan.md

### Effective Dating and Bitemporal Core
Phase: S2 foundation
Schema: core and temporal history

Conclusion: Effective dating is a platform pattern for any business fact that changes over time. It allows the system to answer what was true on a business date, what the system knew at a system time, and why a change happened. This is essential for payroll, assignments, policies, workflow versions, compliance, and reporting.

Approved delivery:
- Shared effective dating service, period validator, as-of query service, change request flow, and history explanation.
- Mandatory valid-time columns for time-changing facts.
- SQL Server temporal table support for high-value history plus approved fallback patterns.
- Backdated, current, future-dated, supersede, cancel, and bulk effective-dated operations.
- Event publication through the outbox for every approved effective-dated change.

Architecture:
- Business APIs call application services, which call the Effective Dating Service before repositories.
- The Period Validator prevents invalid periods, overlaps, duplicate open-ended rows, and unsafe backdating.
- As-of reads are consistent across API, reporting, rules, workflow, and payroll.
- Sensitive corrections can be routed through Workflow Studio before activation.

Database model:
- core.EffectiveDatedEntityRegistration
- core.EffectiveDatedChangeRequest
- core.EffectivePeriodConflict
- EffectiveFrom
- EffectiveTo
- EffectiveStatus
- ChangeReason
- ApprovalReferenceId
- SupersededById
- VersionNumber or rowversion

API examples:
- GET /api/v1/{module}/{resource}?asOfDate=YYYY-MM-DD
- POST /api/v1/{module}/{resource}/future-change
- POST /api/v1/{module}/{resource}/backdated-correction
- GET /api/v1/{module}/{resource}/{id}/history/explain

Event examples:
- EffectiveDatedRecordChanged
- EffectiveDatedChangeApproved
- EffectiveDatedChangeRejected
- EffectiveDatedConflictDetected

Example: If an employee's department changes from Sales to Finance effective 1 July, reports for 30 June still show Sales, payroll from July uses Finance, and the history screen explains who approved the change, when it was entered, and which old row was superseded.

Test focus:
- Overlap prevention works for employee assignment, salary assignment, policy version, and workflow/rule versions.
- As-of API, report, and payroll results agree for the same business date.
- Backdated changes produce audit entries, outbox events, and explain-history evidence.

Source documents:
- docs/02-product-requirements/FEAT-EFFECTIVE-DATING-001-business-requirements.md
- docs/09-development/TECH-EFFECTIVE-DATING-001-technical-design.md
- docs/06-database/DB-DESIGN-EFFECTIVE-DATING-001.md
- docs/07-ui-ux/UI-EFFECTIVE-DATING-001-screens.md
- docs/10-testing/TEST-EFFECTIVE-DATING-001-test-plan.md

### Audit and Time Machine
Phase: S2 foundation
Schema: audit

Conclusion: Audit and Time Machine provide evidence. Every important change, authorization decision, security event, workflow decision, export, and sensitive read is traceable. Time Machine reconstructs business state using effective dating, temporal history, audit records, workflow evidence, and events.

Approved delivery:
- Shared audit capture services consumed by all Phase 7A modules.
- Append-only audit records and field changes with masking, classification, retention, and legal hold.
- Security event collection for login, MFA, ABAC, emergency access, and suspicious activity.
- Time-machine snapshots and explain-history views.
- Controlled audit exports with purpose, approval, expiry, and access tracking.

Architecture:
- Modules write audit through shared middleware, domain-event handlers, and approved capture points.
- Modules do not create private audit tables.
- High-risk audit classes can use hash chaining or ledger-like tamper evidence.
- Audit reads are themselves audited.

Database model:
- audit.AuditRecord
- audit.AuditFieldChange
- audit.SecurityEvent
- audit.TimeMachineSnapshot
- audit.AuditExportRequest

API examples:
- GET /api/v1/audit/search
- GET /api/v1/audit/entities/{entityName}/{entityId}/history
- GET /api/v1/audit/security-events
- POST /api/v1/audit/exports
- POST /api/v1/audit/time-machine/reconstruct

Event examples:
- AuditRecordCreated
- SecurityEventRecorded
- TimeMachineSnapshotGenerated
- AuditExportRequested
- AuditExportDownloaded

Example: When payroll is published, the audit trail can show the run, source snapshot hash, rule versions, approver, exceptions, generated payslips, and every user who downloaded payroll evidence.

Test focus:
- Sensitive values are masked or encrypted and passwords/secrets are never stored.
- Entity history lookup is tenant-filtered and performant.
- Legal hold blocks purge and exports expire correctly.

Source documents:
- docs/02-product-requirements/FEAT-AUDIT-001-business-requirements.md
- docs/09-development/TECH-AUDIT-001-technical-design.md
- docs/06-database/DB-DESIGN-AUDIT-001.md
- docs/07-ui-ux/UI-AUDIT-001-screens.md
- docs/10-testing/TEST-AUDIT-001-test-plan.md

### Event Bus and Transactional Outbox
Phase: S2 foundation
Schema: integration

Conclusion: The event backbone allows modules to communicate without direct database coupling. Phase 7A uses RabbitMQ first behind an event bus abstraction, with Azure Service Bus available later through adapter replacement.

Approved delivery:
- Event contract registry with versioned schemas and compatibility status.
- Transactional outbox so business change and event creation are atomic.
- Outbox publisher worker with retry, backoff, dead-letter handling, and replay approval.
- Inbox store for idempotent consumers.
- Tenant-scoped event metadata, classification, correlation, and causation ids.

Architecture:
- A module command writes domain data and OutboxEvent in the same database transaction.
- The publisher worker sends events to RabbitMQ through IEventBus.
- Consumers record InboxMessage before side effects to prevent duplicate processing.
- Event contracts are versioned; renaming or removing events needs deprecation planning.

Database model:
- integration.EventContract
- integration.OutboxEvent
- integration.InboxMessage
- integration.DeadLetterEvent
- integration.EventReplayRequest

API examples:
- GET /api/v1/integration/events/contracts
- GET /api/v1/integration/outbox
- GET /api/v1/integration/dead-letter
- POST /api/v1/integration/events/replay

Event examples:
- EmployeeCreated
- EmployeeAssignmentChanged
- LeaveApproved
- AttendanceSummaryApproved
- PayrollRunPublished
- ReportExportCreated

Example: When LeaveApproved is committed, the outbox event is committed with it. Payroll can consume the event later to update loss-of-pay input. If RabbitMQ is temporarily down, the outbox keeps the event pending until the worker retries.

Test focus:
- Business data and outbox event are atomic.
- Duplicate events are rejected by EventId and duplicate consumer work is blocked by InboxMessage.
- Dead-letter replay requires approval and preserves reason and audit trail.

Source documents:
- docs/02-product-requirements/FEAT-EVENT-BUS-001-business-requirements.md
- docs/09-development/TECH-EVENT-BUS-001-technical-design.md
- docs/06-database/DB-DESIGN-EVENT-BUS-001.md
- docs/07-ui-ux/UI-EVENT-BUS-001-screens.md
- docs/10-testing/TEST-EVENT-BUS-001-test-plan.md

### Rule Engine
Phase: S3 foundation
Schema: rules

Conclusion: The Rule Engine prevents hardcoded business rules. Leave eligibility, attendance penalties, workflow routing, payroll formulas, statutory rules, feature flag evaluation, and compliance conditions are represented as versioned, effective-dated, testable configuration.

Approved delivery:
- Rule set and rule version lifecycle: draft, validate, simulate, approve, publish, rollback, deprecate.
- Decision tables, expression rules, JSON schema validation, and safe deterministic evaluation.
- Simulation workspace with explanations before publish.
- Runtime evaluation service for modules with tenant, version, correlation, and trace metadata.
- Evaluation logs with hashes and summaries for audit and troubleshooting.

Architecture:
- Modules call the shared Rule Evaluation API; they do not embed business thresholds in code.
- Rule Resolver selects the effective published version for tenant, module, date, and context.
- Evaluator returns outputs plus explanation metadata.
- Payroll and compliance rule versions are retained while referenced by payroll runs.

Database model:
- rules.RuleSet
- rules.RuleSetVersion
- rules.DecisionTable
- rules.RuleSimulation
- rules.RuleEvaluationLog

API examples:
- POST /api/v1/rules/rule-sets
- POST /api/v1/rules/{ruleSetId}/versions/{versionId}/simulate
- POST /api/v1/rules/{ruleSetId}/versions/{versionId}/submit
- POST /api/v1/rules/{ruleSetId}/versions/{versionId}/publish
- GET /api/v1/rules/evaluations/{correlationId}

Event examples:
- RuleSetVersionPublished
- RuleSetVersionDeprecated
- RuleSimulationCompleted
- RuleEvaluationFailed

Example: Instead of coding 'leave days greater than 5 needs HR approval', the tenant config can define a rule: if leave type is annual and duration exceeds the configured threshold, route to HR after manager approval. Changing the threshold is a rule version change, not a code change.

Test focus:
- Rule simulation produces deterministic outputs and explanations.
- Invalid JSON/schema payloads cannot be published.
- Runtime modules evaluate the intended effective version for date and tenant.

Source documents:
- docs/02-product-requirements/FEAT-RULE-ENGINE-001-business-requirements.md
- docs/09-development/TECH-RULE-ENGINE-001-technical-design.md
- docs/06-database/DB-DESIGN-RULE-ENGINE-001.md
- docs/07-ui-ux/UI-RULE-ENGINE-001-screens.md
- docs/10-testing/TEST-RULE-ENGINE-001-test-plan.md

### Workflow Studio
Phase: S3 foundation and S9 hardening
Schema: workflow

Conclusion: Workflow Studio is the approval and process engine for Phase 7A and future modules. It handles routed approvals, tasks, delegation, escalation, SLA timers, comments, decisions, versioned definitions, and outcome events.

Approved delivery:
- Workflow definition and published version lifecycle.
- Runtime workflow instances pinned to exact published version.
- Task inbox, decisions, delegation, reassignment, escalation, and SLA events.
- Workflow UI for designers, reviewers, task owners, and auditors.
- Outcome events that business modules can consume without direct coupling.

Architecture:
- Modules request workflow start and receive task/outcome callbacks or events.
- Workflow uses Rule Engine for routing, eligibility, and dynamic approver decisions.
- Workflow history links back to the source business entity.
- Published definitions are immutable; running instances do not change silently when a new version is published.

Database model:
- workflow.WorkflowDefinition
- workflow.WorkflowDefinitionVersion
- workflow.WorkflowInstance
- workflow.WorkflowTask
- workflow.WorkflowDecision
- workflow.WorkflowSlaEvent

API examples:
- POST /api/v1/workflows/definitions
- POST /api/v1/workflows/definitions/{id}/publish
- POST /api/v1/workflows/instances
- GET /api/v1/workflows/tasks
- POST /api/v1/workflows/tasks/{taskId}/decision

Event examples:
- WorkflowInstanceStarted
- WorkflowTaskAssigned
- WorkflowTaskDecided
- WorkflowSlaBreached
- WorkflowInstanceCompleted

Example: A payroll structure change can require maker-checker approval. Workflow creates a task for Payroll Reviewer, uses SLA rules for reminders, records the decision, and only then allows the salary structure version to be published.

Test focus:
- Running instance remains pinned to original workflow version.
- Delegation and escalation create correct task ownership and audit evidence.
- Task inbox respects assignee, role, delegate, tenant, and ABAC filters.

Source documents:
- docs/02-product-requirements/FEAT-WORKFLOW-001-business-requirements.md
- docs/09-development/TECH-WORKFLOW-001-technical-design.md
- docs/06-database/DB-DESIGN-WORKFLOW-001.md
- docs/07-ui-ux/UI-WORKFLOW-001-screens.md
- docs/10-testing/TEST-WORKFLOW-001-test-plan.md

### Configuration-as-Data
Phase: S3 foundation
Schema: config

Conclusion: Configuration-as-Data makes tenant behavior changeable without core code edits. Forms, feature flags, module manifests, policy payloads, provider settings, UI slots, navigation, rules, and workflow references become governed data with schema validation and published versions.

Approved delivery:
- Module manifest registry for dependencies, features, APIs, events, and UI extension slots.
- Configuration schema registry using JSON Schema.
- Versioned configuration items with effective dates, approval, publish, rollback, export, and import.
- Tenant-aware feature flags aligned to OpenFeature concepts.
- Promotion path between sandbox and production with traceability.

Architecture:
- Runtime services resolve the effective published configuration through shared providers.
- Secrets are references to approved secret storage, never payload values.
- Configuration publish invalidates cache and emits events.
- Customer customization happens through configuration, feature flags, extensions, and plugins.

Database model:
- config.ModuleManifest
- config.ConfigurationSchema
- config.ConfigurationItem
- config.ConfigurationVersion
- config.FeatureFlag
- config.ConfigurationImportExport

API examples:
- GET /api/v1/configuration/schemas
- POST /api/v1/configuration/items
- POST /api/v1/configuration/versions/{id}/validate
- POST /api/v1/configuration/versions/{id}/publish
- POST /api/v1/configuration/import-export

Event examples:
- ConfigurationVersionPublished
- ConfigurationRollbackCompleted
- FeatureFlagChanged
- ModuleManifestRegistered
- ConfigurationImportCompleted

Example: A tenant can add a new onboarding form field or change leave policy display text by publishing a validated configuration version. Core HRMS code does not change.

Test focus:
- Published versions are immutable and schema-validated.
- Feature flags are tenant-scoped and audited.
- Import/export has approval, rollback, and no secret leakage.

Source documents:
- docs/02-product-requirements/FEAT-CONFIGURATION-001-business-requirements.md
- docs/09-development/TECH-CONFIGURATION-001-technical-design.md
- docs/06-database/DB-DESIGN-CONFIGURATION-001.md
- docs/07-ui-ux/UI-CONFIGURATION-001-screens.md
- docs/10-testing/TEST-CONFIGURATION-001-test-plan.md

### Core HR and Employee Self-Service
Phase: S4 business module
Schema: hr

Conclusion: Core HR is the employee master data module. It owns person, employee, assignment, organization, location, document metadata, and self-service change requests. Leave, attendance, payroll, workflow, rules, reports, and integrations consume Core HR through APIs/events, not direct ownership.

Approved delivery:
- Employee and person records with protected personal information.
- Effective-dated assignments, manager hierarchy, departments, designations, grades, locations, and legal entities.
- Employee self-service change requests routed through Workflow Studio.
- Employee document metadata with secure file references.
- Events for employee creation, update, assignment change, and lifecycle status.

Architecture:
- Core HR APIs call the Effective Dating Service for assignment and org history.
- Manager hierarchy queries use ABAC and hierarchy service, not unrestricted employee reads.
- Other modules consume Core HR APIs/events and do not duplicate master data.
- Search/report projections can be rebuilt from Core HR source plus events.

Database model:
- hr.Person
- hr.Employee
- hr.EmployeeAssignment
- hr.OrganizationUnit
- hr.Location
- hr.EssChangeRequest
- hr.EmployeeDocumentMetadata

API examples:
- GET /api/v1/hr/employees
- GET /api/v1/hr/employees/{id}?asOfDate=YYYY-MM-DD
- POST /api/v1/hr/ess/change-requests
- GET /api/v1/hr/organization-units
- GET /api/v1/hr/locations

Event examples:
- EmployeeCreated
- EmployeeUpdated
- EmployeeAssignmentChanged
- EmployeeStatusChanged
- EssChangeRequestApproved

Example: When an employee transfers to a new manager from next month, Core HR creates an effective-dated assignment change. Leave approvals before that date still route to the old manager; approvals after that date route to the new manager.

Test focus:
- Employee number is unique per tenant.
- Manager hierarchy and as-of assignment queries return correct historical state.
- Sensitive personal fields are encrypted, masked, and access controlled.

Source documents:
- docs/02-product-requirements/FEAT-CORE-HR-001-business-requirements.md
- docs/09-development/TECH-CORE-HR-001-technical-design.md
- docs/06-database/DB-DESIGN-CORE-HR-001.md
- docs/07-ui-ux/UI-CORE-HR-001-screens.md
- docs/10-testing/TEST-CORE-HR-001-test-plan.md

### Leave Management
Phase: S5 business module
Schema: leave

Conclusion: Leave Management delivers the first end-to-end HR business workflow: policies, balances, applications, approvals, cancellation, adjustment, holiday calendars, payroll impact, and audit. It proves the platform foundations work together.

Approved delivery:
- Tenant-specific leave types, policy versions, eligibility, accrual, day-count, carry-forward, and approval workflow references.
- Leave request lifecycle: apply, validate, reserve, approve, reject, withdraw, cancel, and correct.
- Ledger-based leave transactions with rebuildable balance projections.
- Holiday calendars scoped by tenant and location.
- Payroll-impact events for unpaid leave, corrections, and balance-affecting decisions.

Architecture:
- Leave consumes Tenant, Identity, Effective Dating, Audit, Event Bus, Rule Engine, Workflow, Configuration, and Core HR.
- Balances are derived from immutable transactions, not manually overwritten totals.
- Rule Engine handles eligibility, accrual, day count, and carry-forward logic.
- Workflow handles approval routing; Event Bus publishes payroll and reporting impacts.

Database model:
- leave.LeaveType
- leave.LeavePolicyVersion
- leave.HolidayCalendar
- leave.Holiday
- leave.LeaveRequest
- leave.LeaveTransaction
- leave.LeaveBalanceProjection

API examples:
- GET /api/v1/leave/types
- GET /api/v1/leave/balances
- POST /api/v1/leave/requests
- POST /api/v1/leave/requests/{id}/withdraw
- GET /api/v1/leave/requests/{id}/history
- POST /api/v1/leave/policies/{id}/preview

Event examples:
- LeaveRequested
- LeaveApproved
- LeaveRejected
- LeaveCancelled
- LeaveBalanceChanged
- LeavePayrollImpactReady

Example: An employee applies for 3 days annual leave. The system checks eligibility and calendar, reserves 3 days in the ledger, starts workflow, and after approval debits the ledger. If the request is cancelled before payroll cutoff, a reversing ledger transaction and payroll-impact event are created.

Test focus:
- Duplicate requests cannot double-reserve or double-debit balance.
- Ledger can rebuild projections exactly.
- Policy versions support historical and future-dated rules.

Source documents:
- docs/02-product-requirements/FEAT-LEAVE-001-business-requirements.md
- docs/09-development/TECH-LEAVE-001-technical-design.md
- docs/06-database/DB-DESIGN-LEAVE-001.md
- docs/07-ui-ux/UI-LEAVE-001-screens.md
- docs/10-testing/TEST-LEAVE-001-test-plan.md

### Attendance and First Connector
Phase: S6 business module
Schema: attendance

Conclusion: Attendance captures raw punches, reconciles daily attendance summaries, supports regularization requests, and feeds payroll. The first connector framework proves how future devices or providers can be added through adapters and configuration.

Approved delivery:
- Attendance policy versions linked to rules and calendars.
- Device and connector configuration with secret references.
- Raw punch ingestion with deduplication and immutability.
- Daily summary calculation for present, absent, late, early leave, work minutes, and payroll impact.
- Regularization workflow for employee corrections and manager/HR approval.

Architecture:
- Connector/Web/API input flows into Punch Ingestion, Raw Punch Store, Attendance Engine, Rules, and Payroll Events.
- Raw punches are immutable; corrections are approved regularization records.
- Daily summaries are rebuildable from raw punches plus approved adjustments.
- Connector adapters are provider-specific; business logic stays provider-neutral.

Database model:
- attendance.AttendancePolicyVersion
- attendance.AttendanceDevice
- attendance.RawPunch
- attendance.AttendanceDaySummary
- attendance.RegularizationRequest
- attendance.ConnectorSyncRun

API examples:
- POST /api/v1/attendance/punches
- GET /api/v1/attendance/summaries
- POST /api/v1/attendance/regularization-requests
- GET /api/v1/attendance/connectors/sync-runs
- POST /api/v1/attendance/reconciliation/run

Event examples:
- RawPunchReceived
- AttendanceSummaryCalculated
- RegularizationRequested
- RegularizationApproved
- AttendancePayrollImpactReady
- ConnectorSyncCompleted

Example: A biometric device sends the same punch twice. The unique external punch key marks the duplicate without double-counting work time. If the employee forgot checkout, they submit regularization, workflow approves it, and the daily summary is recalculated for payroll.

Test focus:
- Duplicate external punches are detected and do not double count.
- Summary rebuild produces consistent payroll-impact results.
- Connector failures and sync gaps are auditable and recoverable.

Source documents:
- docs/02-product-requirements/FEAT-ATTENDANCE-001-business-requirements.md
- docs/09-development/TECH-ATTENDANCE-001-technical-design.md
- docs/06-database/DB-DESIGN-ATTENDANCE-001.md
- docs/07-ui-ux/UI-ATTENDANCE-001-screens.md
- docs/10-testing/TEST-ATTENDANCE-001-test-plan.md

### Shift Foundation
Phase: S6-S8 foundation
Schema: attendance

Conclusion: Shift Foundation defines basic shift templates, employee shift assignments, exceptions, and shift resolution. It is intentionally included in Phase 7A because attendance and payroll cannot be reliable without knowing which shift applied to an employee on a date. Advanced roster planning, workforce demand planning, and shift swaps remain later-phase work.

Approved delivery:
- Configurable shift definitions with start/end time, grace rules, break handling, night shift flag, timezone, and effective versions.
- Effective-dated employee shift assignments linked to branch, department, role, or employee where permitted.
- Controlled one-day or temporary shift overrides routed through workflow when tenant policy requires approval.
- Shift resolver service used by attendance summary calculation, regularization, reports, and payroll source snapshots.
- Audit, events, and explainability for which shift was used in a daily attendance or payroll result.

Architecture:
- Attendance asks the Shift Resolver for the effective shift before calculating late, early, absent, night, overtime, or payroll-impact values.
- Shift definitions are versioned and effective-dated so past attendance and payroll results remain reproducible.
- Branch and role defaults can be overridden by employee-specific assignments when allowed by tenant policy.
- Payroll consumes shift-aware attendance summaries, not raw shift rules, so published payroll stays explainable.

Database model:
- attendance.ShiftDefinition
- attendance.ShiftDefinitionVersion
- attendance.EmployeeShiftAssignment
- attendance.EmployeeShiftOverride
- attendance.ShiftResolutionLog

API examples:
- GET /api/v1/attendance/shifts
- POST /api/v1/attendance/shifts
- POST /api/v1/attendance/shifts/{id}/publish
- POST /api/v1/attendance/shift-assignments
- POST /api/v1/attendance/shift-overrides
- GET /api/v1/attendance/employees/{employeeId}/shift?date=YYYY-MM-DD

Event examples:
- ShiftDefinitionPublished
- ShiftDefinitionRetired
- EmployeeShiftAssigned
- EmployeeShiftAssignmentChanged
- ShiftOverrideApproved
- ShiftPayrollImpactChanged

Example: An employee is assigned to a 10:00 to 19:00 shift for July. If they punch in at 10:20, attendance applies that shift's grace rule. If the employee is temporarily assigned to a night shift for one day, the approved override is used only for that date and payroll can explain the result.

Test focus:
- Effective shift resolution chooses employee override, employee assignment, branch default, and tenant default in the approved priority order.
- Overnight shifts calculate work date, late arrival, early exit, and payable minutes correctly.
- Payroll snapshots reference the shift-aware attendance summary and remain reproducible after shift rules change.

Source documents:
- docs/02-product-requirements/FEAT-SHIFT-FOUNDATION-001-business-requirements.md
- docs/09-development/TECH-SHIFT-FOUNDATION-001-technical-design.md
- docs/06-database/DB-DESIGN-SHIFT-FOUNDATION-001.md
- docs/07-ui-ux/UI-SHIFT-FOUNDATION-001-screens.md
- docs/10-testing/TEST-SHIFT-FOUNDATION-001-test-plan.md

### Payroll and India Compliance
Phase: S7-S8 business module
Schema: payroll

Conclusion: Payroll is the highest-risk Phase 7A business module. It calculates employee payroll from Core HR, Leave, Attendance, salary structures, declarations, and effective-dated statutory rules. Published payroll must be reproducible, explainable, immutable, and compliant with the India-first foundation.

Approved delivery:
- Payroll calendars, periods, cutoff, dry run, approval, lock, publish, and correction flow.
- Salary components, salary structure versions, and effective-dated employee salary assignments.
- Source snapshot for Core HR, Leave, Attendance, and component inputs.
- Calculation engine for earnings, deductions, arrears, LOP, statutory components, and exceptions.
- India compliance foundation: PF, ESI, PT, LWF, TDS, Form 16, FBP, and revisions where applicable.
- Payslip generation and employee access controls.

Architecture:
- Payroll consumes Core HR, Leave, Attendance, Rule Engine, Workflow, Audit, and Event Bus.
- The run captures source snapshot hash and rule-version snapshot before calculation.
- Rule Engine evaluates salary, eligibility, statutory, and tax logic.
- Workflow approves sensitive configuration and payroll run publish.
- Published runs are immutable; corrections create adjustment runs or controlled correction records.

Database model:
- payroll.PayrollCalendar
- payroll.PayPeriod
- payroll.SalaryComponent
- payroll.SalaryStructureVersion
- payroll.EmployeeSalaryAssignment
- payroll.PayrollRun
- payroll.PayrollRunEmployee
- payroll.PayrollRunComponent
- payroll.StatutoryRuleVersion
- payroll.Payslip

API examples:
- POST /api/v1/payroll/runs/dry-run
- POST /api/v1/payroll/runs/{id}/approve
- POST /api/v1/payroll/runs/{id}/publish
- GET /api/v1/payroll/runs/{id}/employees/{employeeId}/explain
- GET /api/v1/payroll/payslips
- POST /api/v1/payroll/statutory-rule-versions

Event examples:
- PayrollRunStarted
- PayrollRunCalculated
- PayrollRunExceptionRaised
- PayrollRunApproved
- PayrollRunPublished
- PayslipPublished

Example: For June payroll, the run snapshots employee assignments, approved leave loss-of-pay, attendance summaries, salary assignments, declarations, and statutory rule versions. A future salary change effective July does not change June results. After publish, June payroll is locked; corrections go through a revision or adjustment process.

Test focus:
- Published payroll can be reproduced from source and rule snapshots.
- Unauthorized users cannot see payroll data outside legal entity, payroll group, or employee-self scope.
- Statutory rule versions are effective-dated and cannot be purged while referenced.
- Explain-calculation returns lineage for each component.

Source documents:
- docs/02-product-requirements/FEAT-PAYROLL-001-business-requirements.md
- docs/09-development/TECH-PAYROLL-001-technical-design.md
- docs/06-database/DB-DESIGN-PAYROLL-001.md
- docs/07-ui-ux/UI-PAYROLL-001-screens.md
- docs/10-testing/TEST-PAYROLL-001-test-plan.md

### Standard Reports
Phase: S10 business module
Schema: reporting

Conclusion: Standard Reports provide the first governed reporting layer. Reports are versioned, permissioned, tenant-scoped, export-controlled, and supported by rebuildable projections. Reporting uses approved APIs, events, and read models rather than unsafe direct cross-module coupling.

Approved delivery:
- Report catalog with definitions, parameters, classifications, permissions, and versions.
- Report run and export flow with status, purpose, expiry, and audit.
- Employee and payroll projections for common operational/statutory reports.
- As-of reporting using Effective Dating.
- Export controls for sensitive data, approvals where required, download limits, and expiration.

Architecture:
- Module events and approved APIs feed reporting projections.
- Report Query Service applies tenant, RBAC, ABAC, filters, pagination, and masking.
- Export Service is asynchronous and audited.
- Projection Builder can rebuild read models from source modules/events.

Database model:
- reporting.ReportDefinition
- reporting.ReportDefinitionVersion
- reporting.ReportRun
- reporting.ReportExport
- reporting.EmployeeReportProjection
- reporting.PayrollReportProjection

API examples:
- GET /api/v1/reports/catalog
- POST /api/v1/reports/{reportCode}/run
- GET /api/v1/reports/runs/{runId}
- POST /api/v1/reports/runs/{runId}/export
- GET /api/v1/reports/exports/{exportId}/download

Event examples:
- ReportRunRequested
- ReportRunCompleted
- ReportExportCreated
- ReportExportDownloaded
- ReportProjectionRebuilt

Example: A payroll summary report uses the payroll projection linked to the exact payroll run and rule snapshot. An HR admin with the correct legal-entity scope can export it with a purpose and expiry; the export download is audited.

Test focus:
- Report results are tenant-scoped, paginated, masked, and permission-filtered.
- As-of report dates match Effective Dating service results.
- Exports expire and access logs are complete.

Source documents:
- docs/02-product-requirements/FEAT-REPORTING-001-business-requirements.md
- docs/09-development/TECH-REPORTING-001-technical-design.md
- docs/06-database/DB-DESIGN-REPORTING-001.md
- docs/07-ui-ux/UI-REPORTING-001-screens.md
- docs/10-testing/TEST-REPORTING-001-test-plan.md

## Shared hardening documents
- API, Event, NFR, and Runbook Standard: docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md - Every module must define versioned APIs, event contracts, error responses, non-functional targets, observability, and runbook expectations.
- Database Classification, Migration, and Rollback Standard: docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md - Every database design must classify data, protect PII/payroll data, define migrations, rollback, verification, retention, and legal-hold behavior.
- UI Accessibility and States Standard: docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md - Every UI must handle loading, empty, error, permission-denied, approval, audit, responsive, and accessibility states.
- Testing Traceability and Abuse Standard: docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md - Tests must trace requirements to scenarios and include tenant isolation, abuse, negative, security, performance, and recovery cases.
- Phase 7A Hardening Backlog: docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md - Module-specific hardening items are tracked without blocking the approval gate, but they must be considered during implementation planning.

## External references
- Microsoft SQL Server Row-Level Security - https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
- Microsoft SQL Server Temporal Tables - https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
- Microsoft SQL Server Ledger - https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview
- OpenAPI Specification - https://spec.openapis.org/oas/latest.html
- CloudEvents - https://cloudevents.io/
- RabbitMQ Reliability Guide - https://www.rabbitmq.com/docs/reliability
- JSON Schema - https://json-schema.org/
- OpenFeature Specification - https://openfeature.dev/specification/
- OWASP API Security Top 10 - https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- WCAG 2.2 - https://www.w3.org/TR/WCAG22/
- EPFO India - https://www.epfindia.gov.in/site_en/index.php
- Income Tax Department India - https://www.incometax.gov.in/iec/foportal/
- Web visual: Wikimedia Commons team meeting photo - WLM international team meeting Vienna 2023-05-27
- Web visual: Wikimedia Commons server infrastructure photo - Wikimedia Servers-0051 19
