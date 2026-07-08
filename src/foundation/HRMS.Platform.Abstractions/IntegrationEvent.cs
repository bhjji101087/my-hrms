namespace HRMS.Platform.Abstractions;

/// <summary>
/// Base type for integration events published across module boundaries via the event bus
/// (outbox-backed). Cross-module communication uses events, not direct calls (ADR-009).
/// </summary>
public abstract record IntegrationEvent
{
    /// <summary>Unique event identifier, used for idempotent consumption.</summary>
    public Guid EventId { get; init; } = Guid.NewGuid();

    /// <summary>UTC instant the event occurred.</summary>
    public DateTimeOffset OccurredOnUtc { get; init; } = DateTimeOffset.UtcNow;

    /// <summary>Tenant the event belongs to. Event routing is tenant-scoped.</summary>
    public Guid TenantId { get; init; }
}
