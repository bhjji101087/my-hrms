# Feature Specification - Core HR and Employee Self-Service

Feature Name: Core HR and Employee Self-Service
Module: Core HR
Phase: 7A / Sprint S4
Owner: Product Owner (Agent 2)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 1 of 5 for Core HR and ESS. Implements PRD FR-003.

## Purpose

Core HR is the system of record for people, employment, organization, assignment, manager,
branch/office, location, and lifecycle data. Every later HR module depends on accurate Core HR data, so
Phase 7A must establish a clean, effective-dated, auditable employee master and employee
self-service foundation.

## Market and Enterprise Context

Vendor portals such as Zoho People, BambooHR, Keka, greytHR, and Darwinbox treat employee
profiles, org structure, document records, self-service updates, and manager visibility as
core HR capabilities. Customer frustration usually appears when employee data is duplicated,
history is overwritten, manager hierarchy is wrong, or self-service changes bypass approval.

## Scope

In scope:
- Employee master profile.
- Employment, assignment, manager, department, designation, grade, branch/office, location,
  and legal entity.
- Employee lifecycle statuses.
- ESS profile view and controlled profile update requests.
- Basic HR document metadata references.
- Effective-dated organization and job data.
- Audit, events, and reporting hooks.

Out of scope:
- Full onboarding/offboarding automation.
- Document generation and e-signature.
- Performance, recruitment, learning, engagement, and assets.

## Business Requirements

1. HR users shall create and maintain employee records with tenant isolation.
2. Employee assignments and compensation-relevant job attributes shall be effective-dated.
3. Employees shall view permitted personal, job, manager, and document metadata.
4. Employee self-service changes shall route through Workflow Studio where approval is required.
5. Manager visibility shall follow organization hierarchy and ABAC rules.
6. Core HR changes shall emit events for leave, attendance, payroll, workflow, reports, and AI.
7. Employee identifiers shall be unique per tenant and support legal entity-specific numbering.
8. Sensitive fields shall be masked or hidden based on permission and data classification.
9. Branch/office assignment shall be effective-dated and available for authorization,
   attendance, payroll, workflow, and reporting.

## Key Entities

- Person and Employee.
- Employment.
- Assignment.
- Organization Unit.
- Branch / Office.
- Legal Entity.
- Location.
- Designation, Grade, Cost Center.
- Emergency Contact.
- Document Metadata.

## Acceptance Criteria

1. HR creates an employee and assignment with effective start date.
2. Employee views own profile and submits an update request through workflow.
3. Manager sees only assigned team members.
4. Payroll can retrieve employee assignment as-of pay period.
5. All employee profile changes are audited and evented.
6. Employee branch/office assignment supports as-of queries and branch admin scoping.

## External References

- Zoho People market reference: https://www.zoho.com/people/
- BambooHR market reference: https://www.bamboohr.com/
- Keka market reference: https://www.keka.com/
- Darwinbox market reference: https://darwinbox.com/

References last validated: 2026-06-28.

## Approval

Product Owner: ____ - HR Domain Expert: ____ - Solution Architect: ____ - Status: Approved
