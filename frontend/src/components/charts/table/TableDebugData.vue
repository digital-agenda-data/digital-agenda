<template>
  <ecl-spinner v-if="loading" size="large" centered class="ecl-u-pa-2xl" />
  <table v-else>
    <thead>
      <tr>
        <th>Country</th>
        <th>{{ unit.display }}</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="item in apiData" :key="item.country">
        <td>{{ countryByCode.get(item.country)?.display }}</td>
        <td>{{ item.value }}</td>
      </tr>
      <tr v-if="apiData.length === 0">
        <td colspan="2">No data</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import IndicatorGroupFilter from "@/components/chart-filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/chart-filters/IndicatorFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import BreakdownGroupFilter from "@/components/chart-filters/BreakdownGroupFilter.vue";
import BreakdownFilter from "@/components/chart-filters/BreakdownFilter.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";

export default {
  name: "TableDebugData",
  components: { EclSpinner },
  extends: BaseChart,
  computed: {
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownGroupFilter,
        BreakdownFilter,
        PeriodFilter,
        UnitFilter,
      ];
    },
    endpointFilters() {
      return ["breakdown", "period", "indicator", "unit"];
    },
  },
};
</script>
