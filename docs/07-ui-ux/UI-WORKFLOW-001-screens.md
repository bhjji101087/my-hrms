# UI Design - Workflow Studio

Module: Platform Foundation
Phase: 7A / Sprint S3-S9
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 4 of 5 for Workflow Studio.

## UX Goals

Workflow Studio must make configuration powerful but safe. Users should see flow shape,
approval logic, task ownership, SLA, and risk before publishing. Everyday approvers should
use a simple task inbox without needing to understand the designer.

## Screen A - Workflow Library

Lists workflow definitions by module, status, effective date, owner, published version,
last edited, and risk classification. Includes templates for Leave, Attendance,
Payroll Approval, ESS Change, Rule Publish, and Configuration Promotion.

## Screen B - Visual Workflow Designer

Canvas with start, task, condition, parallel approval, escalation, notification, and end
nodes. Properties panel defines assignee rule, SLA, decision options, comments, and
business outcome. Validation panel shows errors before publish.

## Screen C - Task Inbox

Unified inbox for managers, HR, payroll, and admins. Cards show requester, type, age, SLA,
delegation, required action, related record, and policy hints. Bulk action is controlled by
workflow and permission.

## Screen D - Instance Tracker

Timeline of submitted, assigned, delegated, escalated, approved/rejected, and completed
steps. Visible from source records such as leave request or payroll run.

## Screen E - Publish and Migration Review

Shows version diff, affected modules, effective date, running-instance policy, simulation
results, and approval route. In-flight migration requires explicit plan.

## Acceptance Criteria

1. Admin can design a conditional two-step approval workflow.
2. Validation prevents publishing incomplete or unsafe workflows.
3. Approvers can complete tasks from unified inbox.
4. Instance tracker clearly shows status and decision history.
5. Published version diff is readable before approval.

## External References

- OMG BPMN: https://www.omg.org/spec/BPMN/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

UX/UI Architect: ____ - Product Owner: ____ - HR Operations Reviewer: ____ - Status: Approved
