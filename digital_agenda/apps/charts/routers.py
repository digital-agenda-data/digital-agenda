from rest_framework_nested import routers

from .views import ChartViewSet
from .views import ChartGroupViewSet


router = routers.SimpleRouter()
router.register("charts", ChartViewSet, basename="charts")
router.register("chart-groups", ChartGroupViewSet, basename="chart-groups")
