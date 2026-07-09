using HRMS.SharedKernel;
using NetArchTest.Rules;
using Xunit;

namespace HRMS.ArchitectureTests;

/// <summary>
/// Boundary rules for the foundation (building-block) layer. These keep the shared kernel
/// dependency-free and prevent infrastructure from leaking upward — the base guarantees
/// that let modules stay independently extractable (ADR-004).
/// </summary>
public class FoundationBoundaryTests
{
    [Fact]
    public void SharedKernel_should_not_depend_on_platform_or_host()
    {
        var result = Types.InAssembly(typeof(Entity<>).Assembly)
            .Should()
            .NotHaveDependencyOnAny(
                ArchitectureConventions.Abstractions,
                ArchitectureConventions.Infrastructure,
                ArchitectureConventions.Host)
            .GetResult();

        Assert.True(result.IsSuccessful, Describe("SharedKernel must not depend on Abstractions, Infrastructure, or the host", result));
    }

    [Fact]
    public void Abstractions_should_not_depend_on_infrastructure_or_host()
    {
        var result = Types.InAssembly(typeof(HRMS.Platform.Abstractions.ITenantContext).Assembly)
            .Should()
            .NotHaveDependencyOnAny(
                ArchitectureConventions.Infrastructure,
                ArchitectureConventions.Host)
            .GetResult();

        Assert.True(result.IsSuccessful, Describe("Abstractions must not depend on Infrastructure or the host (depend on abstractions, not implementations)", result));
    }

    [Fact]
    public void Infrastructure_should_not_depend_on_host()
    {
        var result = Types.InAssembly(typeof(HRMS.Platform.Infrastructure.SystemClock).Assembly)
            .Should()
            .NotHaveDependencyOn(ArchitectureConventions.Host)
            .GetResult();

        Assert.True(result.IsSuccessful, Describe("Infrastructure must not depend on the host", result));
    }

    private static string Describe(string rule, TestResult result)
    {
        var offenders = result.FailingTypeNames is null
            ? "(none reported)"
            : string.Join(", ", result.FailingTypeNames);
        return $"Architecture rule violated: {rule}. Offending types: {offenders}";
    }
}
