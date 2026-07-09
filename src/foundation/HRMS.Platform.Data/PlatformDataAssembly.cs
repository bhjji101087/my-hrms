namespace HRMS.Platform.Data;

/// <summary>
/// Assembly anchor for <c>HRMS.Platform.Data</c>. Gives DI registration and architecture
/// tests a stable type to reference this assembly. The data-access components
/// (connection factory, SQL builder, repository bases, audit, effective dating) are added
/// by the subsequent FR-DATA stories (US-D2 onward).
/// </summary>
public static class PlatformDataAssembly
{
    /// <summary>The kernel's assembly name; used for architecture-boundary assertions.</summary>
    public const string Name = "HRMS.Platform.Data";
}
