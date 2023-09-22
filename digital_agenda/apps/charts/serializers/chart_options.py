from rest_framework import serializers

from digital_agenda.apps.charts.models import BreakdownChartOption
from digital_agenda.apps.charts.models import IndicatorChartOption


class BaseChartOptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["color", "dash_style", "symbol"]


class IndicatorChartOptionSerializer(BaseChartOptionSerializer):
    class Meta:
        model = IndicatorChartOption
        fields = BaseChartOptionSerializer.Meta.fields


class BreakdownChartOptionSerializer(BaseChartOptionSerializer):
    class Meta:
        model = BreakdownChartOption
        fields = BaseChartOptionSerializer.Meta.fields
