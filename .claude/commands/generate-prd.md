---
description: Draft a Product Requirements Document for a module/feature using the PRD template. Usage: /generate-prd <module or feature name>
argument-hint: <module or feature name>
---

Target for this PRD: $ARGUMENTS

Dispatch the `product-owner` agent to draft a PRD for the target above.

Requirements:
1. Read `.ai/PROJECT_STATE.md` and any approved market research / gap analysis first.
2. Use `docs/19-templates/PRODUCT_REQUIREMENTS_TEMPLATE.md` and fill EVERY section:
   business objective, value, stakeholders, personas, functional requirements
   (FR-XXX with acceptance criteria), non-functional requirements, dependencies,
   risks, success metrics, approval.
3. Save to `docs/02-product-requirements/` with a clear filename and `Status: Draft`.
4. Update `.ai/PROJECT_STATE.md` (Change Log + Pending Documents).
5. Report the file path and remind the human to review and approve.
