namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// Overrides the column name for a property. Optional — by convention the column name equals
/// the property name, so this is only needed when they differ (e.g. Id → EmployeeId).
/// </summary>
[AttributeUsage(AttributeTargets.Property, AllowMultiple = false, Inherited = true)]
public sealed class ColumnAttribute : Attribute
{
    public ColumnAttribute(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Column name must be provided.", nameof(name));
        Name = name;
    }

    /// <summary>The database column name.</summary>
    public string Name { get; }
}
