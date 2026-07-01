# Technical Design - Core HR and Employee Self-Service

Module: Core HR
Phase: 7A / Sprint S4
Owner: .NET Architect (Agent 13)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Core HR and ESS.

## Architecture

Core HR owns employee master data and exposes governed APIs/events to other modules. Other
modules must not directly write Core HR tables. Effective-dated records are managed by the
platform effective-dating service.

```text
Core HR API -> Core HR Application -> Employee Domain
                  |       |       |
          Effective Dating Audit Event Bus Workflow
```

## Components

- Employee Profile Service: person, employment, contact, emergency, document metadata.
- Assignment Service: job, manager, org, branch/office, location, grade, legal entity,
  cost center.
- Organization Service: org units, reporting lines, hierarchy views.
- ESS Change Service: self-service requests routed through Workflow Studio.
- Employee Search Provider: tenant-scoped searchable read model.
- Integration Publisher: emits employee and assignment events.

## API Requirements

APIs under `/api/v1/hr` cover employees, assignments, branch/office assignment, org units,
locations, legal entities, designations, grades, ESS change requests, and as-of reads. OpenAPI shall define
field classification, pagination, filters, idempotency for create/import, and error model.

## Data Rules

- Employee record creation requires tenant, legal entity, employee number, status, and
  primary assignment.
- Assignment, manager, department, grade, branch/office, location, and compensation-impacting attributes
  are effective-dated.
- No hardcoded employee lifecycle transitions; transitions are configuration and workflow
  governed.
- Employee number strategy is tenant/legal-entity configurable.

## Security

Permissions include `Employee.ViewSelf`, `Employee.ViewTeam`, `Employee.Manage`,
`Employee.SensitiveView`, `Org.Manage`, and `Employee.Import`. ABAC restricts manager and
HR access by team, branch/office, legal entity, location, department, and data classification.

## Events

`EmployeeCreated`, `EmployeeUpdated`, `EmployeeAssignmentChanged`, `EmployeeManagerChanged`,
`EmployeeStatusChanged`, `EmployeeEssChangeRequested`, `EmployeeEssChangeApproved`.

## Observability

Track employee API latency, import errors, hierarchy rebuild duration, ESS workflow aging,
search indexing lag, and failed event publishing.

## Acceptance Criteria

1. Core HR exposes as-of employee and assignment APIs.
2. ESS updates use Workflow Studio and preserve audit evidence.
3. Manager team query uses ABAC and hierarchy service.
4. Events are published through outbox.
5. Employee search and reports use governed read models.
6. Employee branch/office assignment is available for branch-scoped authorization and
   downstream attendance/payroll/reporting use.

## External References

- Microsoft row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
- Zoho People market reference: https://www.zoho.com/people/
- BambooHR market reference: https://www.bamboohr.com/

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Phase 7A Branch / Office Addendum

Core HR must comply with `docs/09-development/TECH-BRANCH-001-technical-design.md` for
employee branch assignment and branch-scoped access.

## Approval

.NET Architect: ____ - Solution Architect: ____ - Security Architect: ____ - Status: Approved
