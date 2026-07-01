# Database Design - Core HR and Employee Self-Service

Module: Core HR
Schema: `hr`
Phase: 7A / Sprint S4
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Core HR and ESS.

## Tables

```text
hr.Person
  PersonId, TenantId, LegalName, PreferredName, DateOfBirthEncrypted,
  Gender, PrimaryEmail, PrimaryPhoneEncrypted, DataClassification, audit columns

hr.Employee
  EmployeeId, TenantId, PersonId, EmployeeNumber, LegalEntityId,
  EmploymentStatus, JoiningDate, ExitDate, WorkerType, audit columns

hr.EmployeeAssignment
  AssignmentId, TenantId, EmployeeId, BranchOfficeId, LegalEntityId, DepartmentId,
  DesignationId, GradeId, LocationId, ManagerEmployeeId, CostCenterId,
  EffectiveFrom, EffectiveTo, ChangeReason, ApprovalReferenceId, audit columns

hr.OrganizationUnit
  OrganizationUnitId, TenantId, ParentOrganizationUnitId, Code, Name,
  EffectiveFrom, EffectiveTo, IsActive, audit columns

hr.Location
  LocationId, TenantId, Code, Name, CountryCode, StateCode, City,
  TimeZone, CalendarId, EffectiveFrom, EffectiveTo, audit columns

hr.EssChangeRequest
  EssChangeRequestId, TenantId, EmployeeId, ChangeType, PayloadJson,
  Status, WorkflowInstanceId, EffectiveFrom, audit columns

hr.EmployeeDocumentMetadata
  EmployeeDocumentMetadataId, TenantId, EmployeeId, DocumentType,
  FileReference, Classification, ValidFrom, ValidTo, audit columns
```

## Indexes

- `Employee`: unique `(TenantId, EmployeeNumber)`, `(TenantId, EmploymentStatus)`.
- `EmployeeAssignment`: `(TenantId, EmployeeId, EffectiveFrom, EffectiveTo)`,
  `(TenantId, ManagerEmployeeId, EffectiveFrom)`.
- `OrganizationUnit`: `(TenantId, ParentOrganizationUnitId)`.
- `EssChangeRequest`: `(TenantId, EmployeeId, Status)`.

## RLS and Security

All tables are tenant-scoped. Sensitive fields are encrypted or masked. Manager and HR
visibility is enforced in service layer and ABAC policies in addition to RLS.

## Effective Dating

Assignment, branch/office, org, location, grade, designation, and manager relationships
are effective-dated. Backdated changes require reason and may require approval based on
tenant policy. Branch/office hierarchy and branch scope tables are defined in
`DB-DESIGN-BRANCH-001`.

## Retention

Employee lifecycle data retention follows legal, payroll, and compliance obligations.
Document metadata retention follows document classification and legal hold.

## Acceptance Criteria

1. Employee number is unique per tenant.
2. Assignment history supports as-of queries.
3. Manager hierarchy can be built from effective-dated assignments.
4. Sensitive fields are protected.
5. RLS blocks cross-tenant employee data.
6. Branch/office assignment supports as-of queries and branch admin scoping.

## External References

- SQL Server temporal tables: https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
- SQL Server row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - HR Domain Expert: ____ - Security Architect: ____ - Status: Approved
