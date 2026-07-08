using HRMS.Platform.Abstractions;

namespace HRMS.Platform.Infrastructure;

/// <summary>
/// Default <see cref="IClock"/> backed by the real system clock, always UTC.
/// </summary>
public sealed class SystemClock : IClock
{
    public DateTimeOffset UtcNow => DateTimeOffset.UtcNow;
}
