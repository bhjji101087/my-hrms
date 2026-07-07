using HRMS.Platform.Abstractions;

namespace HRMS.Api;

/// <summary>
/// Host-side composition of modules. The host holds the explicit list of modules it ships
/// with; each is registered through its <see cref="IModule"/> seam. Adding a business
/// module later means adding one project reference and one line to <see cref="Modules"/> —
/// the host never references module internals.
/// </summary>
public static class ModuleRegistration
{
    /// <summary>
    /// The modules composed into this host. Empty during S0 scaffold; foundation and
    /// business modules are appended here as they are built (Tenant, Identity, ...).
    /// </summary>
    private static readonly IReadOnlyList<IModule> Modules = new List<IModule>();

    public static IServiceCollection AddModules(this IServiceCollection services, IConfiguration configuration)
    {
        foreach (var module in Modules)
        {
            module.AddModule(services, configuration);
        }

        return services;
    }

    public static WebApplication MapModuleEndpoints(this WebApplication app)
    {
        foreach (var module in Modules)
        {
            module.MapEndpoints(app);
        }

        return app;
    }
}
