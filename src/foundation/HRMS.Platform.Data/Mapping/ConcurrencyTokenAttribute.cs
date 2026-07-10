namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// Marks the property used for optimistic concurrency (a SQL Server <c>rowversion</c>).
/// The repository base adds <c>AND [column] = @token</c> to updates and rejects the write
/// when zero rows match. At most one property per entity may be marked.
/// </summary>
[AttributeUsage(AttributeTargets.Property, AllowMultiple = false, Inherited = true)]
public sealed class ConcurrencyTokenAttribute : Attribute;
