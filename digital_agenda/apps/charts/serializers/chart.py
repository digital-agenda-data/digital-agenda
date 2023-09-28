import math

from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.core.serializers import IndicatorListSerializer
from digital_agenda.common.serializers import CodeRelatedField


class ChartSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(read_only=True)
    chart_group = CodeRelatedField()
    indicator_group_filter_defaults = CodeRelatedField(many=True)
    indicator_group_filter_ignored = CodeRelatedField(many=True)

    indicator_filter_defaults = CodeRelatedField(many=True)
    indicator_filter_ignored = CodeRelatedField(many=True)

    breakdown_group_filter_defaults = CodeRelatedField(many=True)
    breakdown_group_filter_ignored = CodeRelatedField(many=True)

    breakdown_filter_defaults = CodeRelatedField(many=True)
    breakdown_filter_ignored = CodeRelatedField(many=True)

    period_filter_defaults = CodeRelatedField(many=True)
    period_filter_ignored = CodeRelatedField(many=True)

    unit_filter_defaults = CodeRelatedField(many=True)
    unit_filter_ignored = CodeRelatedField(many=True)

    country_filter_defaults = CodeRelatedField(many=True)
    country_filter_ignored = CodeRelatedField(many=True)

    class Meta:
        model = Chart
        fields = (
            "id",
            "name",
            "code",
            "chart_type",
            "description",
            "chart_group",
            "is_draft",
            "image",
            *Chart.filter_options,
            "min_value",
            "max_value",
            "legend_layout",
        )
        read_only_fields = fields


class ChartIndicatorListSerializer(IndicatorListSerializer):
    min_period = serializers.SerializerMethodField(read_only=True)
    max_period = serializers.SerializerMethodField(read_only=True)

    class Meta(IndicatorListSerializer.Meta):
        fields = IndicatorListSerializer.Meta.fields + [
            "min_period",
            "max_period",
            "definition",
            "note",
            "time_coverage",
        ]

    def get_min_period(self, obj):
        return max(obj.fact_min_period.year, obj.period_start or -math.inf)

    def get_max_period(self, obj):
        return min(obj.fact_max_period.year, obj.period_end or math.inf)
