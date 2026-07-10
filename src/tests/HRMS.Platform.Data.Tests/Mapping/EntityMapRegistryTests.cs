using HRMS.Platform.Data.Mapping;
using Xunit;

namespace HRMS.Platform.Data.Tests.Mapping;

public class EntityMapRegistryTests
{
    private readonly EntityMapRegistry _registry = new();

    [Fact]
    public void Maps_schema_and_table_from_TableAttribute()
    {
        var map = _registry.Resolve<SampleEmployee>();

        Assert.Equal("hr", map.Schema);
        Assert.Equal("Employee", map.Table);
        Assert.Equal("[hr].[Employee]", map.QualifiedTable);
    }

    [Fact]
    public void Derives_behaviour_flags_from_marker_interfaces()
    {
        var map = _registry.Resolve<SampleEmployee>();

        Assert.True(map.IsTenantScoped);
        Assert.True(map.IsSoftDeletable);
        Assert.True(map.IsEffectiveDated);
    }

    [Fact]
    public void Maps_public_properties_as_columns_by_convention()
    {
        var map = _registry.Resolve<SampleEmployee>();

        Assert.True(map.HasColumn("FirstName"));
        Assert.True(map.HasColumn("TenantId"));
        Assert.True(map.HasColumn("Id"));
    }

    [Fact]
    public void Excludes_NotMapped_properties()
    {
        var map = _registry.Resolve<SampleEmployee>();

        Assert.False(map.HasColumn("DisplayName"));
    }

    [Fact]
    public void Identifies_key_and_concurrency_columns()
    {
        var map = _registry.Resolve<SampleEmployee>();

        Assert.NotNull(map.KeyColumn);
        Assert.Equal("Id", map.KeyColumn!.ColumnName);

        Assert.NotNull(map.ConcurrencyColumn);
        Assert.Equal("RowVersion", map.ConcurrencyColumn!.ColumnName);
    }

    [Fact]
    public void Columns_are_ordered_deterministically()
    {
        var map = _registry.Resolve<SampleEmployee>();

        var names = map.Columns.Select(c => c.ColumnName).ToList();
        var sorted = names.OrderBy(n => n, StringComparer.Ordinal).ToList();

        Assert.Equal(sorted, names);
    }

    [Fact]
    public void Caches_the_map_per_type()
    {
        var first = _registry.Resolve<SampleEmployee>();
        var second = _registry.Resolve<SampleEmployee>();

        Assert.Same(first, second);
    }

    [Fact]
    public void Throws_when_Table_has_no_schema()
    {
        Assert.Throws<EntityMappingException>(() => _registry.Resolve<NoSchemaEntity>());
    }
}
