import drf_excel.mixins
from django_filters import rest_framework as filters


class CodeLookupMixin:
    lookup_field = "code"
    lookup_url_kwarg = "code"


class CodeInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CustomXLSXFileMixin(drf_excel.mixins.XLSXFileMixin):
    xlsx_use_labels = True
    xlsx_ignore_headers = [
        "is_group",
        "color",
        "groups",
    ]
    column_header = {
        "column_width": 30,
        "style": {
            "fill": {
                "fill_type": "solid",
                "start_color": "f2f5f9",
            },
            "alignment": {
                "horizontal": "left",
                "vertical": "center",
                "wrapText": True,
                "shrink_to_fit": True,
            },
            "border_side": {
                "border_style": "thin",
                "color": "FF000000",
            },
            "font": {
                "name": "Arial",
                "size": 16,
                "bold": True,
                "color": "FF000000",
            },
        },
    }
    body = {
        "style": {
            "alignment": {
                "vertical": "top",
                "wrapText": True,
                "shrink_to_fit": True,
            },
            "border_side": {
                "border_style": "thin",
                "color": "FF000000",
            },
            "font": {
                "name": "Arial",
                "size": 14,
                "bold": False,
                "color": "FF000000",
            },
        },
    }
