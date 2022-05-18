from rest_framework_nested import routers

from .views import (
    IndicatorGroupViewSet,
    IndicatorViewSet,
    BreakdownGroupViewSet,
    BreakdownViewSet,
    UnitViewSet,
    CountryViewSet,
    PeriodViewSet,
    FactsPerCountryViewSet,
)


indicator_groups_router = routers.SimpleRouter()
indicator_groups_router.register(
    "indicator-groups", IndicatorGroupViewSet, basename="indicator-group"
)


indicators_router = routers.SimpleRouter()
indicators_router.register("indicators", IndicatorViewSet, basename="indicator")


breakdown_groups_router = routers.SimpleRouter()
breakdown_groups_router.register(
    "breakdown-groups", BreakdownGroupViewSet, basename="breakdown-group"
)


breakdowns_router = routers.SimpleRouter()
breakdowns_router.register("breakdowns", BreakdownViewSet, basename="breakdown")


units_router = routers.SimpleRouter()
units_router.register("units", UnitViewSet, basename="unit")


countries_router = routers.NestedSimpleRouter(
    indicators_router, "indicators", lookup="indicator"
)
countries_router.register("countries", CountryViewSet, basename="indicator-countries")


periods_router = routers.SimpleRouter()
periods_router.register("periods", PeriodViewSet, basename="period")


# Fact routers
facts_per_country_router = routers.SimpleRouter()
facts_per_country_router.register(
    "facts/facts-per-country", FactsPerCountryViewSet, basename="fact-per-country"
)

main_routers = [
    indicator_groups_router,
    indicators_router,
    breakdown_groups_router,
    breakdowns_router,
    units_router,
    periods_router,
    facts_per_country_router,
]

nested_routers = [
    countries_router,
]
