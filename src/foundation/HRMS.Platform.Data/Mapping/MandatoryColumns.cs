namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// The columns every persisted table must carry (DATABASE_STANDARDS "Mandatory Columns"),
/// plus the tenant/effective-dating columns required by the marker interfaces. The startup
/// self-check (<see cref="EntityMapValidator"/>) fails the boot if any are missing.
/// </summary>
public static class MandatoryColumns
{
    /// <summary>Required on every table.</summary>
    public static readonly IReadOnlyList<string> Common =
    [
        "TenantId",
        "CreatedBy",
        "CreatedDate",
        "ModifiedBy",
        "ModifiedDate",
        "IsDeleted",
        "VersionNumber",
    ];

    /// <summary>Required additionally on tenant-scoped entities (already covered by Common, kept explicit).</summary>
    public const string TenantId = "TenantId";

    /// <summary>Required additionally on effective-dated entities.</summary>
    public static readonly IReadOnlyList<string> EffectiveDating =
    [
        "EffectiveFrom",
        "EffectiveTo",
    ];
}
