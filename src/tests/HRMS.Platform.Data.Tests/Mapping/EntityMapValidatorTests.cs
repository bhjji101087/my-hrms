using HRMS.Platform.Data.Mapping;
using Xunit;

namespace HRMS.Platform.Data.Tests.Mapping;

public class EntityMapValidatorTests
{
    private readonly EntityMapRegistry _registry = new();

    [Fact]
    public void Compliant_entity_passes()
    {
        var map = _registry.Resolve<SampleEmployee>();

        // Should not throw.
        EntityMapValidator.ValidateAll([map]);
    }

    [Fact]
    public void Fails_when_mandatory_columns_are_missing()
    {
        var map = _registry.Resolve<MissingMandatoryColumnsEntity>();

        var ex = Assert.Throws<EntityMappingException>(() => EntityMapValidator.ValidateAll([map]));

        // Every missing mandatory column is reported (not just the first).
        Assert.Contains("CreatedBy", ex.Message);
        Assert.Contains("CreatedDate", ex.Message);
        Assert.Contains("IsDeleted", ex.Message);
        Assert.Contains("VersionNumber", ex.Message);
    }

    [Fact]
    public void Fails_when_effective_dated_entity_lacks_valid_time_columns()
    {
        var map = _registry.Resolve<MissingEffectiveDatingEntity>();

        var ex = Assert.Throws<EntityMappingException>(() => EntityMapValidator.ValidateAll([map]));

        Assert.Contains("EffectiveFrom", ex.Message);
        Assert.Contains("EffectiveTo", ex.Message);
    }

    [Fact]
    public void Aggregates_problems_across_multiple_maps()
    {
        var good = _registry.Resolve<SampleEmployee>();
        var bad1 = _registry.Resolve<MissingMandatoryColumnsEntity>();
        var bad2 = _registry.Resolve<MissingEffectiveDatingEntity>();

        var ex = Assert.Throws<EntityMappingException>(
            () => EntityMapValidator.ValidateAll([good, bad1, bad2]));

        // Problems from both bad entities are surfaced in one boot.
        Assert.Contains(nameof(MissingMandatoryColumnsEntity), ex.Message);
        Assert.Contains(nameof(MissingEffectiveDatingEntity), ex.Message);
    }
}
