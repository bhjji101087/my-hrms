namespace HRMS.Platform.Abstractions;

/// <summary>
/// Immutable, request-scoped tenant context. Established by tenant resolution middleware
/// before any application service runs; data access is blocked unless it is present.
/// See docs/09-development/TECH-TENANT-001-technical-design.md §3–§5.
/// </summary>
public interface ITenantContext
{
    /// <summary>Resolved tenant identifier for the current request/scope.</summary>
    Guid TenantId { get; }

    /// <summary>Human-readable tenant code.</summary>
    string TenantCode { get; }

    /// <summary>True when a valid tenant context has been resolved and applied.</summary>
    bool IsResolved { get; }
}
