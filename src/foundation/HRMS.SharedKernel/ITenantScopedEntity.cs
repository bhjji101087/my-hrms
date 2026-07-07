namespace HRMS.SharedKernel;

/// <summary>
/// Marks an entity as tenant-scoped. Every tenant-scoped root entity must carry
/// <see cref="TenantId"/> so EF global query filters and SQL Server RLS can enforce
/// isolation. See docs/09-development/TECH-TENANT-001-technical-design.md §7.
/// </summary>
public interface ITenantScopedEntity
{
    Guid TenantId { get; }
}
