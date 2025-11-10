from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartFontStyle
from digital_agenda.apps.core.serializers import BaseDimensionSerializer
from digital_agenda.apps.core.serializers import FactSerializer
from digital_agenda.apps.core.serializers import IndicatorListSerializer
from digital_agenda.apps.core.serializers import PeriodSerializer
from digital_agenda.common.serializers import CodeRelatedField


class ChartFontStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartFontStyle
        fields = (
            "field",
            "font_weight",
            "font_size_px",
            "font_color",
        )


class ChartSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(read_only=True)
    chart_group = CodeRelatedField()
    indicator_group_filter_defaults = CodeRelatedField(many=True)
    indicator_group_filter_ignored = CodeRelatedField(many=True)
    indicator_group_filter_values = CodeRelatedField(many=True)

    indicator_filter_defaults = CodeRelatedField(many=True)
    indicator_filter_ignored = CodeRelatedField(many=True)
    indicator_filter_values = CodeRelatedField(many=True)

    breakdown_group_filter_defaults = CodeRelatedField(many=True)
    breakdown_group_filter_ignored = CodeRelatedField(many=True)
    breakdown_group_filter_values = CodeRelatedField(many=True)

    breakdown_filter_defaults = CodeRelatedField(many=True)
    breakdown_filter_ignored = CodeRelatedField(many=True)
    breakdown_filter_values = CodeRelatedField(many=True)

    period_filter_defaults = CodeRelatedField(many=True)
    period_filter_ignored = CodeRelatedField(many=True)
    period_filter_values = CodeRelatedField(many=True)

    unit_filter_defaults = CodeRelatedField(many=True)
    unit_filter_ignored = CodeRelatedField(many=True)
    unit_filter_values = CodeRelatedField(many=True)

    country_filter_defaults = CodeRelatedField(many=True)
    country_filter_ignored = CodeRelatedField(many=True)
    country_filter_values = CodeRelatedField(many=True)

    filter_order = serializers.SlugRelatedField(
        slug_field="filter_field", many=True, read_only=True
    )
    font_styles = ChartFontStyleSerializer(many=True, read_only=True)

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
            # Chart options
            *Chart.get_filter_options(),
            "legend_layout",
            "font_styles",
            "filter_order",
            # Labels
            "indicator_label",
            "breakdown_label",
            "period_label",
            "unit_label",
            "country_label",
            "use_period_label_for_axis",
            # Advanced Settings
            "min_value",
            "max_value",
            "min_year",
            "max_year",
        )
        read_only_fields = fields


class ChartIndicatorListSerializer(BaseDimensionSerializer):
    data_sources = serializers.SlugRelatedField(
        slug_field="code", read_only=True, many=True
    )
    time_coverage = serializers.SerializerMethodField(read_only=True)
    min_period = PeriodSerializer(read_only=True)
    max_period = PeriodSerializer(read_only=True)
    sample_fact = FactSerializer(read_only=True)

    class Meta(IndicatorListSerializer.Meta):
        fields = BaseDimensionSerializer.Meta.fields + [
            "data_sources",
            "note",
            "definition",
            "note",
            "time_coverage",
            "min_period",
            "max_period",
            "sample_fact",
        ]

    @staticmethod
    def _get_interval(start, end):
        if start == end:
            return str(start)

        return f"{start}-{end}"

    def get_time_coverage(self, obj):
        if obj.time_coverage:
            return obj.time_coverage

        intervals = []
        interval_start, interval_end = None, None
        for period in obj.all_periods:
            year = period.date.year
            if not interval_start:
                # First year in the series
                interval_start, interval_end = year, year
            elif year - interval_end > 1:
                # We skipped a year, add a new interval
                intervals.append(self._get_interval(interval_start, interval_end))
                interval_start, interval_end = year, year
            else:
                # Current interval continues
                interval_end = year

        if interval_start and interval_end:
            intervals.append(self._get_interval(interval_start, interval_end))

        return ", ".join(intervals)
