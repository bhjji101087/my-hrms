using HRMS.Platform.Data.Mapping;
using HRMS.SharedKernel;

namespace HRMS.Platform.Data.Tests.Mapping;

// Test fixtures modelling the shapes the registry/validator must handle.

/// <summary>A fully-compliant tenant-scoped, soft-deletable, effective-dated entity.</summary>
[Table("Employee", Schema = "hr")]
internal sealed class SampleEmployee : Entity<Guid>, ITenantScopedEntity, ISoftDeletable, IEffectiveDated
{
    public Guid TenantId { get; init; }
    public string CreatedBy { get; init; } = string.Empty;
    public DateTimeOffset CreatedDate { get; init; }
    public string ModifiedBy { get; init; } = string.Empty;
    public DateTimeOffset ModifiedDate { get; init; }
    public bool IsDeleted { get; init; }
    public int VersionNumber { get; init; }
    public DateOnly EffectiveFrom { get; init; }
    public DateOnly? EffectiveTo { get; init; }

    public string FirstName { get; init; } = string.Empty;

    [ConcurrencyToken]
    public byte[] RowVersion { get; init; } = [];

    // Computed — must not be treated as a column.
    [NotMapped]
    public string DisplayName => FirstName;
}

/// <summary>A tenant-scoped entity that (incorrectly) omits several mandatory columns.</summary>
[Table("Broken", Schema = "hr")]
internal sealed class MissingMandatoryColumnsEntity : Entity<Guid>, ITenantScopedEntity
{
    public Guid TenantId { get; init; }
    // Deliberately missing CreatedBy/CreatedDate/ModifiedBy/ModifiedDate/IsDeleted/VersionNumber.
}

/// <summary>An effective-dated entity missing its valid-time columns.</summary>
[Table("NoValidTime", Schema = "hr")]
internal sealed class MissingEffectiveDatingEntity
    : Entity<Guid>, ITenantScopedEntity, IEffectiveDated
{
    public Guid TenantId { get; init; }
    public string CreatedBy { get; init; } = string.Empty;
    public DateTimeOffset CreatedDate { get; init; }
    public string ModifiedBy { get; init; } = string.Empty;
    public DateTimeOffset ModifiedDate { get; init; }
    public bool IsDeleted { get; init; }
    public int VersionNumber { get; init; }

    // IEffectiveDated implemented explicitly WITHOUT public EffectiveFrom/EffectiveTo columns.
    DateOnly IEffectiveDated.EffectiveFrom => default;
    DateOnly? IEffectiveDated.EffectiveTo => null;
}

/// <summary>An entity with a custom column name and no [Table] schema — used for error tests.</summary>
[Table("NoSchema")]
internal sealed class NoSchemaEntity : Entity<Guid>
{
    public Guid TenantId { get; init; }
}
