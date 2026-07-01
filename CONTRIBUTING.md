# Contributing

## Golden rules (from the project constitution — see [CLAUDE.md](CLAUDE.md))

1. **No code before approved documentation.** Every feature needs five approved documents:
   Business Requirements, Technical Design, Database Design, UI Design, Test Cases.
2. **No hardcoded business rules** — everything configurable (rules engine / config-as-data).
3. **Customer customization never touches core** — configuration, feature flags, extensions,
   plugins only.
4. **RBAC + ABAC + Audit on every module.**
5. **Every API is versioned, documented (OpenAPI), and tested.**
6. **Event-driven where possible.**
7. **Tenant isolation** — every table has `TenantId`; every query is tenant-filtered.
8. **SOLID / DRY / KISS / YAGNI / Clean Architecture / DDD.**
9. **Test coverage ≥ 85%.**

## Branching & PRs

See the canonical rules in
[`docs/20-standards/BRANCHING_AND_COMMIT_RULES.md`](docs/20-standards/BRANCHING_AND_COMMIT_RULES.md).
Summary:

- `main` is protected. **No direct commits to `main`.** It receives merges only from
  `development` via PR, **after each Feature is completed**.
- All work branches off **`development`**, one branch per User Story.
- Branch naming: `feat/dev-bl-<issue#>-<us_description>` — issue number un-padded,
  description lowercase with words separated by `_`
  (e.g. `feat/dev-bl-15-tenant_resolver_from_jwt_host`).
- **One commit = one User Story** — US branches are **squash-merged** into `development`.
- Open a Pull Request into `development`; it must pass CI (build + tests + architecture
  tests) and receive the required approval before merge. Reference the story
  (`Closes #<issue#>`).
- A story's tasks are ticked **only after** its PR is merged into `development`.

## Module boundaries (Modular Monolith)

- Each module owns its own schema. **No cross-schema JOINs across module boundaries.**
- A module reads another module's data only via its published contract or a domain event.
- Module-to-module calls go through public interfaces, never internal classes.
- The `HRMS.ArchitectureTests` project enforces these rules; a violation fails CI.

## Definition of Done (every story)

- [ ] Tenant-filtered + RLS enforced
- [ ] RBAC + ABAC checks
- [ ] Audit records written
- [ ] Effective-dated where applicable
- [ ] Events published via the outbox
- [ ] OpenAPI updated
- [ ] Unit + integration tests, coverage ≥ 85%
- [ ] Architecture tests green
- [ ] `.ai/PROJECT_STATE.md` change log updated
