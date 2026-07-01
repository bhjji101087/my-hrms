# Technical Design - Rule Engine

Module: Platform Foundation
Phase: 7A / Sprint S3
Owner: Solution Architect (Agent 6)
Created Date: 2026-06-28
Version: 1.0
Status: Approved
> Doc 2 of 5 for Rule Engine. Implements FEAT-RULE-ENGINE-001 and ADR-011.

## Architecture

The Rule Engine provides a safe deterministic evaluation service. It supports expression
rules, decision tables, and composed rule sets. CEL-style safe expressions are preferred
for simple predicates and formulas; DMN-style decision tables guide business-readable
decision logic.

```text
Module -> Rule Evaluation API -> Rule Resolver -> Validator -> Evaluator -> Explanation
                         |             |             |
                         |             +-> Effective Version
                         +-> Audit/Event/Telemetry
```

## Components

- Rule Registry: stores rule set metadata, ownership, module usage, and classification.
- Rule Authoring Model: draft, validate, simulate, approve, publish, deprecate.
- Expression Validator: type checks, blocks unsafe functions, enforces complexity limits.
- Decision Table Evaluator: evaluates rows with hit policy and explainable path.
- Context Provider: supplies approved module data snapshots, never arbitrary DB access.
- Explanation Service: returns matched rules, outputs, version, and input summary.
- Runtime Cache: caches published rule definitions with tenant and version partitioning.

## Rule Lifecycle

Draft -> Validated -> Review -> Approved -> Published -> Deprecated -> Retired.
Published versions are immutable. New changes create a new effective-dated version.

## API Requirements

Administrative APIs cover rule set create/update, validate, simulate, submit for approval,
publish, rollback, and history. Runtime APIs are internal and used by modules with tenant
context and correlation ID. OpenAPI shall document admin APIs.

## Security

Rules cannot execute arbitrary code, file access, network access, reflection, SQL, or
provider calls. Context data is explicitly shaped by module adapters. Rule authoring and
publishing are permission-protected and audited.

## Observability

Metrics include evaluation count, latency, failure rate, cache hit rate, simulation count,
publish count, and timeout count. Evaluation logs store rule IDs/versions and decision
summary, not unnecessary PII.

## Extension Points

Modules register rule context schemas, allowed functions, output contracts, and validation
policies through metadata. Adding new modules does not require modifying the core evaluator.

## Acceptance Criteria

1. Rule Engine evaluates leave, workflow, attendance, and payroll rule sets through shared APIs.
2. Published rule versions are immutable and effective-dated.
3. Rule simulation works with sample contexts and explainable output.
4. Unsafe expressions are blocked by validation.
5. Rule evaluation evidence is available for audit and payroll reconciliation.

## External References

- CEL: https://cel.dev/
- OMG DMN: https://www.omg.org/spec/DMN/
- JSON Schema: https://json-schema.org/

References last validated: 2026-06-28.

## Phase 7A Hardening Addendum

This technical design must comply with `docs/09-development/PHASE-7A-STD-001-api-event-nfr-runbooks.md`.
Module-specific recommendations are tracked in
`docs/21-product-backlog/PHASE-7A-HARDENING-BACKLOG-001-review-recommendations.md`.

## Approval

Solution Architect: ____ - .NET Architect: ____ - Security Architect: ____ - Status: Approved
