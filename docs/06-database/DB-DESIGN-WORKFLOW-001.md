# Database Design - Workflow Studio

Module: Platform Foundation
Schema: `workflow`
Phase: 7A / Sprint S3-S9
Owner: Database Architect (Agent 7)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 3 of 5 for Workflow Studio.

## Tables

```text
workflow.WorkflowDefinition
  WorkflowDefinitionId, TenantId, Code, Name, ModuleScope,
  CurrentPublishedVersionId, IsActive, audit columns

workflow.WorkflowDefinitionVersion
  WorkflowDefinitionVersionId, TenantId, WorkflowDefinitionId, VersionNumberText,
  EffectiveFrom, EffectiveTo, Status, DefinitionJson, ApprovalWorkflowInstanceId,
  PublishedBy, PublishedAt, audit columns

workflow.WorkflowInstance
  WorkflowInstanceId, TenantId, WorkflowDefinitionVersionId, BusinessModule,
  BusinessEntityName, BusinessEntityId, Status, StartedBy, StartedAt,
  CompletedAt, CorrelationId, audit columns

workflow.WorkflowTask
  WorkflowTaskId, TenantId, WorkflowInstanceId, StepCode, AssignedToUserId,
  AssignedToRoleId, DueAt, Status, DelegatedFromUserId, EscalatedAt, audit columns

workflow.WorkflowDecision
  WorkflowDecisionId, TenantId, WorkflowTaskId, Decision, Comment,
  DecidedBy, OnBehalfOfUserId, DecidedAt, RuleSetVersionId, audit columns

workflow.WorkflowSlaEvent
  WorkflowSlaEventId, TenantId, WorkflowInstanceId, WorkflowTaskId,
  EventType, TriggeredAt, OutcomeStatus, audit columns
```

## Storage Rules

- Published workflow definition versions are immutable.
- Runtime instance state changes are audited.
- Comments and attachments store metadata only; binary files use approved storage.
- Running instances reference exact definition version.

## Indexes

- `WorkflowTask`: `(TenantId, AssignedToUserId, Status, DueAt)` for inbox.
- `WorkflowInstance`: `(TenantId, BusinessModule, BusinessEntityName, BusinessEntityId)`.
- `WorkflowDefinitionVersion`: `(TenantId, WorkflowDefinitionId, Status, EffectiveFrom)`.
- `WorkflowDecision`: `(TenantId, WorkflowTaskId, DecidedAt)`.

## RLS and Security

Workflow tables are tenant-scoped. Task queries apply ABAC for assignee, manager, delegate,
HR, payroll, and auditor scopes. Payroll and security workflows may require stricter access.

## Retention

Workflow history for payroll, compliance, and employee record decisions follows related
business record retention. Task inbox operational data may be archived after completion
while preserving audit and decision evidence.

## Acceptance Criteria

1. Running workflow instance is pinned to a published version.
2. Inbox indexes support current task lookup.
3. Delegation and escalation evidence is persisted.
4. RLS blocks cross-tenant task visibility.
5. Workflow history links back to source business entity.

## External References

- OMG BPMN: https://www.omg.org/spec/BPMN/
- SQL Server row-level security: https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security

References last validated: 2026-06-28.

## Phase 7A Data Classification and Migration Addendum

This database design must comply with
`docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Database Architect: ____ - Solution Architect: ____ - Security Architect: ____ - Status: Approved
