using HRMS.Api;
using HRMS.Platform.Abstractions;
using HRMS.Platform.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

// --- Platform services (shared across all modules) ---
builder.Services.AddSingleton<IClock, SystemClock>();

// --- OpenAPI / Swagger (Rule 5: every API documented) ---
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new()
    {
        Title = "HRMS Platform API",
        Version = "v1",
        Description = "Enterprise multi-tenant HRMS platform — modular monolith host."
    });
});

// --- Compose modules (each module registers its own services) ---
builder.Services.AddModules(builder.Configuration);

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Liveness/readiness probe used by CI and container orchestration.
app.MapGet("/health", () => Results.Ok(new { status = "healthy" }))
   .WithName("Health")
   .WithTags("Platform");

// --- Map module endpoints ---
app.MapModuleEndpoints();

app.Run();

/// <summary>Exposed so integration tests can reference the host via WebApplicationFactory.</summary>
public partial class Program;
