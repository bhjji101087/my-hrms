# Feature Specification - Effective Dating and Bitemporal Core

Feature Name: Effective Dating and Bitemporal Core
Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: Product Owner (Agent 2)
Created Date: 2026-06-28
Last Updated: 2026-06-28
Version: 1.1
Status: Approved

> Doc 1 of 5 for Effective Dating. Companions: Technical Design, Database Design,
> UI Design, and Test Plan. Implements PRD FR-014 and ADR-007.

## Purpose

The platform must answer "what was true on a given date" and "what did the system know
at a given time" for employee, organization, policy, salary, leave, attendance, payroll,
workflow, rule, and compliance data. Retrofitting this later is risky and expensive, so
Phase 7A must establish one shared effective-dating pattern before business modules start.

## Market and Enterprise Context

Enterprise HR products succeed when HR teams can schedule future changes, correct past
records, explain payroll differences, and audit historical decisions. Market portals such
as Zoho People, greytHR, Keka, Darwinbox, and BambooHR expose employee profile history,
attendance/leave/payroll configuration, and workflow-driven updates; customer pain usually
appears when history is overwritten or payroll cannot be explained after a backdated change.

## Scope

In scope:
- Valid-time effective dating for business facts.
- System-time history for auditability and reconstruction.
- Future-dated, backdated, corrected, cancelled, and superseded changes.
- Standard open-ended active-record representation using `EffectiveTo = NULL` unless a
  different enterprise standard is approved.
- Standard `asOfDate` query semantics for APIs, reports, payroll, workflow, rules,
  analytics, and audit views.
- Overlap prevention for single-active-record periods.
- Mandatory effective-date validation across APIs, services, and database constraints.
- Mandatory reason, approver, and audit record for backdated or payroll-impacting changes.
- Common rules that future bulk effective-dated operations must reuse.

Out of scope:
- Full data warehouse slowly changing dimensions.
- Legal advice on statutory correction handling.
- Module-specific business rules, which stay in each module and the Rule Engine.
- Bulk-operation import, approval, rollback, and user-interface details, which shall be
  defined in a future feature or technical design document.

## Business Requirements

1. The platform shall support effective-dated records with `EffectiveFrom` and
   `EffectiveTo` wherever the business fact can change over time.
2. The platform shall support system-time history for approved tables using SQL Server
   temporal tables or an equivalent approved pattern.
3. Active records without a known end date shall use `EffectiveTo = NULL` unless a
   different enterprise standard is approved through an ADR or approved database standard.
4. For entities that allow only one active period, the platform shall allow only one
   open-ended active record for the same tenant-scoped business key.
5. Creating a new current or future effective record shall automatically close the
   previous active record when the entity uses a single-active-period model and the
   previous period is still open.
6. Users with permission shall be able to schedule future-dated changes.
7. Backdated changes shall require reason capture and may require approval based on tenant
   policy and module impact.
8. `EffectiveFrom` shall be less than or equal to `EffectiveTo` when `EffectiveTo` is not
   `NULL`.
9. Zero-length or invalid date ranges shall be rejected unless the entity explicitly
   supports them through an approved platform configuration.
10. The system shall prevent invalid overlapping active periods unless a table explicitly
   supports multiple concurrent records.
11. Effective-date validation shall be enforced consistently across APIs, application
    services, domain services, and database constraints.
12. Business modules shall consume a shared effective-dating service and shall not invent
    separate local history patterns.
13. Payroll, leave balance, attendance, workflow, rules, reports, and analytics shall run
    against the same as-of business-date behavior.
14. Platform APIs that expose historical business state shall use the standard `asOfDate`
    parameter name and semantics unless a later approved API standard supersedes it.
15. Historical records shall remain tenant-isolated and governed by RBAC, ABAC, RLS,
    audit, and retention policy.
16. Future bulk effective-dated operations, such as annual salary revisions, policy
    updates, organization restructuring, or mass designation changes, shall follow the
    same validation, approval, audit, overlap-prevention, tenant-isolation, and
    effective-dating rules as individual updates.

## Design Notes

### Open-Ended Records

The platform default for an active record without a known end date is `EffectiveTo = NULL`.
Sentinel dates such as 9999-12-31 are not the default unless a different enterprise
standard is approved. For single-active entities, only one open-ended active record may
exist for the same tenant-scoped business key.

When a new current or future record is created for a single-active entity, the platform
closes the previous open record using the approved effective-period boundary convention.
For date-based effective periods, the previous record's `EffectiveTo` is set to the
tenant-local date immediately before the new record's `EffectiveFrom`. The write operation
must remain tenant-scoped, auditable, and safe for future-dated activation.

### Effective Date Validation

All effective-dated entities must apply the same core validation rules:

- `EffectiveFrom` is required.
- `EffectiveTo` may be `NULL` only for an open-ended period.
- `EffectiveFrom` must be less than or equal to `EffectiveTo` when `EffectiveTo` is not
  `NULL`.
- Zero-length or invalid ranges are rejected unless explicitly supported for the entity.
- Overlapping periods are rejected for single-active entities.
- Validation behavior is the same whether the request arrives through an API, service,
  workflow action, import, scheduled job, or database write path.

These rules are platform standards, not module-specific business rules. Entity-specific
exceptions require approved design documentation and must remain compatible with SQL Server
temporal tables, EF Core temporal support, and the shared effective-dating service.

### Time Zone Standard

Effective dates represent tenant-local business dates. They are interpreted using the
tenant's approved time zone and calendar context, not the user's browser time zone or the
server's local time zone. This keeps scheduled future changes, payroll calculations,
workflow due dates, reports, and rules deterministic for each tenant.

Audit, security, and system timestamps are stored in UTC. APIs and reports may display
localized values, but the stored system-time record remains UTC so that bitemporal
reconstruction is unambiguous across tenants, regions, integrations, and background jobs.

### As-Of Query Pattern

The platform standard parameter for valid-time business history is `asOfDate`. It means
"return the record or calculated result that is valid for the tenant-local business date."
All modules must use the same parameter name and semantics for historical APIs, reports,
payroll, workflow evaluation, rules-engine execution, and analytics.

System-time reconstruction may be exposed separately where approved, but modules must not
create their own historical-query parameter names or incompatible as-of behavior.

### Bulk Effective-Dated Changes

Enterprise HR operations often change many records together, including annual salary
revisions, policy updates, organization restructuring, and mass designation changes. This
feature establishes the standards that bulk operations must follow, but it does not define
the bulk-operation implementation.

Future bulk designs must reuse the same effective-date validation, approval routing, audit
trail, overlap prevention, tenant isolation, RBAC, ABAC, and scheduled-activation behavior
as individual effective-dated updates.

## User Roles

- Employee: views permitted historical self-service data.
- Manager: views permitted team history.
- HR Admin: schedules and corrects employee/org/policy changes.
- Payroll Admin: reviews payroll-impacting historical changes.
- Auditor: views approved as-of and time-machine evidence.
- Tenant Admin: configures approval requirements for sensitive changes.

## Acceptance Criteria

1. A future-dated job change becomes active on the correct date without code deployment.
2. A backdated salary change records reason, approver, effective period, and audit trail.
3. Payroll can calculate using the correct salary and policy as-of the pay period.
4. The platform blocks overlapping effective periods for single-active records.
5. Reports and audit views can reconstruct both business-date and system-time history.
6. Active open-ended records use `EffectiveTo = NULL`, and single-active entities cannot
   have more than one open-ended active record for the same tenant-scoped business key.
7. Creating a new current or future record closes the previous open record where the entity
   follows a single-active-period model.
8. Invalid effective-date ranges, unsupported zero-length ranges, and overlapping periods
   are rejected consistently across API, service, workflow, import, job, and database write
   paths.
9. Effective dates behave as tenant-local business dates, while audit and system timestamps
   are stored in UTC.
10. APIs, reports, payroll, workflow, rules, and analytics use the common `asOfDate`
    semantics for business-date history.
11. Future bulk effective-dated operation designs demonstrate that bulk changes follow the
    same validation, approval, audit, and effective-dating rules as individual updates.

## External References

- Microsoft SQL Server temporal tables: https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
- EF Core SQL Server temporal tables: https://learn.microsoft.com/en-us/ef/core/providers/sql-server/temporal-tables
- Zoho People market reference: https://www.zoho.com/people/
- BambooHR market reference: https://www.bamboohr.com/

References last validated: 2026-06-28.

## Approval

Product Owner: Approved by Bhajan Lal 2026-06-28 - Solution Architect: Approved by Codex 2026-06-28 - Database Architect: Pending companion database design approval - Status: Approved
