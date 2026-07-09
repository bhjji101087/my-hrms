# Source Review - src Folder Line-by-Line Walkthrough

Document ID: SRC-REVIEW-001

Date: 2026-07-02

Owner / Agent: Codex Source Review

Status: Review

Scope: All tracked source and configuration files under `src/`, plus generated local
artifacts physically present under `src/`.

Verification: `dotnet build HRMS.sln -m:1 -nr:false --no-incremental` succeeded from
`src/` with 0 warnings and 0 errors on 2026-07-02.

---

## 1. Executive Summary

The current `src/` folder is not a full HRMS application yet. It is the first foundation
for the approved Phase 7A modular monolith:

- `HRMS.SharedKernel` contains framework-independent domain primitives.
- `HRMS.Platform.Abstractions` contains cross-cutting contracts that modules can depend on.
- `HRMS.Platform.Infrastructure` contains concrete implementations of platform contracts.
- No business module code exists yet for Tenant, Identity, Leave, Attendance, Payroll, or
  Reporting. Those modules are expected to be added later using the approved documents.

This source shape aligns with the approved modular monolith direction, tenant isolation
requirements in ADR-006, event-driven backbone in ADR-009, and `.NET 10` standards.

---

## 2. File Inventory

Git-tracked source/configuration files under `src/`: 16.

Generated local files under `src/`: Visual Studio `.vs/`, .NET `obj/`, and .NET `bin/`
artifacts. These are ignored by `.gitignore` and should not be treated as product source.

---

## 3. Solution and Build Files

### 3.1 `src/HRMS.sln`

Purpose: Visual Studio / .NET solution file that groups all foundation projects so they
can be restored, built, and opened together.

Where it fits: Top of the `src/` tree. It is the build entry point for the current .NET
foundation.

How it works:

| Lines | Explanation |
|---|---|
| 1-4 | Declares the file as a Visual Studio solution, including Visual Studio format and minimum supported versions. |
| 5-6 | Creates a solution folder named `foundation`. This is an organizational folder, not a compiled project. |
| 7-8 | Adds `HRMS.SharedKernel`, the lowest-level shared domain project. |
| 9-10 | Adds `HRMS.Platform.Abstractions`, the platform contract project. |
| 11-12 | Adds `HRMS.Platform.Infrastructure`, the platform implementation project. |
| 13 | Starts the global solution settings block. |
| 14-17 | Defines the supported build configurations: `Debug|Any CPU` and `Release|Any CPU`. |
| 18-31 | Maps each project GUID to Debug and Release build settings so every project participates in normal builds. |
| 32-34 | Keeps the solution node visible in Visual Studio. |
| 35-39 | Nests all three projects under the `foundation` solution folder for readability. |
| 40-42 | Stores the solution GUID used by Visual Studio tooling. |
| 43 | Ends the global solution block. |

Why it matters: It gives the platform one consistent build surface. Future modules should
be added here under their own folders while keeping foundation code separate from module
code.

### 3.2 `src/global.json`

Purpose: Pins the .NET SDK policy for this source tree.

Where it fits: `src/` root, so commands run from `src/` use the intended SDK selection.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Opens the JSON document. |
| 2 | Starts the `sdk` configuration block. |
| 3 | Requests .NET SDK `10.0.100` as the baseline SDK. |
| 4 | Allows roll-forward to the latest minor-compatible SDK when the exact SDK is not installed. |
| 5 | Ends the `sdk` block. |
| 6 | Ends the JSON document. |

Why it matters: The project standard requires .NET 10. This file reduces build drift
between developer machines and CI.

### 3.3 `src/Directory.Build.props`

Purpose: Centralizes common build settings for all .NET projects below `src/`.

Where it fits: MSBuild automatically imports this file into child projects.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Opens the MSBuild project file. |
| 2 | Blank separator for readability. |
| 3-7 | Comment explaining this is shared build configuration and references the modular monolith and .NET standards. |
| 8 | Opens a property group containing shared build properties. |
| 9 | Sets every project to target `net10.0`. |
| 10 | Uses the latest available C# language version. |
| 11 | Enables implicit common `using` directives. |
| 12 | Enables nullable reference type analysis. |
| 13 | Blank separator. |
| 14 | Comment introducing quality gate settings. |
| 15 | Treats compiler warnings as build errors. |
| 16 | Enforces code style during build. |
| 17 | Uses the latest recommended analyzer level. |
| 18 | Disables XML documentation file generation for now. |
| 19 | Blank separator. |
| 20 | Enables deterministic builds. |
| 21 | Closes the property group. |
| 22 | Blank separator. |
| 23 | Closes the MSBuild project file. |

Why it matters: This prevents each project from drifting into different target frameworks,
nullability settings, and quality rules.

---

## 4. Shared Kernel Project

### 4.1 `src/foundation/HRMS.SharedKernel/HRMS.SharedKernel.csproj`

Purpose: Defines the `HRMS.SharedKernel` project.

Where it fits: Lowest-level foundation library. It should stay free of EF Core, ASP.NET,
infrastructure, and business-module dependencies.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Declares this as an SDK-style .NET project. |
| 2 | Blank separator. |
| 3-6 | Comment states the architectural rule: shared domain primitives only, no infrastructure or module dependency. |
| 7 | Opens the project property group. |
| 8 | Sets the root C# namespace to `HRMS.SharedKernel`. |
| 9 | Sets the compiled assembly name to `HRMS.SharedKernel`. |
| 10 | Closes the property group. |
| 11 | Blank separator. |
| 12 | Closes the project file. |

Why it matters: This is the safest place for universal concepts like `Entity`, `Result`,
tenant-scoped markers, soft delete markers, and effective-dated markers.

### 4.2 `src/foundation/HRMS.SharedKernel/Entity.cs`

Purpose: Base class for domain entities that have a strongly typed identity.

Where it fits: Domain model foundation. Future entities can inherit this to get consistent
identity equality.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the class in the `HRMS.SharedKernel` namespace. |
| 2 | Blank separator. |
| 3-5 | XML summary explains the class purpose for documentation and IntelliSense. |
| 6 | Declares an abstract generic entity class named `Entity<TId>`. |
| 7 | Requires `TId` to be non-null, preventing nullable identifiers. |
| 8 | Opens the class body. |
| 9 | Defines `Id` with public read access and protected write access. Derived entities can set it; outside callers cannot freely mutate it. |
| 10 | Blank separator. |
| 11-12 | Overrides equality: two entities are equal only when they are the same runtime type and have the same `Id`. |
| 13 | Blank separator. |
| 14 | Builds a hash code from runtime type plus `Id`, matching the equality rule. |
| 15 | Closes the class. |

Why it matters: This supports DDD-style entity identity and avoids comparing entities by
every property.

Review note: Future implementation should be careful with new unsaved entities that still
have default identifiers; two default IDs of the same type can compare equal unless
constructors assign IDs early.

### 4.3 `src/foundation/HRMS.SharedKernel/Result.cs`

Purpose: Lightweight success/failure return type for operations where failure is expected
and should not always be represented by exceptions.

Where it fits: Shared domain/application primitive.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the file in `HRMS.SharedKernel`. |
| 2 | Blank separator. |
| 3-5 | XML summary describes the result pattern. |
| 6 | Declares the non-generic `Result` class. |
| 7 | Opens the class body. |
| 8-9 | Defines a protected constructor accepting success state and optional error. Only this class and derived classes can create raw results. |
| 10-11 | Rejects invalid state: success cannot contain an error. |
| 12-13 | Rejects invalid state: failure must contain an error. |
| 14 | Blank separator. |
| 15 | Stores whether the result succeeded. |
| 16 | Stores the error, if any. |
| 17 | Closes the constructor. |
| 18 | Blank separator. |
| 19 | Exposes success state. |
| 20 | Exposes failure state as the inverse of success. |
| 21 | Exposes the error object when failure occurs. |
| 22 | Blank separator. |
| 23 | Factory method for successful operations without a return value. |
| 24 | Factory method for failed operations without a return value. |
| 25 | Blank separator. |
| 26 | Factory method for successful operations with a value. |
| 27 | Factory method for failed operations with a value type. |
| 28 | Closes the `Result` class. |
| 29 | Blank separator. |
| 30 | XML summary for generic result. |
| 31 | Declares sealed `Result<TValue>` so behavior cannot be changed through inheritance. |
| 32 | Opens the generic result class. |
| 33 | Stores the success value internally and allows null before success validation. |
| 34 | Blank separator. |
| 35-36 | Internal constructor passes success/failure information to the base class and stores the value. |
| 37 | Blank separator. |
| 38-40 | Exposes `Value` only when successful; throws if caller tries to read a failed result's value. |
| 41 | Closes `Result<TValue>`. |
| 42 | Blank separator. |
| 43 | XML summary for machine-readable errors. |
| 44 | Defines an immutable `ResultError` record with `Code` and `Message`. |
| 45 | Opens the record body. |
| 46 | Provides a reusable empty error object. |
| 47 | Closes the record. |

Why it matters: It gives services a consistent way to return validation/business failures
without hardcoding UI behavior or throwing exceptions for normal business outcomes.

### 4.4 `src/foundation/HRMS.SharedKernel/ITenantScopedEntity.cs`

Purpose: Marker interface for entities that belong to exactly one tenant.

Where it fits: Shared domain contract used by EF global filters and SQL Server RLS
patterns described in ADR-006 and `TECH-TENANT-001`.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the interface in `HRMS.SharedKernel`. |
| 2 | Blank separator. |
| 3-7 | XML summary explains tenant isolation intent and references the tenant technical design. |
| 8 | Declares the `ITenantScopedEntity` interface. |
| 9 | Opens the interface body. |
| 10 | Requires a `TenantId` property on tenant-scoped entities. |
| 11 | Closes the interface. |

Why it matters: Tenant isolation is a golden rule. This marker gives infrastructure a
standard way to detect tenant-scoped entities and apply query/write rules.

### 4.5 `src/foundation/HRMS.SharedKernel/ISoftDeletable.cs`

Purpose: Marker interface for entities that are logically deleted rather than physically
removed.

Where it fits: Shared domain contract used by query filters and audit-safe data handling.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the interface in `HRMS.SharedKernel`. |
| 2 | Blank separator. |
| 3-6 | XML summary explains soft delete use with tenant filtering. |
| 7 | Declares the `ISoftDeletable` interface. |
| 8 | Opens the interface body. |
| 9 | Requires an `IsDeleted` property. |
| 10 | Closes the interface. |

Why it matters: HRMS data often needs audit/history retention. Soft delete supports hiding
inactive records from normal screens while preserving data for audit, retention, or
recovery workflows.

### 4.6 `src/foundation/HRMS.SharedKernel/IEffectiveDated.cs`

Purpose: Marker interface for records that are valid during a business date range.

Where it fits: Shared contract for the approved effective dating/bitemporal foundation.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the interface in `HRMS.SharedKernel`. |
| 2 | Blank separator. |
| 3-7 | XML summary explains open-ended records and references the approved effective dating design. |
| 8 | Declares the `IEffectiveDated` interface. |
| 9 | Opens the interface body. |
| 10 | XML summary for the valid-time start date. |
| 11 | Requires `EffectiveFrom` as a tenant-local `DateOnly`. |
| 12 | Blank separator. |
| 13 | XML summary for the valid-time end date. |
| 14 | Requires nullable `EffectiveTo`; null means currently open-ended. |
| 15 | Closes the interface. |

Why it matters: HR data changes over time. Salary, assignment, branch, shift, policy, and
role records often need "what was true on this date" behavior.

---

## 5. Platform Abstractions Project

### 5.1 `src/foundation/HRMS.Platform.Abstractions/HRMS.Platform.Abstractions.csproj`

Purpose: Defines the project that contains cross-cutting platform interfaces.

Where it fits: Above `SharedKernel`, below concrete infrastructure and business modules.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Declares this as an SDK-style .NET project. |
| 2 | Blank separator. |
| 3-7 | Comment explains the project purpose: contracts for tenant context, event bus, clock, and future provider seams. |
| 8 | Opens the property group. |
| 9 | Sets root namespace to `HRMS.Platform.Abstractions`. |
| 10 | Sets assembly name to `HRMS.Platform.Abstractions`. |
| 11 | Closes the property group. |
| 12 | Blank separator. |
| 13 | Opens an item group for project references. |
| 14 | References `HRMS.SharedKernel`, allowing abstractions to reuse shared primitives. |
| 15 | Closes the item group. |
| 16 | Blank separator. |
| 17 | Closes the project file. |

Why it matters: Modules should depend on stable abstractions instead of concrete
infrastructure. This keeps the modular monolith easier to test and easier to split later.

### 5.2 `src/foundation/HRMS.Platform.Abstractions/ITenantContext.cs`

Purpose: Defines the request-scoped tenant context contract.

Where it fits: Tenant resolution, data access, authorization, logging, audit, and events
will depend on this contract.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the interface in `HRMS.Platform.Abstractions`. |
| 2 | Blank separator. |
| 3-7 | XML summary explains that tenant context must be resolved before application services run. |
| 8 | Declares the `ITenantContext` interface. |
| 9 | Opens the interface body. |
| 10 | XML summary for the tenant GUID. |
| 11 | Requires resolved `TenantId`. |
| 12 | Blank separator. |
| 13 | XML summary for readable tenant code. |
| 14 | Requires `TenantCode`. |
| 15 | Blank separator. |
| 16 | XML summary for resolution state. |
| 17 | Requires `IsResolved`, allowing fail-closed checks. |
| 18 | Closes the interface. |

Why it matters: All tenant-scoped work must know which tenant is active. ADR-006 says no
tenant context means the request must fail closed.

Review note: ADR-006 also mentions region, shard, and entitlements. Those can be added
later as the tenant catalog implementation grows.

### 5.3 `src/foundation/HRMS.Platform.Abstractions/IntegrationEvent.cs`

Purpose: Base type for events published across module boundaries.

Where it fits: Event-driven architecture foundation required by ADR-009.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the record in `HRMS.Platform.Abstractions`. |
| 2 | Blank separator. |
| 3-6 | XML summary states that cross-module communication should use outbox-backed events. |
| 7 | Declares abstract record `IntegrationEvent`. Records are useful for immutable event data. |
| 8 | Opens the record body. |
| 9 | XML summary for event identity. |
| 10 | Initializes `EventId` with a new GUID for idempotent processing. |
| 11 | Blank separator. |
| 12 | XML summary for event timestamp. |
| 13 | Initializes `OccurredOnUtc` to the current UTC instant. |
| 14 | Blank separator. |
| 15 | XML summary for tenant ownership. |
| 16 | Requires/holds `TenantId` so events remain tenant-scoped. |
| 17 | Closes the record. |

Why it matters: Events are how future modules such as Attendance, Payroll, Notifications,
Reports, Audit, and AI can react without tight direct coupling.

### 5.4 `src/foundation/HRMS.Platform.Abstractions/IEventBus.cs`

Purpose: Defines the contract for publishing integration events.

Where it fits: Application services can publish through this interface; infrastructure can
later provide RabbitMQ, Azure Service Bus, or in-memory/outbox implementations.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the interface in `HRMS.Platform.Abstractions`. |
| 2 | Blank separator. |
| 3-7 | XML summary explains the outbox-backed event bus and provider-swappable seam. |
| 8 | Declares the `IEventBus` interface. |
| 9 | Opens the interface body. |
| 10 | Defines async `PublishAsync` with an event and optional cancellation token. |
| 11 | Restricts `TEvent` so only `IntegrationEvent` subclasses can be published. |
| 12 | Closes the interface. |

Why it matters: The platform can enforce event-driven communication without coupling
module code to a specific broker library.

Review note: The comment currently names RabbitMQ, while ADR-009 also identifies Azure
Service Bus as the cloud broker and RabbitMQ as the portable/self-hosted option. The code
contract is fine; the comment can be broadened when broker implementation begins.

### 5.5 `src/foundation/HRMS.Platform.Abstractions/IClock.cs`

Purpose: Defines a testable abstraction over the current time.

Where it fits: Effective dating, audit timestamps, event timestamps, token/session logic,
and tests should use this instead of directly calling system time.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Places the interface in `HRMS.Platform.Abstractions`. |
| 2 | Blank separator. |
| 3-7 | XML summary explains UTC consistency and testability. |
| 8 | Declares the `IClock` interface. |
| 9 | Opens the interface body. |
| 10 | XML summary for current UTC time. |
| 11 | Requires a `UtcNow` property. |
| 12 | Closes the interface. |

Why it matters: Time-dependent HR logic is hard to test if every class reads the machine
clock directly. This interface lets tests provide fixed time.

---

## 6. Platform Infrastructure Project

### 6.1 `src/foundation/HRMS.Platform.Infrastructure/HRMS.Platform.Infrastructure.csproj`

Purpose: Defines the project for shared infrastructure implementations.

Where it fits: Edge of the foundation layer. It implements contracts from
`HRMS.Platform.Abstractions`.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Declares this as an SDK-style .NET project. |
| 2 | Blank separator. |
| 3-8 | Comment explains this project will hold implementations such as clock, EF base context, tenant interceptors, outbox, and adapters. |
| 9 | Opens the property group. |
| 10 | Sets root namespace to `HRMS.Platform.Infrastructure`. |
| 11 | Sets assembly name to `HRMS.Platform.Infrastructure`. |
| 12 | Closes the property group. |
| 13 | Blank separator. |
| 14 | Opens project references. |
| 15 | References `HRMS.SharedKernel`. |
| 16 | References `HRMS.Platform.Abstractions`. |
| 17 | Closes project references. |
| 18 | Blank separator. |
| 19 | Closes the project file. |

Why it matters: Concrete technology choices live here, not in domain modules. This keeps
business logic testable and provider-swappable.

### 6.2 `src/foundation/HRMS.Platform.Infrastructure/SystemClock.cs`

Purpose: Real implementation of `IClock` using the machine's UTC clock.

Where it fits: Infrastructure implementation registered by the application host later.

How it works:

| Lines | Explanation |
|---|---|
| 1 | Imports `HRMS.Platform.Abstractions` so the class can implement `IClock`. |
| 2 | Blank separator. |
| 3 | Places the implementation in `HRMS.Platform.Infrastructure`. |
| 4 | Blank separator. |
| 5-7 | XML summary explains this is the default real UTC clock. |
| 8 | Declares sealed `SystemClock` implementing `IClock`. |
| 9 | Opens the class body. |
| 10 | Returns `DateTimeOffset.UtcNow` whenever current UTC time is requested. |
| 11 | Closes the class. |

Why it matters: Production code gets real time, while tests can use a fake clock through
the same `IClock` contract.

---

## 7. Generated Local Files Under `src/`

These files are physically present after opening/building the solution but are not source
files:

| Path pattern | Purpose | Should developers edit it? |
|---|---|---|
| `src/.vs/**` | Visual Studio workspace state, file indexes, design-time build cache, solution user options. | No. Local editor cache only. |
| `src/**/obj/**` | .NET intermediate build and restore files such as generated assembly info, generated global usings, NuGet restore assets, and build caches. | No. Regenerated by restore/build. |
| `src/**/bin/**` | Compiled output such as DLLs, PDBs, and dependency files. | No. Regenerated by build. |

Why no line-by-line explanation for these: many are binary/cache/generated files, and
their line content is not stable product logic. The correct review action is to confirm
they are ignored and not treated as design authority.

---

## 8. Overall Review Notes

- The current source is a clean first foundation, not a feature-complete system.
- It supports the approved direction: modular monolith first, future service extraction
  through abstractions and events.
- Tenant isolation is represented by `ITenantScopedEntity` and `ITenantContext`, but the
  full middleware, EF filters, SQL Server RLS, and tenant catalog implementation still
  need to be built.
- Event-driven behavior is represented by `IntegrationEvent` and `IEventBus`, but the
  outbox, dispatcher, broker adapter, retry, DLQ, and idempotent consumer store still need
  to be built.
- Effective dating is represented by `IEffectiveDated`, but validation, overlap checks,
  as-of query behavior, and temporal history behavior still need implementation.
- The solution builds successfully when run sequentially.

---

## 9. Recommended Next Development Additions

1. Add test projects for `SharedKernel`, `Platform.Abstractions`, and
   `Platform.Infrastructure`.
2. Add a fake/test clock for deterministic tests.
3. Start Tenant Catalog + RLS implementation only against the approved five-document set.
4. Add EF Core base context and tenant query-filter infrastructure before any tenant data
   entity is introduced.
5. Add event outbox contracts and dispatcher infrastructure before business modules publish
   cross-module events.

---

## 10. References

- `.ai/ARCHITECTURE_PRINCIPLES.md`
- `docs/20-standards/CODING_STANDARDS_DOTNET.md`
- `docs/16-decisions/ADR-006-tenant-context-data-access.md`
- `docs/16-decisions/ADR-009-event-driven-backbone.md`
- `docs/09-development/TECH-TENANT-001-technical-design.md`
- `docs/09-development/TECH-EVENT-BUS-001-technical-design.md`
- `docs/09-development/TECH-EFFECTIVE-DATING-001-technical-design.md`

