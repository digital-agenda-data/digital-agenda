<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import CountryMultiFilter from "@/components/filters/CountryMultiFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";
import { colorForCountry } from "@/lib/utils";

export default {
  name: "ColumnCompareCountries",
  extends: BaseChart,
  computed: {
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        PeriodFilter,
        UnitFilter,
        {
          component: CountryMultiFilter,
          attrs: { allInitial: true },
        },
      ];
    },
    endpointFilters() {
      return ["breakdown", "period", "indicator", "unit"];
    },
    groupBy() {
      return ["country"];
    },
    series() {
      return [
        {
          data: this.countries.map((country) => {
            return {
              y: this.apiValuesGrouped[country.code] || 0,
              apiValue: this.apiValuesGrouped[country.code],
              name: this.getDisplay(country),
              color: colorForCountry(country.code),
            };
          }),
          dataSorting: {
            enabled: true,
          },
        },
      ];
    },
    chartOptions() {
      return {
        chart: {
          type: "column",
        },
        xAxis: {
          type: "category",
        },
      };
    },
  },
};
</script>
