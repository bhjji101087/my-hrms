namespace HRMS.ArchitectureTests;

/// <summary>
/// Central place for the namespace/assembly conventions the architecture tests enforce.
/// As modules are added under HRMS.Modules.*, these conventions apply automatically.
/// </summary>
internal static class ArchitectureConventions
{
    public const string SharedKernel = "HRMS.SharedKernel";
    public const string Abstractions = "HRMS.Platform.Abstractions";
    public const string Infrastructure = "HRMS.Platform.Infrastructure";
    public const string Data = "HRMS.Platform.Data";
    public const string Host = "HRMS.Api";

    /// <summary>The data-access kernel is the ONLY project allowed to reference these (ADR-037).</summary>
    public const string Dapper = "Dapper";
    public const string SqlClient = "Microsoft.Data.SqlClient";

    /// <summary>EF Core must not be referenced anywhere (ADR-037 removed it).</summary>
    public const string EntityFrameworkCore = "Microsoft.EntityFrameworkCore";

    /// <summary>Root namespace under which every business/foundation module lives.</summary>
    public const string ModulesRoot = "HRMS.Modules";

    /// <summary>Namespace segment marking a module's internal (non-public-contract) types.</summary>
    public const string InfrastructureSegment = "Infrastructure";
}
