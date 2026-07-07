using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Routing;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace HRMS.Platform.Abstractions;

/// <summary>
/// Contract every module implements so the host can compose it without referencing the
/// module's internal types. This is the in-process module boundary of the Modular
/// Monolith (ADR-004): the host calls <see cref="AddModule"/> at startup to register the
/// module's services and <see cref="MapEndpoints"/> to expose its endpoints. A module can
/// later be extracted to a microservice because the host only ever touches this seam.
/// </summary>
public interface IModule
{
    /// <summary>Stable, unique module name (used for logging, schema prefixing, discovery).</summary>
    string Name { get; }

    /// <summary>Register the module's services into the host DI container.</summary>
    IServiceCollection AddModule(IServiceCollection services, IConfiguration configuration);

    /// <summary>Map the module's HTTP endpoints onto the host route builder.</summary>
    IEndpointRouteBuilder MapEndpoints(IEndpointRouteBuilder endpoints);
}
