namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// A single mapped column: the database column name and the CLR property it binds to.
/// </summary>
/// <param name="ColumnName">The database column name.</param>
/// <param name="PropertyName">The CLR property name.</param>
/// <param name="IsKey">True if this is the entity's primary-key column.</param>
/// <param name="IsConcurrencyToken">True if this is the optimistic-concurrency token column.</param>
public sealed record ColumnMap(
    string ColumnName,
    string PropertyName,
    bool IsKey,
    bool IsConcurrencyToken);
