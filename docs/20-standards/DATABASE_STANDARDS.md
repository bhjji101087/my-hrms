# DATABASE_STANDARDS.md

# SQL Server Standards

---

# Naming Conventions

Tables

PascalCase

Example:

Employee

LeaveRequest

PayrollRun

---

Columns

PascalCase

Example:

EmployeeId

FirstName

CreatedDate

---

Primary Keys

TableNameId

Example:

EmployeeId

LeaveRequestId

---

Foreign Keys

ReferencedTableId

Example:

EmployeeId

DepartmentId

---

# Mandatory Columns

Every table must contain:

TenantId

CreatedBy

CreatedDate

ModifiedBy

ModifiedDate

IsDeleted

VersionNumber

---

# Soft Delete Policy

Never physically delete business data.

Use:

IsDeleted

---

# Audit Policy

All critical tables require audit history.

---

# Schema Strategy

Core

Employee

Attendance

Leave

Payroll

Recruitment

Performance

Workflow

Security

Audit

Integration

AI

---

# Indexing Standards

Primary Keys

Foreign Keys

Frequently Queried Columns

TenantId

Mandatory Index

---

# Migration Standards

EF Core Migrations Only

No manual production schema changes.

---

# Performance Standards

Avoid:

SELECT *

Use:

Explicit Columns

---

# Security Standards

No dynamic SQL without validation.

Parameterized queries only.
