from rest_framework import serializers

from .models import (
    IndicatorGroup,
    Indicator,
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
        fields = ["code", "label", "alt_label"]


class BreakdownSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Breakdown


class BreakdownGroupSerializer(serializers.ModelSerializer):

    breakdowns = BreakdownSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = BreakdownGroup
        fields = (
            "code",
            "label",
            "alt_label",
            "breakdowns",
        )


class UnitSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Unit


class CountrySerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Country


class PeriodSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Period


class BaseIndicatorSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Indicator


class IndicatorSerializer(BaseIndicatorSerializer):

    breakdowns = BreakdownSerializer(many=True, read_only=True)
    units = UnitSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    periods = PeriodSerializer(many=True, read_only=True)

    class Meta(BaseIndicatorSerializer.Meta):
        fields = BaseIndicatorSerializer.Meta.fields + [
            "definition",
            "note",
            "breakdowns",
            "units",
            "countries",
            "periods",
        ]


class IndicatorGroupSerializer(serializers.ModelSerializer):

    indicators = BaseIndicatorSerializer(
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
