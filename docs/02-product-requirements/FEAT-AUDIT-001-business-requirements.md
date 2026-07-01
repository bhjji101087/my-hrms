# Feature Specification - Audit and Time Machine

Feature Name: Audit and Time Machine
Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: Product Owner (Agent 2)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 1 of 5 for Audit and Time Machine. Implements PRD FR-008.

## Purpose

Every meaningful business and security action must be explainable. The platform must show
who changed what, when, from where, under which tenant, through which role or delegated
context, and why. Time Machine allows authorized users to reconstruct historical state
without weakening privacy or tenant isolation.

## Market and Enterprise Context

HR systems hold employment, payroll, identity, attendance, and compliance records. Market
expectation is no longer simple "last modified by"; enterprise customers expect audit
history, approval evidence, policy version evidence, export tracking, and investigation
support. Customer frustration appears when HR and payroll teams cannot explain historical
salary, leave, or statutory differences.

## Scope

In scope:
- Business change audit for all Phase 7A modules.
- Security audit for authentication, authorization, impersonation, emergency access, and
  configuration changes.
- Time Machine read views for approved entities.
- Export, report, and administrative action audit.
- Legal hold and retention integration.
- Tamper-evidence strategy for high-risk audit records.

Out of scope:
- External SIEM product implementation.
- Full forensic case-management system.
- Replacing database backups.

## Business Requirements

1. Every create, update, delete, approval, rejection, export, import, login, permission
   change, configuration change, and payroll action shall create audit evidence.
2. Audit records shall include tenant, actor, subject, action, entity, before/after values
   where appropriate, reason, source IP/device where permitted, correlation ID, and time.
3. Delegation and impersonation shall include `OnBehalfOf` details.
4. Time Machine views shall reconstruct approved historical states using effective-dated
   and temporal data.
5. Audit access itself shall be audited.
6. Audit retention shall follow compliance policy, legal hold, and ADR-022.
7. Audit evidence shall be searchable by authorized users without exposing cross-tenant data.
8. High-risk audit records shall support tamper-evidence through hash chaining or ledger
   table strategy approved by architecture.

## User Roles

- Auditor: searches and exports approved evidence.
- Security Admin: reviews security events.
- HR Admin: reviews employee and workflow history.
- Payroll Admin: reviews payroll run and component history.
- Tenant Admin: configures audit retention and access policy within platform limits.

## Acceptance Criteria

1. Any employee salary change shows before/after values, reason, actor, approval, and date.
2. A payroll run can be traced to rule versions, source data, approvals, and generated output.
3. Audit search cannot return another tenant's records.
4. Exporting audit data creates a separate audit record.
5. Time Machine reconstructs a selected employee record as of a selected date.

## External References

- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- NIST SP 800-92 Log Management: https://csrc.nist.gov/pubs/sp/800/92/final
- SQL Server ledger overview: https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview

References last validated: 2026-06-28.

## Approval

Product Owner: ____ - Security Architect: ____ - Compliance Reviewer: ____ - Status: Approved
