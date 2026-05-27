from django.db.models import Value
from django.db.models.functions import Coalesce, NullIf
from django_filters import rest_framework as filters
from rest_framework import viewsets

from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.serializers import CountrySerializer
from digital_agenda.apps.core.views import DimensionViewSetMixin, ExistingFactFilterSet


class CountryViewSet(DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet):
    model = Country
    serializer_class = CountrySerializer
    queryset = Country.objects.all().order_by(
        Coalesce(
            NullIf("alt_label", Value("")),
            NullIf("label", Value("")),
            "code",
        )
    )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
