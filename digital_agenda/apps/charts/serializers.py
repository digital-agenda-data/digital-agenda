from rest_framework import serializers

from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.core.serializers import IndicatorGroupDetailSerializer
from digital_agenda.apps.core.serializers import PeriodSerializer


class ChartGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartGroup
        fields = (
            "code",
            "name",
            "short_name",
            "description",
            "image",
            "is_draft",
        )
        read_only_fields = fields


class ChartGroupDetailSerializer(serializers.ModelSerializer):
    periods = PeriodSerializer(many=True, read_only=True)
    indicator_groups = IndicatorGroupDetailSerializer(many=True, read_only=True)

    class Meta:
        model = ChartGroup
        fields = ChartGroupListSerializer.Meta.fields + (
            "periods",
            "indicator_groups",
        )
        read_only_fields = fields
