namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// The resolved persistence description of one entity type: its schema-qualified table, its
/// columns, and the behaviour flags (derived from the SharedKernel marker interfaces the
/// entity implements). The SQL builder (US-D3) and repository bases (US-D6/D8) read this to
/// generate schema-qualified, explicit-column, tenant/soft-delete/as-of-aware SQL.
/// </summary>
public sealed class EntityMap
{
    public EntityMap(
        Type entityType,
        string schema,
        string table,
        IReadOnlyList<ColumnMap> columns,
        bool isTenantScoped,
        bool isSoftDeletable,
        bool isEffectiveDated)
    {
        EntityType = entityType;
        Schema = schema;
        Table = table;
        Columns = columns;
        IsTenantScoped = isTenantScoped;
        IsSoftDeletable = isSoftDeletable;
        IsEffectiveDated = isEffectiveDated;

        KeyColumn = columns.SingleOrDefault(c => c.IsKey);
        ConcurrencyColumn = columns.SingleOrDefault(c => c.IsConcurrencyToken);
    }

    public Type EntityType { get; }

    /// <summary>Owning module schema (schema-per-module).</summary>
    public string Schema { get; }

    /// <summary>Table name (without schema).</summary>
    public string Table { get; }

    /// <summary>Bracket-quoted, schema-qualified table reference, e.g. <c>[hr].[Employee]</c>.</summary>
    public string QualifiedTable => $"[{Schema}].[{Table}]";

    /// <summary>All mapped columns, in a deterministic order.</summary>
    public IReadOnlyList<ColumnMap> Columns { get; }

    /// <summary>The primary-key column, if one was identified.</summary>
    public ColumnMap? KeyColumn { get; }

    /// <summary>The optimistic-concurrency column, if the entity declares one.</summary>
    public ColumnMap? ConcurrencyColumn { get; }

    /// <summary>True when the entity implements <c>ITenantScopedEntity</c>.</summary>
    public bool IsTenantScoped { get; }

    /// <summary>True when the entity implements <c>ISoftDeletable</c>.</summary>
    public bool IsSoftDeletable { get; }

    /// <summary>True when the entity implements <c>IEffectiveDated</c>.</summary>
    public bool IsEffectiveDated { get; }

    /// <summary>True if a column with the given name (case-insensitive) is mapped.</summary>
    public bool HasColumn(string columnName) =>
        Columns.Any(c => string.Equals(c.ColumnName, columnName, StringComparison.OrdinalIgnoreCase));
}
