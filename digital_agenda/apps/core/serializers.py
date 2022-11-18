from rest_framework import serializers

from .models import (
    IndicatorGroup,
    Indicator,
    DataSource,
    BreakdownGroup,
    Breakdown,
    Unit,
    Country,
    Period,
    Fact,
)

########################
# Dimensions serializers
########################


class BaseDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["code", "label", "alt_label", "definition"]


class BreakdownSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Breakdown


class BreakdownGroupListSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = BreakdownGroup


class BreakdownGroupDetailSerializer(BreakdownGroupListSerializer):

    breakdowns = BreakdownSerializer(
        many=True,
        read_only=True,
    )

    class Meta(BreakdownGroupListSerializer.Meta):
        fields = BreakdownGroupListSerializer.Meta.fields + [
            "breakdowns",
        ]


class UnitSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Unit


class CountrySerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Country


class PeriodSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Period


class DataSourceSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = DataSource
        fields = BaseDimensionSerializer.Meta.fields + ["note", "url"]


class IndicatorListSerializer(BaseDimensionSerializer):
    periods = serializers.SlugRelatedField(many=True, slug_field="code", read_only=True)
    data_source = serializers.SlugRelatedField(slug_field="code", read_only=True)

    class Meta(BaseDimensionSerializer.Meta):
        model = Indicator
        fields = BaseDimensionSerializer.Meta.fields + [
            "periods",
            "data_source",
        ]


class IndicatorDetailSerializer(IndicatorListSerializer):

    breakdowns = BreakdownSerializer(many=True, read_only=True)
    units = UnitSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    periods = PeriodSerializer(many=True, read_only=True)
    data_source = DataSourceSerializer(many=False, read_only=True)

    class Meta(IndicatorListSerializer.Meta):
        fields = IndicatorListSerializer.Meta.fields + [
            "definition",
            "note",
            "breakdowns",
            "units",
            "countries",
        ]


class IndicatorGroupListSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = IndicatorGroup


class IndicatorGroupDetailSerializer(serializers.ModelSerializer):

    indicators = IndicatorListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = IndicatorGroup
        fields = (
            "code",
            "label",
            "alt_label",
            "indicators",
        )


###################
# Facts serializers
###################


class CountryFactSerializer(serializers.ModelSerializer):

    country = serializers.CharField(source="country.code", read_only=True)

    class Meta:
        model = Fact
        fields = ["country", "value", "flags"]
