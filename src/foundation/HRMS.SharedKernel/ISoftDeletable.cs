namespace HRMS.SharedKernel;

/// <summary>
/// Marks an entity that supports soft delete. Combined with tenant filtering in the
/// EF global query filter (see TECH-TENANT-001 §7).
/// </summary>
public interface ISoftDeletable
{
    bool IsDeleted { get; }
}
