# HRMS Platform — Project Constitution

This is the root operating contract for every AI agent and every session in this
repository. It is loaded automatically. You never need to be told to read it.

All AI agents must follow these instructions.

---

## Mission

Build a configurable, multi-tenant, enterprise HRMS platform.

The platform must support:

* Multi-Tenant
* Multi-Country
* Multi-Language
* White Labeling
* Dynamic Workflows
* Dynamic Forms
* Dynamic Rules
* Dynamic Reports
* Extension-Based Customization
* AI Features

---

## Golden Rules

### Rule 1 — No code before approved documentation

Never start coding before approved documentation exists. A feature requires all five:

* Business Requirements
* Technical Design
* Database Design
* UI Design
* Test Cases

"Approved" means the document's `Status:` field reads `Approved`. Only the human
owner flips `Draft` / `Review` → `Approved`.

### Rule 2 — No hardcoded business rules

Bad:

```csharp
if (leaveDays > 5)
```

Good: rules stored in the database / rules engine. Everything configurable.

### Rule 3 — Customer customization never touches core

All customer-specific functionality must be implemented using:

* Configuration
* Feature Flags
* Extensions
* Plugins

Never modify core logic.

### Rule 4 — RBAC + ABAC + Audit on every module

Every module must support RBAC, ABAC, and Audit Logging.

### Rule 5 — Every API is versioned, documented, tested

OpenAPI documentation is mandatory.

### Rule 6 — Event-driven where possible

Example:

Attendance Approved → Event → Payroll → Notifications → Reports

### Rule 7 — Tenant isolation

Every feature must support tenant isolation. Every table has `TenantId`; every query
is tenant-filtered. No cross-tenant access, ever.

### Rule 8 — Every architectural decision is documented

Architectural forks become an ADR in `docs/16-decisions/`.

### Rule 9 — SOLID

All code must follow SOLID principles (and DRY, KISS, YAGNI, Clean Architecture, DDD —
see `ARCHITECTURE_PRINCIPLES.md`).

### Rule 10 — Test coverage

* Unit Test Coverage ≥ 85%
* Integration Tests
* End-to-End Tests

---

## Mandatory last step of EVERY task

Before you finish any task, **append an entry to `.ai/PROJECT_STATE.md`**
(Change Log section): date, who/which agent, what was produced, and the document's
status. This file is the project's memory. A task that does not update it is not
complete.

---

## Technology Standards

Frontend

* React
* Next.js
* TypeScript

Backend

* .NET (Primary)
* Node.js (Specialized Services)

Database

* SQL Server

Caching

* Redis

Search

* Elasticsearch

Storage

* Azure Blob Storage

Messaging

* RabbitMQ / Azure Service Bus

Version Control

* GitHub

CI/CD

* GitHub Actions

---

## Development Workflow

Research → Documentation → Architecture → Database → UX/UI → API Design →
Development → Testing → Security Review → Release.

**No phase may be skipped.** A phase may not start or advance until the prior phase's
required documents are `Approved`. Hard gate example: **Phase 2 Product Discovery cannot
start until Phase 1 Market Research is complete and its required documents are
`Approved`.** Use `/next` to see what comes next; `/start-phase <n>` to begin one.

---

## Documentation First Policy

Every output must be stored in `/docs`. No implementation without documentation.

---

## AI Agent Collaboration

Every agent must:

1. Read previous approved documents.
2. Reference existing decisions (ADRs in `docs/16-decisions/`).
3. Avoid duplicate work.
4. Document assumptions.
5. Request clarification when requirements are unclear.

---

## Success Criteria

The platform must allow:

* New customers without code changes
* New workflows without code changes
* New forms without code changes
* New reports without code changes
* New modules via extensions
* New integrations via connectors

End Goal: a world-class enterprise HRMS platform.

---

## Always-loaded context

@.ai/HRMS_Plan.md
@.ai/ARCHITECTURE_PRINCIPLES.md
@.ai/PROJECT_STATE.md

## Read-on-demand standards (do NOT preload — read the relevant one when the task touches that area)

* Backend / .NET → `docs/20-standards/CODING_STANDARDS_DOTNET.md`
* Frontend / React → `docs/20-standards/CODING_STANDARDS_REACT.md`
* Database → `docs/20-standards/DATABASE_STANDARDS.md`
* API → `docs/20-standards/API_STANDARDS.md`
* Security → `docs/20-standards/SECURITY_STANDARDS.md`
* Testing → `docs/20-standards/TESTING_STANDARDS.md`
* UI → `docs/20-standards/UI_STANDARDS.md`

## Templates (always use when creating a new document)

`docs/19-templates/` — PRD, Feature, API Spec, DB Design, Test Plan, UI Screen, ADR.

---

## Documentation map (`docs/`)

`01-market-research` `02-product-requirements` `03-gap-analysis` `04-roadmap`
`05-architecture` `06-database` `07-ui-ux` `08-api-specs` `09-development`
`10-testing` `11-release` `12-security` `13-compliance` `14-integrations`
`15-ai` `16-decisions` `17-meeting-notes` `18-customer-customizations`
`19-templates` `20-standards` `21-product-backlog`

## The agent organization

Specialist agents live in `.Codex/agents/` (the executable source of truth).
`.ai/AGENTS.md` is the human-readable roster. Every agent: reads approved docs first,
produces documentation only unless in the Development phase, writes to its assigned
`docs/` folder, and updates `PROJECT_STATE.md` as its final step.
