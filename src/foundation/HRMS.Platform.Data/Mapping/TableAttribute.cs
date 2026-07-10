namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// Declares the SQL schema and table an entity maps to (schema-per-module, ADR-004).
/// Required on every persisted entity so the SQL builder can schema-qualify table names.
/// </summary>
[AttributeUsage(AttributeTargets.Class, AllowMultiple = false, Inherited = false)]
public sealed class TableAttribute : Attribute
{
    public TableAttribute(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Table name must be provided.", nameof(name));
        Name = name;
    }

    /// <summary>The table name (without schema).</summary>
    public string Name { get; }

    /// <summary>The owning module schema (e.g. "hr", "leave", "payroll"). Required.</summary>
    public string Schema { get; init; } = string.Empty;
}
