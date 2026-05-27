from django.urls import include, path
from rest_framework import routers

from .views import ChartGroupIndicatorSearchViewSet, ChartGroupViewSet, ChartViewSet

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
