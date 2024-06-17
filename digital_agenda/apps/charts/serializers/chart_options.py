from rest_framework import serializers

from digital_agenda.apps.charts.models import BreakdownChartOption
from digital_agenda.apps.charts.models import ExtraChartNote
from digital_agenda.apps.charts.models import IndicatorChartOption


class BaseChartOptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "color",
            "dash_style",
            "line_width",
            "symbol",
            "custom_symbol",
            "marker_enabled",
            "marker_radius",
            "data_labels_enabled",
        ]


class IndicatorChartOptionSerializer(BaseChartOptionSerializer):
    class Meta:
        model = IndicatorChartOption
        fields = BaseChartOptionSerializer.Meta.fields


class BreakdownChartOptionSerializer(BaseChartOptionSerializer):
    class Meta:
        model = BreakdownChartOption
        fields = BaseChartOptionSerializer.Meta.fields


class ExtraChartNoteSerializer(serializers.ModelSerializer):
    indicator = serializers.SlugRelatedField(slug_field="code", read_only=True)
    period = serializers.SlugRelatedField(slug_field="code", read_only=True)

    class Meta:
        model = ExtraChartNote
        fields = ("indicator", "period", "note", "hide_from_line_charts")
