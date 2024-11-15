from django.urls import path, include
from rest_framework import routers

from .views.misc import AppSettingsView
from .views.facts import FactsViewSet
from .views.feedback import FeedbackViewSet
from .views.misc import StaticPageViewSet
from .views.unit import UnitViewSet
from .views.period import PeriodViewSet
from .views.country import CountryViewSet
from .views.breakdown import BreakdownViewSet
from .views.indicator import IndicatorViewSet
from .views.data_source import DataSourceViewSet
from .views.breakdown_group import BreakdownGroupViewSet
from .views.indicator_group import IndicatorGroupViewSet

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

urlpatterns = [
    path("", include(router.urls)),
    path(
        "app-settings/",
        AppSettingsView.as_view(),
        name="app-settings",
    ),
]
