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
    code = serializers.CharField()

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


class BreakdownWithGroupsSerializer(BaseDimensionSerializer):
    groups = serializers.SlugRelatedField(slug_field="code", many=True, read_only=True)

    class Meta(BaseDimensionSerializer.Meta):
        model = Breakdown
        fields = BaseDimensionSerializer.Meta.fields + ["groups"]


class UnitSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Unit


class CountrySerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Country
        fields = BaseDimensionSerializer.Meta.fields + ["color", "is_group"]


class PeriodSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Period


class DataSourceSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = DataSource
        fields = BaseDimensionSerializer.Meta.fields + ["note", "url"]


class IndicatorListSerializer(BaseDimensionSerializer):
    data_sources = serializers.SlugRelatedField(
        slug_field="code", read_only=True, many=True
    )
    groups = serializers.SlugRelatedField(slug_field="code", many=True, read_only=True)

    class Meta(BaseDimensionSerializer.Meta):
        model = Indicator
        fields = BaseDimensionSerializer.Meta.fields + [
            "data_sources",
            "groups",
        ]


class IndicatorDetailSerializer(IndicatorListSerializer):
    data_sources = DataSourceSerializer(many=True, read_only=True)

    class Meta(IndicatorListSerializer.Meta):
        fields = IndicatorListSerializer.Meta.fields + [
            "definition",
            "note",
        ]


class IndicatorGroupListSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = IndicatorGroup


class IndicatorGroupDetailSerializer(serializers.ModelSerializer):
    indicators = serializers.SlugRelatedField(
        slug_field="code", many=True, read_only=True
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

    period = serializers.CharField(source="period.code", read_only=True)
    country = serializers.CharField(source="country.code", read_only=True)
    indicator = serializers.CharField(source="indicator.code", read_only=True)
    breakdown = serializers.CharField(source="breakdown.code", read_only=True)
    unit = serializers.CharField(source="unit.code", read_only=True)

    class Meta:
        model = Fact
        fields = [
            "period",
            "indicator",
            "breakdown",
            "unit",
            "country",
            "value",
            "flags",
        ]
