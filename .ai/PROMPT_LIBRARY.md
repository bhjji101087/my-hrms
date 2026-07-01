# PROMPT_LIBRARY.md — Index (not source of truth)

> **Source of truth for agent prompts is now `.claude/agents/*.md`.**
> Those files are what Claude actually executes. This file is only a human-readable
> index so prompts do not drift across two places. To change how an agent behaves,
> edit its file under `.claude/agents/`, not here.

## Cross-cutting rules (apply to all agents)

These live in the root `CLAUDE.md` (the constitution) and are inherited by every
session and agent:
1. Read existing approved documents first. 2. Follow architecture, coding, security,
and testing standards. 3. Document assumptions. 4. Never skip documentation.
5. Update `.ai/PROJECT_STATE.md` as the final step of every task.

## Agent roster → prompt files

| Agent | Persona | Prompt file |
|---|---|---|
| 1 HR Domain Expert | Senior HR director (20+ yrs) | `.claude/agents/hr-domain-expert.md` |
| 2 Product Owner | SaaS Product Owner | `.claude/agents/product-owner.md` |
| 6 Solution Architect | Principal architect | `.claude/agents/solution-architect.md` |
| 7 Database Architect | Senior SQL Server architect | `.claude/agents/database-architect.md` |
| 9 Security Architect | Security architect (OWASP) | `.claude/agents/security-architect.md` |
| 13 .NET Architect | Senior backend architect | `.claude/agents/dotnet-architect.md` |
| 21 QA Architect | Test architect | `.claude/agents/qa-architect.md` |
| 24 Documentation Engineer | Docs/formatting | `.claude/agents/documentation-engineer.md` |

Remaining agents (3, 4, 5, 8, 10–12, 14–20, 22, 23, 25) are described in
`.ai/AGENTS.md` and will get their own `.claude/agents/*.md` file when first needed.
