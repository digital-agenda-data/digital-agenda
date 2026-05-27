from django.urls import include, path
from rest_framework import routers

from .views.breakdown import BreakdownViewSet
from .views.breakdown_group import BreakdownGroupViewSet
from .views.country import CountryViewSet
from .views.country_profile_indicator import CountryProfileIndicatorViewSet
from .views.data_source import DataSourceViewSet
from .views.facts import FactsViewSet
from .views.feedback import FeedbackViewSet
from .views.indicator import IndicatorViewSet
from .views.indicator_group import IndicatorGroupViewSet
from .views.misc import AppSettingsView, StaticPageViewSet
from .views.period import PeriodViewSet
from .views.unit import UnitViewSet

router = routers.DefaultRouter()
router.register("facts", FactsViewSet)
router.register("units", UnitViewSet)
router.register("periods", PeriodViewSet)
router.register("countries", CountryViewSet)
router.register("breakdowns", BreakdownViewSet)
router.register("indicators", IndicatorViewSet)
router.register("data-sources", DataSourceViewSet)
router.register("breakdown-groups", BreakdownGroupViewSet)
router.register("indicator-groups", IndicatorGroupViewSet)
router.register("feedback", FeedbackViewSet, "feedback")
router.register("static-pages", StaticPageViewSet)
router.register(
    "country-profile-indicators",
    CountryProfileIndicatorViewSet,
    basename="country-profile-indicators",
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "app-settings/",
        AppSettingsView.as_view(),
        name="app-settings",
    ),
]
