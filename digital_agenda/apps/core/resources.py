from import_export import resources

from digital_agenda.apps.core.models import (
    DataSource,
    Indicator,
    Breakdown,
    Period,
    Unit,
    Country,
)


class DimensionResource(resources.ModelResource):
    class Meta:
        import_id_fields = ("code",)
        fields = ("code", "label", "alt_label", "definition", "note")


class DataSourceResource(DimensionResource):
    class Meta:
        model = DataSource
        fields = DimensionResource.Meta.fields + ("url",)


class IndicatorResource(DimensionResource):
    class Meta:
        model = Indicator
        fields = DimensionResource.Meta.fields + ("time_coverage",)


class BreakdownResource(DimensionResource):
    class Meta:
        model = Breakdown


class PeriodResource(DimensionResource):
    class Meta:
        model = Period
        fields = DimensionResource.Meta.fields + ("date",)


class UnitResource(DimensionResource):
    class Meta:
        model = Unit


class CountryResource(DimensionResource):
    class Meta:
        model = Country
        fields = DimensionResource.Meta.fields + ("is_group", "color")
