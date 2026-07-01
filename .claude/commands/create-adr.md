---
description: Record an Architecture Decision Record for a decision/fork. Usage: /create-adr <decision title>
argument-hint: <decision title>
---

Decision to record: $ARGUMENTS

Dispatch the `solution-architect` agent to author an ADR.

Requirements:
1. Read existing ADRs in `docs/16-decisions/` to find the next free `ADR-XXX` number
   and to avoid contradicting an approved decision.
2. Use `docs/19-templates/ARCHITECTURE_DECISION_TEMPLATE.md`. Fill: context, decision,
   alternatives considered, consequences (positive/negative/risks), impact, approval.
3. Save as `docs/16-decisions/ADR-XXX-<kebab-title>.md` with `Status: Proposed`.
4. Update `.ai/PROJECT_STATE.md` (Change Log; add to Approved Documents only once the
   human approves it).
5. Report the file path and remind the human to approve (Proposed → Approved).
