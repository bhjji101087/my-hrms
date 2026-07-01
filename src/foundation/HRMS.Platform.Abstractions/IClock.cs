namespace HRMS.Platform.Abstractions;

/// <summary>
/// Abstraction over the system clock so time-dependent logic (effective dating, audit
/// timestamps) is testable and consistently UTC. System timestamps are UTC per
/// DB-DESIGN-EFFECTIVE-DATING-001.
/// </summary>
public interface IClock
{
    /// <summary>Current instant in UTC.</summary>
    DateTimeOffset UtcNow { get; }
}
