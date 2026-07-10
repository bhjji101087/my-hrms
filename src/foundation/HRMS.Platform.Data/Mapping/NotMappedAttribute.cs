namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// Excludes a property from mapping. Use on computed/derived properties that are not database
/// columns. By convention every other public readable property is treated as a column.
/// </summary>
[AttributeUsage(AttributeTargets.Property, AllowMultiple = false, Inherited = true)]
public sealed class NotMappedAttribute : Attribute;
