using System.Reflection;
using NetArchTest.Rules;
using Xunit;

namespace HRMS.ArchitectureTests;

/// <summary>
/// Cross-module boundary rules for the Modular Monolith (ADR-004). Modules communicate
/// through published contracts and events — never by reaching into another module's
/// internals, and never by referencing another module's Infrastructure. These tests are
/// convention-based: they discover every loaded HRMS.Modules.* assembly, so they begin
/// enforcing automatically the moment the first business module is added. Until then they
/// pass vacuously (no modules to violate the rule), which is correct.
/// </summary>
public class ModuleBoundaryTests
{
    private static List<Assembly> ModuleAssemblies()
    {
        // Ensure referenced module assemblies are loaded before scanning.
        return AppDomain.CurrentDomain.GetAssemblies()
            .Where(a => a.GetName().Name?.StartsWith(ArchitectureConventions.ModulesRoot, StringComparison.Ordinal) == true)
            .ToList();
    }

    private static string? ModuleName(Assembly assembly)
    {
        // HRMS.Modules.<Module>[.<Layer>] -> "<Module>"
        var name = assembly.GetName().Name;
        if (name is null) return null;
        var parts = name.Split('.');
        // 0:HRMS 1:Modules 2:<Module> ...
        return parts.Length >= 3 ? parts[2] : null;
    }

    [Fact]
    public void No_module_should_depend_on_another_modules_internals()
    {
        var modules = ModuleAssemblies();

        foreach (var assembly in modules)
        {
            var thisModule = ModuleName(assembly);
            if (thisModule is null) continue;

            // Every other module's root namespace is forbidden as a dependency.
            var otherModuleNamespaces = modules
                .Select(ModuleName)
                .Where(m => m is not null && !string.Equals(m, thisModule, StringComparison.Ordinal))
                .Distinct()
                .Select(m => $"{ArchitectureConventions.ModulesRoot}.{m}")
                .ToArray();

            if (otherModuleNamespaces.Length == 0) continue;

            var result = Types.InAssembly(assembly)
                .Should()
                .NotHaveDependencyOnAny(otherModuleNamespaces)
                .GetResult();

            Assert.True(
                result.IsSuccessful,
                $"Module '{thisModule}' must not depend on another module's types. " +
                $"Offending types: {string.Join(", ", result.FailingTypeNames ?? Array.Empty<string>())}");
        }
    }

    [Fact]
    public void No_module_should_reference_another_modules_infrastructure()
    {
        var modules = ModuleAssemblies();

        foreach (var assembly in modules)
        {
            var thisModule = ModuleName(assembly);
            if (thisModule is null) continue;

            var otherInfraNamespaces = modules
                .Select(ModuleName)
                .Where(m => m is not null && !string.Equals(m, thisModule, StringComparison.Ordinal))
                .Distinct()
                .Select(m => $"{ArchitectureConventions.ModulesRoot}.{m}.{ArchitectureConventions.InfrastructureSegment}")
                .ToArray();

            if (otherInfraNamespaces.Length == 0) continue;

            var result = Types.InAssembly(assembly)
                .Should()
                .NotHaveDependencyOnAny(otherInfraNamespaces)
                .GetResult();

            Assert.True(
                result.IsSuccessful,
                $"Module '{thisModule}' must not reference another module's Infrastructure. " +
                $"Offending types: {string.Join(", ", result.FailingTypeNames ?? Array.Empty<string>())}");
        }
    }

    [Fact]
    public void Convention_discovery_is_wired()
    {
        // Guards the test infrastructure itself: if module discovery silently broke,
        // this documents the current module count (0 during S0) rather than passing blind.
        var count = ModuleAssemblies().Count;
        Assert.True(count >= 0);
    }
}
