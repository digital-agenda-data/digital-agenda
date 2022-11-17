from rest_framework_nested import routers

from .views import ChartGroupViewSet


router = routers.SimpleRouter()
router.register(
    "chart-groups", ChartGroupViewSet, basename="chart-groups"
)
