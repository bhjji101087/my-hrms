# Branching, Commit & PR Rules

Status: Approved (owner Bhajan Lal, 2026-07-01)

These rules are **mandatory** for all Phase 7A (and later) development. AI agents and
humans must follow them without being reminded.

---

## 1. Branch model

- `main` — protected, release-quality. No direct commits. Only receives merges from
  `development` via PR.
- `development` — long-lived integration branch, cut from `main`. All User Story branches
  are created **from `development`** and merged **back into `development`**.
- **User Story branches** — one branch per GitHub User Story issue, cut from `development`.

```
main
 └── development
      ├── feat/dev-bl-15-tenant_resolver_from_jwt_host
      ├── feat/dev-bl-16-itenantcontext_middleware
      └── ...
```

## 2. Branch naming (exact format)

```
feat/dev-bl-<issue#>-<us_description>
```

Rules:
- `<issue#>` = the GitHub **issue number of the User Story**, used **as assigned, with no
  zero-padding** (e.g. `1`, `2`, `15`, `103`).
- `<us_description>` = short description of the User Story, **all lowercase**, each word
  **separated by an underscore `_`**.
- The whole branch name is lowercase.
- Prefix is `feat/` for features. (Use `fix/` for bug branches, same rest of the format.)

Examples:
- `feat/dev-bl-3-create_hrms_sln_building_blocks`
- `feat/dev-bl-15-tenant_resolver_from_jwt_host`
- `feat/dev-bl-19-sql_rls_filter_and_block_predicates`

## 3. One commit = one User Story

- A commit (as landed on `development`) must contain the work of **exactly one User
  Story** — never 2 or 3 US together.
- This is enforced by **squash-merging** each US branch into `development`: the branch may
  have multiple work-in-progress commits, but the merge collapses them into **one commit**
  for that US. The repository is configured to allow **squash merge only**.
- The squash commit message references the US issue (e.g. `Closes #15`).

## 4. Task / US completion rule

For each User Story:
- The story's **Tasks** are marked done **only after**:
  1. the code is committed,
  2. a PR is raised for that US, and
  3. the PR is **merged into `development`**.
- Tasks and the User Story are **linked to the PR** for that US (PR references the issue
  with `Closes #<US#>`; merging closes the issue and its task checklist is completed).
- Do not tick task checkboxes before the PR is merged.

## 5. Pull Request rules

- Every US branch → PR into `development`.
- PR title references the US: include `Closes #<issue#>`.
- PR must pass CI (build + tests + architecture-boundary tests) and get the required
  approval before merge (see repo branch protection).
- One PR corresponds to one User Story.

## 6. Merge to main

- `development` is merged into `main` **after each Feature is completed** — i.e. once all
  User Stories under a Feature are merged into `development` and the Feature is done,
  `development` is promoted to `main` via PR.
- The merge to `main` is done via PR, after CI passes and the owner approves.
- (`development` may also be merged to `main` at a release/milestone checkpoint.)
