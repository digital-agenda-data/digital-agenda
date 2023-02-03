from django_filters import rest_framework as filters
from django_filters import rest_framework as filters


class CodeLookupMixin:
    lookup_field = "code"
    lookup_url_kwarg = "code"


class CodeInFilter(filters.BaseInFilter, filters.CharFilter):
    pass
