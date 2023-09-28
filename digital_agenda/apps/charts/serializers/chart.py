import math

from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.core.serializers import BaseDimensionSerializer
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


class ChartIndicatorListSerializer(BaseDimensionSerializer):
    data_sources = serializers.SlugRelatedField(
        slug_field="code", read_only=True, many=True
    )
    time_coverage = serializers.SerializerMethodField(read_only=True)

    class Meta(IndicatorListSerializer.Meta):
        fields = BaseDimensionSerializer.Meta.fields + [
            "data_sources",
            "note",
            "definition",
            "note",
            "time_coverage",
        ]

    def _get_interval(self, start, end):
        if start == end:
            return str(start)

        return f"{start}-{end}"

    def get_time_coverage(self, obj):
        if obj.time_coverage:
            return obj.time_coverage

        start = obj.period_start or -math.inf
        end = obj.period_end or math.inf
        all_years = {
            period.year for period in obj.all_periods if (start <= period.year <= end)
        }

        intervals = []
        interval_start, interval_end = None, None
        for year in sorted(all_years):
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
