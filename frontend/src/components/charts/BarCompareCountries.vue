<template>
  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m chart-filters"
  >
    <indicator-group-filter @change="indicatorGroup = $event" />
    <indicator-filter @change="indicator = $event" />
    <breakdown-group-filter @change="breakdownGroup = $event" />
    <breakdown-filter @change="breakdown = $event" />
    <period-filter @change="period = $event" />
    <unit-filter @change="unit = $event" />
  </div>
  <hr />
  <br />

  <pre>
$route: {{ $route.query }}

indicatorGroup: {{ indicatorGroup }}

indicator: {{ indicator }}

period: {{ period }}

unit: {{ unit }}

breakdownGroup: {{ breakdownGroup }}

breakdown: {{ breakdown }}

  </pre>
</template>

<script>
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import BreakdownFilter from "@/components/filters/BreakdownFilter.vue";

export default {
  name: "BarCompareCountries",
  components: {
    BreakdownFilter,
    BreakdownGroupFilter,
    UnitFilter,
    PeriodFilter,
    IndicatorFilter,
    IndicatorGroupFilter,
  },
  data() {
    return {
      indicatorGroup: null,
      indicator: null,
      period: null,
      unit: null,
      breakdownGroup: null,
      breakdown: null,
    };
  },
};
</script>

<style scoped>
.chart-filters {
  display: grid;
  grid-gap: 1rem 2rem;
  grid-template-columns: 1fr 1fr;
}
</style>
