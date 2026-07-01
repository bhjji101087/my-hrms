# UI Design - Audit and Time Machine

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 4 of 5 for Audit and Time Machine.

## UX Goals

The experience must help authorized users investigate confidently without exposing
unnecessary personal data. It should feel like evidence review: clear filters, clear
lineage, clear before/after values, and clear export controls.

## Screen A - Audit Search

Filters: date range, module, action type, actor, subject, entity, risk level, correlation
ID, approval reference, and source type. Results show action, actor, subject, entity,
time, reason, risk, and evidence availability.

## Screen B - Entity History

Shows a chronological timeline for one employee, leave request, attendance record, payroll
run, rule version, workflow definition, or configuration item. Each entry opens field-level
change detail, workflow approval reference, and event correlation.

## Screen C - Time Machine

Authorized users select entity, business date, and optional system time. The UI displays a
clear historical banner and reconstructs the selected state with differences from current
state.

## Screen D - Security Events

Shows login, MFA, permission change, impersonation, break-glass, API key, and abnormal
authorization events. High-risk events are visually prominent and linked to runbooks where
applicable.

## Screen E - Evidence Export

Requires purpose, date range, data classification notice, approval if configured, and
expiry. Export status and download history are audited.

## Accessibility and Privacy

WCAG 2.2 AA applies. Sensitive fields are masked by default and require explicit reveal
permission. Export buttons are disabled when filters are too broad or policy blocks export.

## Acceptance Criteria

1. Users can find audit events by correlation ID and entity.
2. Entity history shows before/after fields according to permission.
3. Time Machine mode is visually distinct from current view.
4. Evidence exports require purpose and create audit records.
5. Unauthorized users see no sensitive or cross-tenant evidence.

## External References

- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

References last validated: 2026-06-28.

## Phase 7A UX Hardening Addendum

This UI design must comply with
`docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

UX/UI Architect: ____ - Security Architect: ____ - Product Owner: ____ - Status: Approved
