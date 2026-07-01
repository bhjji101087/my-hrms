# Enterprise HRMS Platform

A configurable, multi-tenant, multi-country, white-label enterprise Human Resource
Management System (HRMS).

> **Status:** Phase 7A development starting. All Phase 7A architecture, design, database,
> UI, and test documentation is **Approved**. This repository holds the approved
> documentation and (from Phase 7A onward) the application source code.

## Platform pillars

- Multi-tenant with strict tenant isolation (SQL Server Row-Level Security)
- Multi-country, multi-language, white-label ready
- Dynamic workflows, forms, rules, and reports (configuration, not code)
- Extension / plugin based customization — core is never modified per customer
- RBAC + ABAC + full audit on every module
- Event-driven, API-first, AI-ready

## Architecture

**Enterprise Modular Monolith with microservice-ready boundaries** (see
[ADR-004](docs/16-decisions/ADR-004-modular-monolith.md)):

- One deployable application, one primary SQL Server database
- Schema-per-module (`catalog`, `security`, `hr`, `leave`, `attendance`, `payroll`, …)
- Modules communicate via published contracts and domain events — no cross-schema reach-in
- Any module (e.g. Payroll, Attendance) can later be extracted into a microservice

### Technology

| Layer | Choice |
|---|---|
| Frontend | React, Next.js, TypeScript |
| Backend | .NET (primary), Node.js (specialized real-time / connector services) |
| Database | SQL Server |
| Cache | Redis |
| Search | Elasticsearch |
| Vector store | Qdrant (self-hosted first) |
| Messaging | RabbitMQ (self-hosted first) / Azure Service Bus (optional later) |
| CI/CD | GitHub Actions |

## Local development

Infrastructure runs in Docker; the .NET API runs from Visual Studio (F5) against the
containers.

```bash
docker compose up -d      # starts SQL Server, RabbitMQ, Redis, Qdrant
# then open the solution in Visual Studio and run the API
```

> `docker-compose.yml` and the .NET solution are added in the S0 scaffold.

## Documentation

All design documentation lives under [`docs/`](docs/). The project operating contract is
[CLAUDE.md](CLAUDE.md); project memory/state is in [.ai/PROJECT_STATE.md](.ai/PROJECT_STATE.md).

| Area | Folder |
|---|---|
| Architecture & ADRs | `docs/05-architecture`, `docs/16-decisions` |
| Database designs | `docs/06-database` |
| API specs / OpenAPI | `docs/08-api-specs` |
| Feature requirements | `docs/02-product-requirements` |
| UI / UX | `docs/07-ui-ux` |
| Test plans | `docs/10-testing` |
| Standards | `docs/20-standards` |

## Contributing

- No direct commits to `main` — all changes via Pull Request with review (see
  [CONTRIBUTING.md](CONTRIBUTING.md)).
- Every feature requires its five approved documents before implementation
  (Business, Technical, Database, UI, Test).
