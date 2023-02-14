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
    code = serializers.CharField(label="Code")
    label = serializers.CharField(label="Label")
    alt_label = serializers.CharField(label="Alt. label")
    definition = serializers.CharField(label="Definition")

    class Meta:
        fields = ["code", "label", "alt_label", "definition"]


class BreakdownSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Breakdown


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

    class Meta(BaseDimensionSerializer.Meta):
        model = Indicator
        fields = BaseDimensionSerializer.Meta.fields + ["data_sources", "note"]


class IndicatorGroupSerializer(BaseDimensionSerializer):
    members = serializers.SlugRelatedField(
        source="indicators", slug_field="code", many=True, read_only=True
    )

    class Meta(BaseDimensionSerializer.Meta):
        model = IndicatorGroup
        fields = BaseDimensionSerializer.Meta.fields + ["members"]


class BreakdownGroupSerializer(BaseDimensionSerializer):
    members = serializers.SlugRelatedField(
        source="breakdowns", slug_field="code", many=True, read_only=True
    )

    class Meta(BaseDimensionSerializer.Meta):
        model = BreakdownGroup
        fields = BaseDimensionSerializer.Meta.fields + ["members"]


###################
# Facts serializers
###################


class FactSerializer(serializers.ModelSerializer):

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


########################
# Feedback serializers
########################


class FeedbackSerializer(serializers.Serializer):
    url = serializers.URLField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=False, allow_blank=True)
    message = serializers.CharField(
        write_only=True, required=True, min_length=10, max_length=10_000
    )

    class Meta:
        fields = ["url", "email", "message"]
