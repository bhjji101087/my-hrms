# Expert Assessment - ARCH-REVIEW-001 Platform Architecture

Document Owner: Codex Architecture Review
Created Date: 2026-06-17
Status: Superseded by correction pass

## Review Decision

ARCH-REVIEW-001 was architecturally strong and directionally correct, but it was not
approval-ready at the time of this review. A correction pass on 2026-06-17 updated the
foundation-group language and ADR tracker. Remaining approval still depends on Solution
Architect review plus DB, security, provider-abstraction, and ADR alignment.

## Correction Status

Resolved in ARCH-REVIEW-001 v1.1:

- Phase 7A now uses the full foundation group, not the older limited-foundation wording.
- ADR status tracker now separates Approved, Proposed, and Not Started decisions.
- AI wording now points to multi-provider LLM/RAG architecture instead of one hardcoded
  model direction.

Still needs Phase 3 review:

- Provider abstraction must be formally accepted through ARCH-REVIEW-002 and ADR-027.
- Tenant isolation traceability must be validated against ADR-006 and DB/security docs.
- Foundational DB and security documents remain Draft.

## Findings

### P1 - ADR status section was stale

Source: `docs/05-architecture/ARCH-REVIEW-001-platform-architecture-review.md` lines
489-506.

Original finding: the document said only ADR-001 to ADR-004 existed and listed ADR-005,
ADR-007, ADR-010, and ADR-011 as "to author". In project memory these were already
approved, while ADR-006, ADR-008, ADR-009, ADR-019, and ADR-027 remained proposed.

Correction status: resolved in ARCH-REVIEW-001 v1.1 by adding a current ADR tracker:
Approved, Proposed, and Still to Author / Confirm.

### P1 - Phase 7A recommendation was outdated

Source: `docs/05-architecture/ARCH-REVIEW-001-platform-architecture-review.md` lines
521-548.

Original finding: the document treated Rule Engine, effective dating, and Tenant
Catalog/RLS as pending roadmap moves. This had already happened in the approved PRD and
roadmap.

Correction status: resolved in ARCH-REVIEW-001 v1.1 by replacing the old three-item
wording with the full Phase 7A foundation group.

### P1 - Provider abstraction is not integrated into the main architecture baseline

Source: `docs/05-architecture/ARCH-REVIEW-001-platform-architecture-review.md` lines
391-396.

Provider adapters are mentioned, but the document does not treat
ARCH-REVIEW-002 and ADR-027 as Phase 3 gate inputs. Given the approved strategy of
future modules and providers being added without core changes, provider abstraction is
part of the core architecture baseline, not a side note.

Required fix: add ARCH-REVIEW-002 and ADR-027 as required Phase 3 inputs, and show how
storage, messaging, notification, identity, search, BI, and LLM providers are selected
per tenant.

### P1 - Tenant isolation design needs explicit implementation traceability

Source: `docs/05-architecture/ARCH-REVIEW-001-platform-architecture-review.md` lines
275-284.

The recommendation for TenantId, EF global filters, SQL Server RLS, tenant context
resolver, and shard/catalog map is correct. However, before approval the architecture
document should link this to ADR-006 and DB-DESIGN-TENANT-001, including how SQL Server
SESSION_CONTEXT is set and tested.

Required fix: add a traceability table from FR-015 to ADR-005, ADR-006,
DB-DESIGN-TENANT-001, SECURITY tests, and OpenAPI tenant behavior.

### P2 - AI architecture wording conflicts with model-switchable strategy

Source: `docs/05-architecture/ARCH-REVIEW-001-platform-architecture-review.md` line 506.

Original finding: ADR-019 was worded as if one LLM model family was the architecture
choice. The approved direction is model-switchable and admin-controlled: Claude, OpenAI,
Gemini, or future providers through a provider abstraction.

Correction status: resolved in ARCH-REVIEW-001 v1.1 by replacing hardcoded model wording
with multi-provider LLM/RAG architecture wording.

### P2 - Database and security gate dependencies are still Draft

Source:

- `docs/06-database/DB-DESIGN-001-foundations.md` status is Draft.
- `docs/12-security/SEC-DESIGN-001-threat-model.md` status is Draft.

ARCH-REVIEW-001 cannot be treated as a complete Phase 3 approval package until the
foundational database design and security/threat model are refreshed and aligned with
the approved PRD/roadmap.

Required fix: coordinate Solution Architect, Database Architect, and Security Architect
before owner approval.

## What Is Strong

- Workflow Studio is correctly treated as a reusable platform service, not a leave-only
  workflow feature.
- Rule Engine is correctly rules-as-data, versioned, effective-dated, and sandboxed.
- Hybrid pooled tenancy with TenantId plus SQL Server RLS is the right direction.
- Running workflow instances pin definition versions, which protects customers from
  silent regression.
- The open/closed module ingestion contract is strong and matches the approved product
  strategy.

## Recommendation

Do not approve ARCH-REVIEW-001 yet. Ask the Solution Architect to refresh it to version
1.1 and include:

- Current approved PRD and roadmap baseline.
- Current ADR status tracker.
- Provider-abstraction baseline from ARCH-REVIEW-002 and ADR-027.
- FR-to-architecture traceability for FR-015, FR-002, FR-014, FR-013, FR-007, FR-009,
  and FR-006.
- Links to database, security, integration, and OpenAPI follow-up documents.

After these updates, the document should be suitable for owner review and approval.

---

## 2026-06-29 Resolution Note

This expert assessment is retained as a historical reference. Its unresolved architecture
recommendations have been converted into the approved architecture baseline and/or tracked
through the Phase 7A hardening backlog:

- `docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`
- `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`
- `docs/06-database/DB-DESIGN-PHASE-7A-STD-001-data-classification-migration.md`
- `docs/07-ui-ux/UI-PHASE-7A-STD-001-accessibility-states.md`
- `docs/10-testing/TEST-PHASE-7A-STD-001-traceability-abuse.md`
