using System.Reflection;
using HRMS.Platform.Abstractions;
using HRMS.Platform.Data;
using HRMS.SharedKernel;
using NetArchTest.Rules;
using Xunit;

namespace HRMS.ArchitectureTests;

/// <summary>
/// Data-access boundary rules (ADR-037). These make "the repository base is the only way to
/// build SQL" structurally true: only <c>HRMS.Platform.Data</c> may reference Dapper /
/// Microsoft.Data.SqlClient, and EF Core must not be referenced anywhere (it was removed).
/// The rules apply to the whole solution, so they also cover future module assemblies.
/// </summary>
public class DataAccessBoundaryTests
{
    // The solution assemblies currently in play. Business modules are added as they are built;
    // these rules then cover them automatically because they scan each assembly's dependencies.
    private static readonly Assembly[] NonKernelAssemblies =
    [
        typeof(Entity<>).Assembly,                             // HRMS.SharedKernel
        typeof(ITenantContext).Assembly,                       // HRMS.Platform.Abstractions
        typeof(HRMS.Platform.Infrastructure.SystemClock).Assembly, // HRMS.Platform.Infrastructure
        typeof(Program).Assembly,                              // HRMS.Api (host)
    ];

    [Fact]
    public void Only_the_data_kernel_may_depend_on_Dapper()
    {
        foreach (var assembly in NonKernelAssemblies)
        {
            var result = Types.InAssembly(assembly)
                .Should()
                .NotHaveDependencyOn(ArchitectureConventions.Dapper)
                .GetResult();

            Assert.True(result.IsSuccessful, Describe(assembly, "Dapper", result));
        }
    }

    [Fact]
    public void Only_the_data_kernel_may_depend_on_SqlClient()
    {
        foreach (var assembly in NonKernelAssemblies)
        {
            var result = Types.InAssembly(assembly)
                .Should()
                .NotHaveDependencyOn(ArchitectureConventions.SqlClient)
                .GetResult();

            Assert.True(result.IsSuccessful, Describe(assembly, "Microsoft.Data.SqlClient", result));
        }
    }

    [Fact]
    public void No_assembly_may_depend_on_EntityFrameworkCore()
    {
        // ADR-037 removed EF Core. Include the kernel itself in this rule.
        var all = NonKernelAssemblies.Append(typeof(PlatformDataAssembly).Assembly);

        foreach (var assembly in all)
        {
            var result = Types.InAssembly(assembly)
                .Should()
                .NotHaveDependencyOn(ArchitectureConventions.EntityFrameworkCore)
                .GetResult();

            Assert.True(result.IsSuccessful, Describe(assembly, "Microsoft.EntityFrameworkCore", result));
        }
    }

    private static string Describe(Assembly assembly, string forbidden, TestResult result)
    {
        var offenders = result.FailingTypeNames is null
            ? "(none reported)"
            : string.Join(", ", result.FailingTypeNames);
        return $"{assembly.GetName().Name} must not depend on {forbidden}. Offending types: {offenders}";
    }
}
