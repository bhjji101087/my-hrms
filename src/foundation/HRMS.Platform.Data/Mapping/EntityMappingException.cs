namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// Thrown when an entity's persistence mapping is invalid — a missing <c>[Table]</c>, a missing
/// mandatory column, or a marker/column mismatch. Surfaced at startup so a bad map fails the
/// boot rather than leaking or crashing at runtime.
/// </summary>
public sealed class EntityMappingException : Exception
{
    public EntityMappingException(string message) : base(message)
    {
    }

    public EntityMappingException(string message, Exception innerException)
        : base(message, innerException)
    {
    }
}
