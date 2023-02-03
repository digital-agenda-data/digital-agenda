from django import forms
from django.db.models import Subquery
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.serializers import CountryFactSerializer
from digital_agenda.apps.core.views import CodeLookupMixin


def filter_indicator_groups(queryset, name, value):
    return queryset.filter(
        indicator__id__in=Subquery(
            Indicator.objects.filter(groups__code=value).only("id")
        )
    )


def filter_breakdown_groups(queryset, name, value):
    return queryset.filter(
        breakdown__id__in=Subquery(
            Breakdown.objects.filter(groups__code=value).only("id")
        )
    )


class FactsFilter(filters.FilterSet):
    indicator_group = filters.CharFilter(
        field_name="indicator__code", method=filter_indicator_groups
    )
    indicator = filters.CharFilter(field_name="indicator__code")
    breakdown_group = filters.CharFilter(
        field_name="breakdown_code", method=filter_breakdown_groups
    )
    breakdown = filters.CharFilter(field_name="breakdown__code")
    unit = filters.CharFilter(field_name="unit__code", required=True)
    period = filters.CharFilter(field_name="period__code")
    country = filters.CharFilter(field_name="country__code")

    def get_form_class(self):
        # Ensure that at least one indicator and one breakdown filter
        # has been used to avoid accidentally making huge queries.

        def clean_indicator(form):
            data = form.cleaned_data
            if not data["indicator_group"] and not data["indicator"]:
                raise forms.ValidationError(
                    "Either indicator or indicator_group is required"
                )
            return data["indicator"]

        def clean_breakdown(form):
            data = form.cleaned_data
            if not data["breakdown_group"] and not data["breakdown"]:
                raise forms.ValidationError(
                    "Either breakdown or breakdown_group is required"
                )
            return data["breakdown"]

        form_class = super().get_form_class()
        form_class.clean_indicator = clean_indicator
        form_class.clean_breakdown = clean_breakdown

        return form_class

    class Meta:
        model = Fact
        fields = [
            "indicator_group",
            "indicator",
            "breakdown_group",
            "breakdown",
            "unit",
            "period",
            "country",
        ]


class FactsViewSet(CodeLookupMixin, ListModelMixin, viewsets.GenericViewSet):
    model = Fact
    serializer_class = CountryFactSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FactsFilter
    queryset = (
        Fact.objects.order_by(
            "period__code",
            "indicator__code",
            "breakdown__code",
            "unit__code",
            "country__code",
        )
        .select_related("country", "indicator", "breakdown", "period", "unit")
        .only(
            "period__code",
            "indicator__code",
            "breakdown__code",
            "unit__code",
            "country__code",
            "value",
            "flags",
        )
        .all()
    )
    pagination_class = None

    # Likely to have a lot of cache misses, does not seem worth caching.
    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
