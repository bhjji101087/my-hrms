using System.Text;

namespace HRMS.Platform.Data.Mapping;

/// <summary>
/// Startup self-check for entity maps. Asserts every registered entity carries the mandatory
/// columns (DATABASE_STANDARDS) plus the columns implied by its marker interfaces. Wired into
/// application startup (US-D10) so a non-compliant map fails the boot — never a runtime leak.
/// </summary>
public static class EntityMapValidator
{
    /// <summary>
    /// Validate a set of maps. Throws <see cref="EntityMappingException"/> listing every problem
    /// found across all maps (so one boot surfaces all mapping errors, not just the first).
    /// </summary>
    public static void ValidateAll(IEnumerable<EntityMap> maps)
    {
        ArgumentNullException.ThrowIfNull(maps);

        var problems = new List<string>();

        foreach (var map in maps)
        {
            Validate(map, problems);
        }

        if (problems.Count > 0)
        {
            var sb = new StringBuilder();
            sb.AppendLine("Entity mapping validation failed:");
            foreach (var problem in problems)
            {
                sb.Append(" - ").AppendLine(problem);
            }

            throw new EntityMappingException(sb.ToString());
        }
    }

    /// <summary>Validate a single map, appending any problems to <paramref name="problems"/>.</summary>
    public static void Validate(EntityMap map, List<string> problems)
    {
        ArgumentNullException.ThrowIfNull(map);
        ArgumentNullException.ThrowIfNull(problems);

        var entity = map.EntityType.Name;

        // Every persisted table must carry the mandatory columns.
        foreach (var column in MandatoryColumns.Common)
        {
            if (!map.HasColumn(column))
            {
                problems.Add($"{entity} ({map.QualifiedTable}) is missing mandatory column '{column}'.");
            }
        }

        // Tenant-scoped entities must expose TenantId (already in Common, but assert against the
        // marker so a mis-declared entity is caught explicitly).
        if (map.IsTenantScoped && !map.HasColumn(MandatoryColumns.TenantId))
        {
            problems.Add($"{entity} implements ITenantScopedEntity but has no '{MandatoryColumns.TenantId}' column.");
        }

        // Effective-dated entities must expose the valid-time columns.
        if (map.IsEffectiveDated)
        {
            foreach (var column in MandatoryColumns.EffectiveDating)
            {
                if (!map.HasColumn(column))
                {
                    problems.Add($"{entity} implements IEffectiveDated but has no '{column}' column.");
                }
            }
        }

        // A persisted entity needs a key.
        if (map.KeyColumn is null)
        {
            problems.Add($"{entity} ({map.QualifiedTable}) has no key column (expected an 'Id' property).");
        }
    }
}
