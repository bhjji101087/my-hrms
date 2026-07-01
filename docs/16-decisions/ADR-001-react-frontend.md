# ADR-001 — React + Next.js + TypeScript for the frontend

Architecture Decision Record

Date: 2026-06-14
Status: Approved

---

# Context

The HRMS needs a modern, responsive, mobile-friendly, white-label-capable frontend
usable by non-technical HR staff, managers, and employees, with strong component
reuse and accessibility (WCAG).

# Decision

Use **React with Next.js and TypeScript**, Material UI as the component library,
TanStack Query for server state, React Hook Form + Zod for forms.

# Alternatives Considered

- Angular — heavier, steeper learning curve for the team.
- Vue — smaller enterprise/component ecosystem for our needs.
- Blazor — keeps one language but weaker UI ecosystem and talent pool.

# Consequences

Positive: large talent pool, rich MUI ecosystem, SSR/routing from Next.js, strong typing.
Negative: more frontend/backend separation to manage.
Risks: framework churn; mitigated by sticking to stable, well-supported libraries.

# Impact

Architecture: API-first separation. Database: none. Security: SPA auth (JWT) patterns.
Performance: code splitting / lazy loading required. Development: TypeScript discipline.

# Approval

Solution Architect: Approved · Project Manager: Approved · Product Owner: Approved
