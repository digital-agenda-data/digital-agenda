import logging

import requests
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from rest_framework import serializers

from .models import (
    IndicatorGroup,
    Indicator,
    DataSource,
    BreakdownGroup,
    Breakdown,
    Unit,
    Country,
    Period,
    Fact,
)
from .models import StaticPage
from ..charts.serializers.chart_options import BreakdownChartOptionSerializer
from ..charts.serializers.chart_options import ExtraChartNoteSerializer
from ..charts.serializers.chart_options import IndicatorChartOptionSerializer

logger = logging.getLogger(__name__)

########################
# Dimensions serializers
########################


class BaseDimensionSerializer(serializers.ModelSerializer):
    code = serializers.CharField(label="Code")
    label = serializers.CharField(label="Label")
    alt_label = serializers.CharField(label="Alt. label")
    definition = serializers.CharField(label="Definition")
    display = serializers.SerializerMethodField(label="Display", read_only=True)

    class Meta:
        fields = ["code", "label", "alt_label", "definition", "display"]

    def get_display(self, obj):
        """A suitable display string for this dimension"""
        return obj.alt_label or obj.label or obj.code


class BreakdownSerializer(BaseDimensionSerializer):
    chart_options = BreakdownChartOptionSerializer(many=False, read_only=True)

    class Meta(BaseDimensionSerializer.Meta):
        model = Breakdown
        fields = BaseDimensionSerializer.Meta.fields + ["chart_options"]


class UnitSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Unit


class CountrySerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Country
        fields = BaseDimensionSerializer.Meta.fields + ["color", "is_group"]


class PeriodSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = Period
        fields = BaseDimensionSerializer.Meta.fields + ["date"]


class DataSourceSerializer(BaseDimensionSerializer):
    class Meta(BaseDimensionSerializer.Meta):
        model = DataSource
        fields = BaseDimensionSerializer.Meta.fields + ["note", "url"]


class IndicatorListSerializer(BaseDimensionSerializer):
    data_sources = serializers.SlugRelatedField(
        slug_field="code", read_only=True, many=True
    )
    chart_options = IndicatorChartOptionSerializer(many=False, read_only=True)
    extra_notes = ExtraChartNoteSerializer(many=True, read_only=True)

    class Meta(BaseDimensionSerializer.Meta):
        model = Indicator
        fields = BaseDimensionSerializer.Meta.fields + [
            "data_sources",
            "note",
            "chart_options",
            "extra_notes",
        ]


class IndicatorGroupSerializer(BaseDimensionSerializer):
    members = serializers.SlugRelatedField(
        source="indicators", slug_field="code", many=True, read_only=True
    )

    class Meta(BaseDimensionSerializer.Meta):
        model = IndicatorGroup
        fields = BaseDimensionSerializer.Meta.fields + ["members"]


class BreakdownGroupSerializer(BaseDimensionSerializer):
    members = serializers.SlugRelatedField(
        source="breakdowns", slug_field="code", many=True, read_only=True
    )

    class Meta(BaseDimensionSerializer.Meta):
        model = BreakdownGroup
        fields = BaseDimensionSerializer.Meta.fields + ["members"]


###################
# Facts serializers
###################


class FactSerializer(serializers.ModelSerializer):
    period = serializers.CharField(source="period.code", read_only=True)
    country = serializers.CharField(source="country.code", read_only=True)
    indicator = serializers.CharField(source="indicator.code", read_only=True)
    breakdown = serializers.CharField(source="breakdown.code", read_only=True)
    unit = serializers.CharField(source="unit.code", read_only=True)

    class Meta:
        model = Fact
        fields = [
            "period",
            "indicator",
            "breakdown",
            "unit",
            "country",
            "value",
            "flags",
            "reference_period",
            "remarks",
        ]


########################
# Feedback serializers
########################


@deconstructible
class CaptchaValidator:
    """Validate EU Captcha response

    See https://wikis.ec.europa.eu/display/WEBGUIDE/09.+EU+CAPTCHA for details.
    """

    code = "invalid_captcha"

    def __init__(self, code=None):
        if code is not None:
            self.code = code

    def __call__(self, value):
        if missing := {"wt_captcha_sid", "wt_captcha_answer"}.difference(
            set(value.keys())
        ):
            raise ValidationError(
                f"Missing values for: {', '.join(missing)}", code=self.code
            )

        try:
            resp = requests.post(
                f"https://webtools.europa.eu/rest/captcha/verify",
                headers={
                    "Referer": "https://europa.eu/",
                },
                json={
                    "sid": value["wt_captcha_sid"],
                    "answer": value["wt_captcha_answer"],
                },
                timeout=30,
            )
            resp = resp.json()
            logger.debug("Captcha validation response: %s", resp)

            assert resp["status"] == "success", "incorrect answer"
        except (requests.RequestException, AssertionError, TypeError, ValueError) as e:
            logger.debug("Captcha validation failed: %s", e)
            raise ValidationError(f"Unable to verify captcha: {e}", code=self.code)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.code == other.code


class CaptchaField(serializers.JSONField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(CaptchaValidator())


class FeedbackSerializer(serializers.Serializer):
    url = serializers.URLField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=False, allow_blank=True)
    message = serializers.CharField(
        write_only=True, required=True, min_length=10, max_length=10_000
    )
    captcha = CaptchaField(write_only=True, required=True)

    class Meta:
        fields = ["url", "email", "message", "captcha"]


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ["code", "title", "body"]
