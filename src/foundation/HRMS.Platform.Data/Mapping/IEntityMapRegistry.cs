namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// Resolves and caches the <see cref="EntityMap"/> for an entity type. The map is built once
/// (reflection) and reused for the life of the process.
/// </summary>
public interface IEntityMapRegistry
{
    /// <summary>Get the map for <typeparamref name="TEntity"/>.</summary>
    EntityMap Resolve<TEntity>();

    /// <summary>Get the map for the given entity type.</summary>
    EntityMap Resolve(Type entityType);
}
