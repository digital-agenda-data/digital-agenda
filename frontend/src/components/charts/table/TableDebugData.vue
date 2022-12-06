<template>
  <div
    v-if="loading"
    class="ecl-u-d-flex ecl-u-justify-content-center ecl-u-pa-2xl"
  >
    <ecl-spinner size="large" />
  </div>
  <table>
    <thead>
      <tr>
        <th>Country</th>
        <th>Value</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="item in apiData" :key="item.country">
        <td>{{ getDisplay(countryByCode.get(item.country)) }}</td>
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
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import BreakdownFilter from "@/components/filters/BreakdownFilter.vue";
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
