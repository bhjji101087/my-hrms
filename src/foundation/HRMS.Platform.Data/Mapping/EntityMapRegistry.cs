using System.Collections.Concurrent;
using System.Reflection;
using HRMS.SharedKernel;

namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// Builds <see cref="EntityMap"/>s from entity types using a convention + attribute model:
/// every public readable instance property is a column (name = property name) unless marked
/// <see cref="NotMappedAttribute"/>; <see cref="ColumnAttribute"/> overrides the column name.
/// Behaviour flags come from the SharedKernel marker interfaces the entity implements. Maps
/// are cached per type.
/// </summary>
public sealed class EntityMapRegistry : IEntityMapRegistry
{
    private readonly ConcurrentDictionary<Type, EntityMap> _cache = new();

    public EntityMap Resolve<TEntity>() => Resolve(typeof(TEntity));

    public EntityMap Resolve(Type entityType)
    {
        ArgumentNullException.ThrowIfNull(entityType);
        return _cache.GetOrAdd(entityType, Build);
    }

    private static EntityMap Build(Type entityType)
    {
        var table = entityType.GetCustomAttribute<TableAttribute>()
            ?? throw new EntityMappingException(
                $"Entity '{entityType.Name}' must declare a [Table(...)] attribute.");

        if (string.IsNullOrWhiteSpace(table.Schema))
            throw new EntityMappingException(
                $"Entity '{entityType.Name}' [Table] must specify a Schema (schema-per-module).");

        var columns = BuildColumns(entityType);

        return new EntityMap(
            entityType,
            table.Schema,
            table.Name,
            columns,
            isTenantScoped: typeof(ITenantScopedEntity).IsAssignableFrom(entityType),
            isSoftDeletable: typeof(ISoftDeletable).IsAssignableFrom(entityType),
            isEffectiveDated: typeof(IEffectiveDated).IsAssignableFrom(entityType));
    }

    private static List<ColumnMap> BuildColumns(Type entityType)
    {
        var keyPropertyName = ResolveKeyPropertyName(entityType);
        var columns = new List<ColumnMap>();
        var concurrencyCount = 0;

        // Deterministic ordering: declaration order is not guaranteed by reflection, so sort by
        // name for stable generated SQL (tests assert on generated SQL text).
        var properties = entityType
            .GetProperties(BindingFlags.Public | BindingFlags.Instance)
            .Where(p => p.CanRead && p.GetIndexParameters().Length == 0)
            .Where(p => p.GetCustomAttribute<NotMappedAttribute>() is null)
            .OrderBy(p => p.Name, StringComparer.Ordinal);

        foreach (var property in properties)
        {
            var columnName = property.GetCustomAttribute<ColumnAttribute>()?.Name ?? property.Name;
            var isConcurrency = property.GetCustomAttribute<ConcurrencyTokenAttribute>() is not null;
            if (isConcurrency) concurrencyCount++;

            columns.Add(new ColumnMap(
                columnName,
                property.Name,
                IsKey: string.Equals(property.Name, keyPropertyName, StringComparison.Ordinal),
                IsConcurrencyToken: isConcurrency));
        }

        if (concurrencyCount > 1)
            throw new EntityMappingException(
                $"Entity '{entityType.Name}' declares more than one [ConcurrencyToken] property.");

        if (columns.Count == 0)
            throw new EntityMappingException(
                $"Entity '{entityType.Name}' has no mapped columns.");

        return columns;
    }

    private static string? ResolveKeyPropertyName(Type entityType)
    {
        // Entities derive from Entity<TId>, whose key property is "Id".
        return entityType.GetProperty("Id", BindingFlags.Public | BindingFlags.Instance)?.Name;
    }
}
