# UI Design - Effective Dating and History

Module: Platform Foundation
Phase: 7A / Sprint S2
Owner: UX/UI Architect (Agent 11)
Created Date: 2026-06-28
Last Updated: 2026-06-28
Version: 1.1
Status: Approved

> Doc 4 of 5 for Effective Dating. This is a shared UX pattern consumed by HR, Payroll,
> Leave, Attendance, Rules, Workflow, and Configuration screens.

## UX Goals

Users should understand whether they are editing current data, scheduling future data, or
correcting historical data. The interface must prevent accidental overwrites and make the
business impact of backdated changes visible.

The pattern must be reusable across HR, Payroll, Leave, Attendance, Workflow, Rules, and
Configuration screens. It must not introduce module-specific business logic; module impact,
approval, and validation details come from the shared Effective Dating service, Workflow
Studio, Rule Engine, audit, and permission model.

## Shared Components

- Effective Date Picker: current, future, and backdated modes.
- Effective Date Preview: shows when the proposed change becomes active and which current
  record will automatically close.
- Visual History Timeline: shows Current, Future, Historical, Corrected, Superseded, and
  Cancelled versions with effective periods, status, approver, reason, source, and audit
  summary.
- As-Of Viewer: opens any supported screen as of a selected date.
- Change Impact Panel: shows possible payroll, leave, workflow, reporting, and compliance
  impact before submit.
- Overlap Conflict Validator: checks the proposed period in real time and blocks submit
  until conflicts are resolved.
- Correction Reason Dialog: mandatory for backdated or sensitive changes.
- Compare Versions View: highlights field-level differences between two versions.
- Audit Information Drawer: expands from timeline, compare, and change preview surfaces.
- Bulk Effective-Dated Change Preview: summarizes affected records, validation state,
  warnings, errors, and approval impact before execution.

## Screen A - Schedule Change

Used in employee assignment, salary, policy, leave type, workflow definition, and rule
version screens. It requires `EffectiveFrom`, optional `EffectiveTo`, reason, and approval
preview where configured.

The screen shows an Effective Date Preview after the user selects a date:

- Proposed active date and effective period.
- Current record that will close automatically, including its new `EffectiveTo`.
- Whether the change is current, future-dated, or backdated.
- Required approval route and reason requirements.
- Any downstream impact severity.

The submit action remains disabled while required fields are missing, the user lacks
permission, overlap conflicts exist, the selected period is invalid, or approval evidence
is incomplete. Disabled actions must show a clear reason through inline text or accessible
help text instead of failing only after submit.

If the user leaves the page with unsaved effective-dated changes, the UI must show a
confirmation warning. The warning must identify that date, reason, impact, and draft values
may be lost unless the user saves or discards the change.

## Screen B - History Timeline

Shows a visual chronological record of Current, Future, Historical, Corrected, Superseded,
and Cancelled versions. Users can filter by date, status, changed by, approval reference,
and module.

The timeline replaces a simple history list. It must support:

- Status chips, icons, and accessible text for every version state.
- Effective period and open-ended indicator.
- Changed by, changed at, approved by, reason, workflow, change request, and audit
  reference summary.
- Expand/collapse details for dense enterprise histories.
- Selection of two versions for compare view.
- Read-only detail view for historical records.
- Copy Previous Version and Restore as New Change actions where permitted.

Historical versions are always read-only. Corrections, restore operations, and copy actions
create new effective-dated versions and never edit prior history. Superseded, corrected,
and cancelled versions must remain traceable in the timeline.

Standard status labels use design-system semantic tokens and must never rely on color
alone:

| Status | Label | Semantic color token |
|---|---|---|
| Current | Current | `status.success` |
| Future | Future | `status.info` |
| Historical | Historical | `status.neutral` |
| Corrected | Corrected | `status.warning` |
| Superseded | Superseded | `status.muted` |
| Cancelled | Cancelled | `status.danger` |

Tenant themes may change the resolved color values, but labels, icons, tooltips,
screen-reader text, and semantic meaning remain consistent.

## Screen C - Backdated Correction

Displays a warning, impact panel, mandatory reason, optional payroll lock warning, and
approval route. Submit is disabled until all required evidence is provided.

Real-time overlap detection must run as users change dates. The UI displays the conflicting
period, affected record, status, and recommended next step. Submission is blocked until the
conflict is resolved or the entity explicitly supports overlap.

The Change Impact Panel uses four impact severity levels:

- Informational: no expected downstream recalculation or approval escalation.
- Warning: downstream review may be needed.
- Payroll Impact: payroll, arrears, salary, tax, or pay-period calculations may change.
- Compliance Impact: statutory, audit, policy, or legal evidence may be affected.

Impact levels are shown with semantic tokens, text labels, and icons. They must be
announced to assistive technologies and must not depend only on color.

## Screen D - As-Of Mode

Global date control lets authorized users view data as of a business date. A visible banner
shows the selected date so users do not confuse history with current data.

As-Of Mode must show a persistent "Viewing Historical Data" indicator across the screen,
including detail panels, related widgets, tables, and exported/printable views where
applicable. The indicator includes the selected tenant-local business date and a clear
return-to-current action.

In As-Of Mode, edit actions are hidden or disabled based on permission and context. If an
action is disabled because the user is viewing historical data, the UI explains that the
user must return to current view or create a new effective-dated change.

## Screen E - Compare Versions

Compare Versions View displays field-level differences between two selected versions.
For every changed field it shows:

- Field label.
- Old value.
- New value.
- Changed by.
- Change reason.
- Effective date and effective period.
- Approval reference and audit reference where available.

Unchanged fields may be collapsed by default. Sensitive fields follow RBAC/ABAC masking and
redaction rules. Export, print, and copy behavior must preserve permission filtering.

## Screen F - Audit Information Drawer

The Audit Information Drawer is available from timeline items, compare rows, correction
previews, and submitted change summaries. It shows:

- Changed by and changed at.
- Approved by and approved at.
- Reason.
- Workflow instance or task reference.
- Change request reference.
- Audit reference.
- System timestamps in localized display form with UTC source retained in metadata.

The drawer is read-only. It must support keyboard focus management, escape-to-close,
screen-reader labels, and responsive full-screen behavior on mobile.

## Screen G - Bulk Effective-Dated Operations

Bulk effective-dated operation UX is a shared pattern for future large-scale changes such
as annual revisions, policy updates, organization restructuring, shift calendar updates,
and holiday calendar updates. It does not define module-specific rules.

The bulk flow includes:

- Upload or selection preview.
- Affected record count and sample records.
- Validation summary with success, warning, conflict, and error counts.
- Overlap and date-boundary errors before submission.
- Impact severity summary.
- Required approval route and reason.
- Warnings for partial failure, retry, and long-running processing.
- Progress state for queued, validating, awaiting approval, processing, partially failed,
  completed, cancelled, and failed.
- Downloadable validation error list where permitted.

Bulk submit is disabled until blocking errors are resolved and required approvals or
reason fields are complete.

## Loading and Long-Running States

Historical snapshot loading must provide clear progress indicators. Short retrieval uses
skeleton rows or inline loading states. Long-running history retrieval uses a progress
panel with entity name, selected date, retrieval stage, retry state, and safe cancel or
background option where supported.

If the system cannot retrieve the requested historical snapshot, the UI shows an actionable
error with correlation ID and preserves the selected filters/date so the user can retry
without rebuilding the query.

## Responsive Behavior

The shared pattern must work on mobile, tablet, and desktop:

- Timeline: desktop shows horizontal or two-column timeline where space permits; tablet
  uses a stacked timeline; mobile uses compact vertical cards with status, dates, and one
  primary action per item.
- Compare View: desktop uses side-by-side old/new values; tablet uses a two-column table;
  mobile stacks old value above new value per field.
- Date Picker: supports keyboard entry, calendar selection, locale-aware formatting, and
  touch-friendly controls. Mobile uses a full-screen or bottom-sheet picker.
- Impact Panel: desktop may remain side-by-side with the form; tablet stacks below the
  date section; mobile uses collapsible sections with severity summary pinned near submit.
- Audit Drawer: desktop uses a side drawer; mobile uses a full-screen drawer with clear
  close and back behavior.
- Bulk Validation Summary: desktop uses table plus summary panel; mobile uses filterable
  cards and collapsible error groups.

## Security and Accessibility

Sensitive history fields are hidden unless permission and ABAC checks allow them. WCAG 2.2
AA applies. Date fields must support keyboard entry and locale-aware display.

The UI must evaluate permissions before presenting actions. Unavailable actions are hidden
or disabled with an accessible reason, according to the action's sensitivity and disclosure
risk. Users must not learn sensitive data through disabled labels, validation text, export
names, or timeline metadata.

Accessibility requirements:

- Full keyboard support for date picker, timeline, compare view, drawers, and bulk
  validation tables.
- Visible focus states.
- Screen-reader labels and live regions for validation, overlap detection, impact severity,
  loading, and long-running snapshot retrieval.
- No color-only status or severity communication.
- Touch targets at least 44px on mobile.
- Locale-aware dates and RTL-ready layout.

## Acceptance Criteria

1. Users can schedule a future change without modifying current data.
2. Backdated corrections show impact and require reason before submission.
3. Effective Date Preview shows activation date and the current record that will close.
4. Timeline visually represents Current, Future, Historical, Corrected, Superseded, and
   Cancelled versions using standard labels, semantic colors, icons, and accessible text.
5. Users without permission cannot view sensitive history.
6. Real-time overlap detection blocks submission until conflicts are resolved.
7. Historical versions are read-only; copy, restore, and correction actions create new
   effective-dated versions.
8. Unsaved effective-dated changes warn before navigation away.
9. Audit Information Drawer shows changed by, approved by, reason, workflow, change
   request, audit reference, and timestamps.
10. Compare Versions View shows old value, new value, changed by, reason, and effective
    date for each changed field.
11. As-Of Mode has a persistent visible historical-data indicator across the screen.
12. Bulk effective-dated operation UX includes preview, validation summary, affected
    records, warnings, errors, progress, and disabled submit for blocking issues.
13. Timeline, Compare View, Date Picker, Impact Panel, Audit Drawer, and bulk validation
    summary are responsive across mobile, tablet, and desktop.
14. Historical snapshot loading provides appropriate progress indicators and retry context.
15. WCAG 2.2 AA, localization, theme tokens, RBAC, and ABAC are respected across all
    effective-dating UI patterns.

## External References

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- BambooHR market reference: https://www.bamboohr.com/
- Zoho People market reference: https://www.zoho.com/people/

References last validated: 2026-06-28.

## Approval

UX/UI Architect: Approved by Codex 2026-06-28 - Product Owner: Approved by Bhajan Lal 2026-06-28 - Accessibility Reviewer: Approved as WCAG 2.2 AA aligned 2026-06-28 - Status: Approved
