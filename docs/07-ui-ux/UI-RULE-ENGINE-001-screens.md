# UI Design - Rule Engine

Module: Platform Foundation
Phase: 7A / Sprint S3
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 4 of 5 for Rule Engine.

## UX Goals

Authorized business users should configure and test rules safely without needing
developers. The UI must reduce errors through templates, validation, previews, simulation,
and approval workflow.

## Screen A - Rule Library

Lists rule sets by module, status, effective date, owner, classification, current
published version, and last changed by. Users can search and filter by module: Leave,
Attendance, Payroll, Workflow, Reporting, Configuration.

## Screen B - Rule Builder

Supports guided condition builder, expression editor for advanced users, decision-table
view, approved function list, and live validation. No free execution of scripts is allowed.

## Screen C - Simulation Lab

Users select sample employee/context, business date, and expected result. Output shows
matched path, calculated values, warnings, and explanation. Simulations can be attached to
approval evidence.

## Screen D - Publish Review

Shows diff from current version, impacted modules, effective date, test coverage summary,
approvers, rollback option, and high-risk warning for payroll/compliance rules.

## Screen E - Rule History

Timeline of draft, approved, published, deprecated, and retired versions with audit link
and as-of preview.

## Acceptance Criteria

1. Business user can create a decision table from a template.
2. Invalid expressions are highlighted before save.
3. Simulation output clearly shows why a rule matched.
4. Publishing a high-risk rule requires approval evidence.
5. Rule history can open previous versions as read-only.

## External References

- CEL: https://cel.dev/
- OMG DMN: https://www.omg.org/spec/DMN/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

UX/UI Architect: ____ - Product Owner: ____ - HR/Payroll Reviewer: ____ - Status: Approved
