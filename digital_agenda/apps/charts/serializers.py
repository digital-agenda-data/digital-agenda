from rest_framework import serializers

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.serializers import IndicatorGroupDetailSerializer
from digital_agenda.apps.core.serializers import PeriodSerializer


class CodeRelatedField(serializers.SlugRelatedField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("slug_field", "code")
        kwargs.setdefault("read_only", True)

        super().__init__(*args, **kwargs)


class ChartGroupListSerializer(serializers.ModelSerializer):
    periods = CodeRelatedField(many=True)
    indicator_groups = CodeRelatedField(many=True)

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


class ChartGroupDetailSerializer(serializers.ModelSerializer):
    periods = PeriodSerializer(many=True, read_only=True)
    indicator_groups = IndicatorGroupDetailSerializer(many=True, read_only=True)

    class Meta:
        model = ChartGroup
        fields = ChartGroupListSerializer.Meta.fields
        read_only_fields = fields


class ChartSerializer(serializers.ModelSerializer):
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
            "name",
            "code",
            "chart_type",
            "description",
            "chart_group",
            "is_draft",
            *Chart.filter_options,
        )
        read_only_fields = fields


class ChartGroupIndicatorSearchSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source="groups__code", read_only=True)
    chart_group = serializers.CharField(
        source="groups__chartgroup__code", read_only=True
    )

    class Meta:
        model = Indicator
        fields = [
            "code",
            "label",
            "alt_label",
            "definition",
            "group",
            "chart_group",
        ]
