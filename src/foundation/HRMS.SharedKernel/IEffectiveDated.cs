namespace HRMS.SharedKernel;

/// <summary>
/// Base contract for effective-dated (valid-time) records. An open-ended record has
/// <see cref="EffectiveTo"/> == null. See ADR-007 and
/// docs/06-database/DB-DESIGN-EFFECTIVE-DATING-001.md.
/// </summary>
public interface IEffectiveDated
{
    /// <summary>Inclusive start of the valid-time period (tenant-local date).</summary>
    DateOnly EffectiveFrom { get; }

    /// <summary>Inclusive end of the valid-time period, or null when open-ended (active).</summary>
    DateOnly? EffectiveTo { get; }
}
