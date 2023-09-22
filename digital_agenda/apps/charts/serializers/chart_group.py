from rest_framework import serializers

from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.core.models import Indicator
from digital_agenda.common.serializers import CodeRelatedField


class ChartGroupSerializer(serializers.ModelSerializer):
    indicator_groups = CodeRelatedField(many=True)

    class Meta:
        model = ChartGroup
        fields = (
            "code",
            "name",
            "short_name",
            "license",
            "description",
            "image",
            "is_draft",
            "period_start",
            "period_end",
            "indicator_groups",
            # Custom labels
            "indicator_group_label",
            "indicator_label",
            "breakdown_group_label",
            "breakdown_label",
            "period_label",
            "unit_label",
        )
        read_only_fields = fields


class ChartGroupIndicatorSearchSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source="group_code", read_only=True)
    chart_group = serializers.CharField(source="chart_group_code", read_only=True)
    highlight = serializers.JSONField(read_only=True)
    rank = serializers.FloatField(read_only=True)

    class Meta:
        model = Indicator
        fields = [
            "code",
            "label",
            "alt_label",
            "definition",
            "group",
            "chart_group",
            "highlight",
            "rank",
        ]
