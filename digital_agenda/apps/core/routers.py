from rest_framework_nested import routers

from .views.facts import *
from .views.dimensions import *

indicator_groups_router = routers.SimpleRouter()
indicator_groups_router.register(
    "indicator-groups", IndicatorGroupViewSet, basename="indicator-group"
)


group_indicators_router = routers.NestedSimpleRouter(
    indicator_groups_router, "indicator-groups", lookup="indicator_group"
)
group_indicators_router.register(
    "indicators", IndicatorGroupIndicatorViewSet, basename="indicator-group-indicators"
)


indicators_router = routers.SimpleRouter()
indicators_router.register("indicators", IndicatorViewSet, basename="indicator")


breakdown_groups_router = routers.SimpleRouter()
breakdown_groups_router.register(
    "breakdown-groups", BreakdownGroupViewSet, basename="breakdown-group"
)

group_breakdowns_router = routers.NestedSimpleRouter(
    breakdown_groups_router, "breakdown-groups", lookup="breakdown_group"
)
group_breakdowns_router.register(
    "breakdowns", BreakdownGroupBreakdownViewSet, basename="breakdown-group-breakdowns"
)

breakdowns_router = routers.SimpleRouter()
breakdowns_router.register("breakdowns", BreakdownViewSet, basename="breakdown")


units_router = routers.SimpleRouter()
units_router.register("units", UnitViewSet, basename="unit")


indicator_units_router = routers.NestedSimpleRouter(
    indicators_router, "indicators", lookup="indicator"
)
indicator_units_router.register(
    "units", IndicatorUnitViewSet, basename="indicator-units"
)


countries_router = routers.SimpleRouter()
countries_router.register("countries", CountryViewSet, basename="country")


indicator_countries_router = routers.NestedSimpleRouter(
    indicators_router, "indicators", lookup="indicator"
)
indicator_countries_router.register(
    "countries", IndicatorCountryViewSet, basename="indicator-countries"
)


periods_router = routers.SimpleRouter()
periods_router.register("periods", PeriodViewSet, basename="period")


indicator_periods_router = routers.NestedSimpleRouter(
    indicators_router, "indicators", lookup="indicator"
)
indicator_periods_router.register(
    "periods", IndicatorPeriodViewSet, basename="indicator-periods"
)

indicator_breakdowns_router = routers.NestedSimpleRouter(
    indicators_router, "indicators", lookup="indicator"
)
indicator_breakdowns_router.register(
    "breakdowns",
    IndicatorBreakdownViewSet,
    basename="indicator-breakdowns",
)

indicator_breakdowns_groups_router = routers.NestedSimpleRouter(
    indicators_router, "indicators", lookup="indicator"
)
indicator_breakdowns_groups_router.register(
    "breakdown-groups",
    IndicatorBreakdownGroupViewSet,
    basename="indicator-breakdown-groups",
)

indicator_breakdowns_groups_breakdowns_router = routers.NestedSimpleRouter(
    indicator_breakdowns_groups_router, "breakdown-groups", lookup="breakdown_group"
)
indicator_breakdowns_groups_breakdowns_router.register(
    "breakdowns",
    IndicatorBreakdownGroupBreakdownViewSet,
    basename="indicator-breakdowns-groups-breakdowns",
)


data_sources_router = routers.SimpleRouter()
data_sources_router.register("data-sources", DataSourceViewSet, basename="data-source")


# Fact routers
facts_per_country_router = routers.SimpleRouter()
facts_per_country_router.register("facts", FactsViewSet, basename="fact")

main_routers = [
    indicator_groups_router,
    indicators_router,
    breakdown_groups_router,
    breakdowns_router,
    units_router,
    countries_router,
    periods_router,
    data_sources_router,
    facts_per_country_router,
]

nested_routers = [
    group_indicators_router,
    group_breakdowns_router,
    indicator_units_router,
    indicator_countries_router,
    indicator_periods_router,
    indicator_breakdowns_router,
    indicator_breakdowns_groups_router,
    indicator_breakdowns_groups_breakdowns_router,
]
