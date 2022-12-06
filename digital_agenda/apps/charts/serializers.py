from rest_framework import serializers

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.core.serializers import IndicatorGroupDetailSerializer
from digital_agenda.apps.core.serializers import PeriodSerializer


class ChartGroupListSerializer(serializers.ModelSerializer):
    periods = serializers.SlugRelatedField(slug_field="code", many=True, read_only=True)

    class Meta:
        model = ChartGroup
        fields = (
            "code",
            "name",
            "short_name",
            "description",
            "image",
            "is_draft",
            "periods",
            # Custom labels
            "indicator_group_label",
            "indicator_label",
            "breakdown_group_label",
            "breakdown_label",
            "period_label",
            "unit_label",
        )
        read_only_fields = fields


class ChartGroupDetailSerializer(serializers.ModelSerializer):
    periods = PeriodSerializer(many=True, read_only=True)
    indicator_groups = IndicatorGroupDetailSerializer(many=True, read_only=True)

    class Meta:
        model = ChartGroup
        fields = ChartGroupListSerializer.Meta.fields + ("indicator_groups",)
        read_only_fields = fields


class ChartSerializer(serializers.ModelSerializer):
    chart_group = serializers.SlugRelatedField(
        slug_field="code", read_only=True, many=False
    )

    class Meta:
        model = Chart
        fields = (
            "name",
            "code",
            "chart_type",
            "description",
            "chart_group",
            "is_draft",
        )
        read_only_fields = fields
