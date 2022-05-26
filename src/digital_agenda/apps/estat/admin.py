from django.contrib import admin
from django.db.models.functions import Lower
from django.forms import ModelForm
from django.urls import resolve

from admin_auto_filters.filters import AutocompleteFilter, AutocompleteFilterFactory

from .models import (
    Dataset,
    Dimension,
    DimensionValue,
    DatasetConfig,
    Fact,
)


class DatasetConfigInline(admin.StackedInline):
    model = DatasetConfig
    verbose_name = "Configuration"

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """Filter choices for fields that are FK to Dimension"""
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name in ("indicator", "breakdown", "unit", "country", "period"):
            dataset_id = resolve(request.path_info).kwargs.get("object_id")
            if dataset_id is not None:
                field.queryset = field.queryset.filter(dataset_id=dataset_id)
        if db_field.name in (
            "indicator_surrogate",
            "breakdown_surrogate",
            "unit_surrogate",
            "country_surrogate",
            "period_surrogate",
        ):
            dataset_id = resolve(request.path_info).kwargs.get("object_id")
            if dataset_id is not None:
                field.queryset = field.queryset.filter(
                    dimension__dataset_id=dataset_id,
                    dimension__code=Dimension.SURROGATE_CODE,
                )

        return field


class DatasetAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    inlines = [DatasetConfigInline]
    list_per_page = 30

    def get_ordering(self, request):
        return [Lower("code")]


admin.site.register(Dataset, DatasetAdmin)


class DatasetFilter(AutocompleteFilter):
    title = "Dataset"
    field_name = "dataset"


class DimensionAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "dataset")
    search_fields = ("code", "label")
    list_filter = [DatasetFilter]
    list_per_page = 30


admin.site.register(Dimension, DimensionAdmin)


class DimensionAdminFilter(admin.SimpleListFilter):
    title = "Dimension"
    parameter_name = "dimension"

    def lookups(self, request, model_admin):
        dataset = request.GET.get("dimension__dataset", "")
        if dataset:
            dimensions = Dimension.objects.filter(dataset_id=dataset)
        else:
            dimensions = Dimension.objects.none()

        return dimensions.values_list("id", "code")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(dimension=self.value())

        return queryset


class FilterKwargsMixin:
    """Mixin for extracting kwargs from `_changelist_filters` params."""

    @staticmethod
    def parse_filter_kwargs(**kwargs):
        if "initial" in kwargs:
            if "_changelist_filters" in kwargs["initial"]:
                filters = kwargs["initial"].pop("_changelist_filters")
                for key, value in [p.split("=") for p in filters.split("&")]:
                    kwargs["initial"][key] = value
        return kwargs


class DimensionValueForm(ModelForm, FilterKwargsMixin):
    class Meta:
        model = DimensionValue
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        kwargs = self.parse_filter_kwargs(**kwargs)
        super().__init__(*args, **kwargs)


class DimensionValueAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "enabled", "dimension", "dimension_dataset")
    search_fields = ("code", "label")
    list_filter = [
        AutocompleteFilterFactory("Dataset", "dimension__dataset"),
        DimensionAdminFilter,
    ]
    autocomplete_fields = ("dimension",)
    list_per_page = 30
    actions = ["enable", "disable"]
    form = DimensionValueForm

    def get_ordering(self, request):
        return ["dimension__dataset", Lower("code")]

    @admin.display(description="Dataset")
    def dimension_dataset(self, obj):
        return obj.dimension.dataset.code

    @admin.action(description="Enable selected codes")
    def enable(self, request, queryset):
        queryset.update(enabled=True)

    @admin.action(description="Disable selected codes")
    def disable(self, request, queryset):
        queryset.update(enabled=False)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """Filter choices for dimension"""
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "dimension":
            dimension_id = resolve(request.path_info).kwargs.get("dimension")
            if dimension_id is not None:
                field.queryset = field.queryset.filter(dimension_id=dimension_id)

        return field


admin.site.register(DimensionValue, DimensionValueAdmin)


class FactAdmin(admin.ModelAdmin):
    list_display = (
        "dataset",
        "indicator",
        "breakdown",
        "unit",
        "country",
        "period",
        "value",
        "flags",
    )
    list_per_page = 50
    list_filter = [DatasetFilter]


admin.site.register(Fact, FactAdmin)
