from django.urls import path, include
from rest_framework import routers

from .views import ChartViewSet
from .views import ChartGroupViewSet
from .views import ChartGroupIndicatorSearchViewSet

router = routers.DefaultRouter()
router.register("charts", ChartViewSet, basename="charts")
router.register("chart-groups", ChartGroupViewSet, basename="chart-groups")
router.register(
    "chart-groups-indicator-search",
    ChartGroupIndicatorSearchViewSet,
    basename="chart-groups-indicator-search",
)


urlpatterns = [
    path("", include(router.urls)),
]
