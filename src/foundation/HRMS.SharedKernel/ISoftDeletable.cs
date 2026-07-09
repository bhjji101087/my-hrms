namespace HRMS.SharedKernel;

/// <summary>
/// Marks an entity that supports soft delete. Combined with tenant filtering in the
/// repository-injected predicate (ADR-037; see TECH-TENANT-001 §7).
/// </summary>
public interface ISoftDeletable
{
    bool IsDeleted { get; }
}
