from rest_framework_nested import routers

from .views import ChartViewSet
from .views import ChartGroupViewSet
from .views import ChartGroupIndicatorSearchViewSet


router = routers.SimpleRouter()
router.register("charts", ChartViewSet, basename="charts")
router.register("chart-groups", ChartGroupViewSet, basename="chart-groups")
router.register("chart-groups-indicator-search", ChartGroupIndicatorSearchViewSet, basename="chart-groups-indicator-search")
