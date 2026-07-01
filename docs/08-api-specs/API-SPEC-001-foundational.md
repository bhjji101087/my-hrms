# API Specification — Foundational Endpoints (Phase 7A)

Document Owner: .NET Architect (Agent 13) + API Governance (Agent 15)
Created Date: 2026-06-14
Version: 1.2
Status: Approved
Approved By: Bhajan Lal (Product Owner)
Approved Date: 2026-06-22
Owner Amendment: Provider categories are registry-driven; VectorStore added for Qdrant-first architecture

> Foundational REST APIs powering the approved screens (SCREENS-001 / DESIGN-SPEC-002):
> auth, tenant context, identity, employees, leave, workflow/approvals, rules, provider
> management, search, notifications, and audit. Follows `API_STANDARDS.md` and the
> approved ADRs (005 tenancy, 006 data-access, 008 identity, 009 events, 010 workflow,
> 011 rules, 027 provider abstraction). Module-specific specs (payroll, attendance,
> compliance) follow separately. Every endpoint ships with **OpenAPI** (Swagger mandatory).

Machine-readable OpenAPI artifact:

- `docs/08-api-specs/OPENAPI-001-foundational-v1.yaml`

Phase 5 refresh inputs:

- Approved Phase 2 PRD and roadmap.
- Approved Phase 3 architecture, DB, provider, ADR, and security package.
- Approved Phase 4 UI/UX alignment checkpoint.

---

# Conventions (from API_STANDARDS)

- **Base:** `/api/v1` · REST · JSON · OpenAPI documented.
- **Success envelope:** `{ "success": true, "message": "", "data": {…} }`
- **Error envelope:** `{ "success": false, "message": "…", "errors": [ {field,code,msg} ] }`
- **Lists:** `page`, `pageSize`, `sort`, `filter`, `search`; return `data.items` + `data.page`.
- **Security (every request):** `Authorization: Bearer <JWT>`; tenant resolved from token
  (ADR-006) — never from body; **RBAC + ABAC** checked (ADR-008); deny-by-default.
- **Headers:** `X-Correlation-Id` (echoed), `Idempotency-Key` (required on critical POSTs).
- **Errors:** 400 validation · 401 unauthenticated · 403 forbidden · 404 not found ·
  409 conflict/idempotency · 422 business-rule · 429 rate-limited · 500 server.
- **Audit/events:** mutating endpoints write audit (FR-008) and may publish domain events
  via the outbox (ADR-009).

---

# 1. Auth & Identity  `/api/v1/auth`, `/api/v1/me`, `/api/v1/roles`

### POST /auth/login
- **Desc:** local login; returns JWT + refresh. (SSO via `/auth/sso/{tenant}` → OIDC.)
- **Body:** `{ "email", "password", "tenantHint?" }`
- **200:** `{ success, data:{ accessToken, refreshToken, expiresIn, mfaRequired } }`
- **Errors:** 400 invalid, 401 bad creds (generic), 403 tenant suspended, 423 locked.
- **Audit:** `AccessLog: Login` (success/fail). **Rate-limited.**

### POST /auth/refresh · POST /auth/logout
- Rotate refresh token (revoke old) / forced logout. **Audit:** `Login`/`Logout`.

### GET /auth/sso/{tenant}
- Redirects to tenant IdP (Entra/Google/Okta). SCIM provisioning handled out-of-band (ADR-008).

### GET /me
- **200:** `{ data:{ userId, tenantId, roles[], permissions[], locale, attributes } }`
  (drives PermissionGate/ABAC in the UI).

### Role and permission management (`Roles.Manage`)
- `GET /roles`, `POST /roles`, `PUT /roles/{id}`
- `PUT /roles/{id}/permissions`
- Permission catalog remains global reference data; role assignments are tenant-scoped.
- Every change is audited; ABAC policies reference Rule Engine rulesets.

---

# 2. Tenant, Feature Flags & Branding `/api/v1/tenant`

### GET /tenant/current
- Returns tenant profile, status, region, branding, enabled features, locale defaults,
  and provider summary. Drives tenant-aware shell and white-label rendering.

### Tenant administration (`Tenant.Manage`)
- `GET /tenants/{id}` · `PUT /tenants/{id}`.
- `GET /tenants/{id}/feature-flags` · `PUT /tenants/{id}/feature-flags/{featureKey}`.
- `GET /tenants/{id}/branding` · `PUT /tenants/{id}/branding`.
- `GET /tenants/{id}/config-versions` · `POST /tenants/{id}/config-promotions`.
- All endpoints are platform/tenant-admin permission gated, audited, and tenant-isolated.

---

# 3. Employees  `/api/v1/employees`  (effective-dated, ADR-007)

### GET /employees
- **Perm:** `People.View` (ABAC: managers scoped to own org).
- **Query:** `search, department, location, status, page, pageSize, sort, asOf?`
- **200:** `{ data:{ items:[ {employeeId, employeeNumber, name, designation, department, managerName, status} ], page:{number,size,total} } }`

### GET /employees/{id}?asOf=YYYY-MM-DD
- Returns the values valid as-of date (default today). **Perm:** `People.View` + ABAC.

### POST /employees   *(Idempotency-Key required)*
- **Perm:** `People.Create`. **Body:** core HR + initial assignment (effective-dated).
- **201:** created employee. **Event:** `EmployeeCreated`. **Audit:** Create.

### PUT /employees/{id}   *(effective-dated change)*
- **Body:** `{ effectiveFrom, changes:{…}, reason }` → creates a new version, preserves
  history (ADR-007). **403** if ABAC scope fails. **Event:** `EmployeeUpdated`. **Audit:** field-level old→new + reason (feeds Time Machine).

### GET /employees/{id}/history
- **Perm:** `People.View`. Returns audit/effective-dated timeline (powers Audit Center).

### GET /org-chart?rootId=&depth=
- Reporting hierarchy tree + counts (powers Org screen).

---

# 4. Leave  `/api/v1/leave`

### GET /leave/balances?employeeId=
- **200:** `{ data:{ balances:[ {type, available, accrued, used} ] } }` (rules via FR-013).

### GET /leave/types
- Tenant-configured leave types (no hardcoding) + rule metadata for client-side hints.

### POST /leave/requests   *(Idempotency-Key required)*
- **Perm:** `Leave.Apply`. **Body:** `{ employeeId, typeId, from, to, halfDay?, reason }`
- **Flow:** validates against **Rule Engine** (balance, overlap, min-notice, eligibility);
  starts a **Workflow** instance (approval chain) per ADR-010.
- **201:** `{ data:{ requestId, status:"Submitted", workflowInstanceId, approvalChain[] } }`
- **422:** rule failure (e.g. insufficient balance) with `errors[]`.
- **Event:** `LeaveRequested`. **Audit:** Create.

### GET /leave/requests?status=&employeeId=&page=
- List with filters; self-service shows own; managers see team (ABAC).

### POST /leave/requests/{id}/withdraw
- Withdraws if not finalized; emits event; audited.

---

# 5. Workflow & Approvals  `/api/v1/workflow` (ADR-010)

### GET /workflow/tasks?assignee=me&status=pending
- **Perm:** authenticated. Returns the **Approvals Inbox** (cross-module): `{ items:[ {taskId, module, subject, requester, step, slaDueAt, slaState, onBehalfOf?} ] }`.
- Honors **delegation** (acting-as): includes tasks delegated to the caller.

### POST /workflow/tasks/{id}/decision   *(Idempotency-Key required)*
- **Body:** `{ decision:"Approve"|"Reject", comment?, onBehalfOf? }`
- Advances the state machine; emits the next event; on SLA breach escalation already
  handled by the timer service.
- **200:** `{ data:{ taskId, newState, instanceStatus } }`
- **403** if not the assignee/delegate. **Event:** `LeaveApproved` / module event.
  **Audit:** decision + `OnBehalfOf` (delegation) → Time Machine.

### Workflow authoring (Tenant Admin · `Workflows.Manage`)
- `GET /workflow/definitions?key=` · `GET /workflow/definitions/{key}/versions`
- `POST /workflow/definitions` (save draft) · `POST /workflow/definitions/{id}/validate`
  (publish-time graph + rule validation) · `POST /workflow/definitions/{id}/publish`
  (creates immutable v+1; **running instances stay pinned** — ADR-010).
- `GET /workflow/instances/{id}` → state + append-only event log (audit).

---

# 6. Rule Engine `/api/v1/rules` (ADR-011)

### Rule authoring (`Rules.Manage`)
- `GET /rules/rulesets?key=&status=` · `POST /rules/rulesets` (save draft).
- `POST /rules/rulesets/{id}/validate` validates JSON-AST, references, and effective dates.
- `POST /rules/rulesets/{id}/test` runs sample facts through the ruleset.
- `POST /rules/rulesets/{id}/publish` creates immutable published version.
- **Audit:** rule diff + actor + reason. **Events:** `RuleSetPublished`.

---

# 7. Provider Management `/api/v1/providers` (ADR-027)

### Provider registry and tenant config
- `GET /providers/types` returns provider categories (storage, cache, messaging, email,
  SMS, push, identity, search, reporting, LLM, vector store). Category keys come from the
  provider registry and are not a closed API enum, so future provider categories can be
  added without changing feature code or the `/api/v1` contract.
- `GET /providers?type=` returns available adapters and capability flags.
- `GET /providers/config?type=` returns current tenant provider config.
- `POST /providers/config` creates/updates tenant provider config.
- `POST /providers/config/{id}/test` validates config before activation.
- `POST /providers/config/{id}/activate` activates config; idempotency required.
- `GET /providers/health` returns per-tenant/provider health for Integration Hub.

Provider config is admin-only, audited, effective-dated where needed, and stores only
secret references. Raw secrets are never returned by the API.

---

# 8. Cross-cutting endpoints

- **Search** `GET /search?q=` → grouped results (employee/leave/workflow/report) for the ⌘K + results screen.
- **Notifications** `GET /notifications` · `POST /notifications/{id}/read|snooze|pin` (event-driven, ADR-009).
- **Audit** `GET /audit/changes?entityType=&entityId=` → field-level history for Time Machine.
- **Config (no-code, `*.Manage` perms):** `/forms`, `/navigation`, `/branding`,
  `/feature-flags`, `/tenants/{id}` — all versioned, audited, sandbox→prod
  (ARCH-REVIEW §1B). Detailed in their own specs.
- **AI** APIs are intentionally excluded from `OPENAPI-001-foundational-v1.yaml` until
  Phase 6 AI Strategy and ADR-019 are approved. The expected future endpoint is
  `POST /ai/ask` with tenant-scoped RAG, RBAC/ABAC, citations, and audited actions.

---

# Non-functional (API)

- P95 < 2s; pagination mandatory on lists; rate limiting + quotas per tenant (ADR-023).
- Idempotency on all critical POSTs; correlation IDs on every request/log.
- Versioning + deprecation policy; OpenAPI published per endpoint (Swagger mandatory).
- All access tenant- + permission-validated; no dynamic SQL; parameterized only.

---

## Approval

.NET Architect: ____ · API Governance: ____ · Solution Architect: ____ · Security Architect: ____
Product Owner: Bhajan Lal · Approved 2026-06-22
