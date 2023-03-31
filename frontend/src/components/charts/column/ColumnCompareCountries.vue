<script>
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import BaseChart from "@/components/charts/base/BaseChart.vue";
import CountryMultiFilter from "@/components/chart-filters/CountryMultiFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import { colorForCountry, sortNumeric } from "@/lib/utils";

export default {
  name: "ColumnCompareCountries",
  extends: BaseChart,
  computed: {
    chartType() {
      return "column";
    },
    filterComponents() {
      return [
        IndicatorWithGroupsFilter,
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
    sortedCountries() {
      return sortNumeric(this.countries, {
        reverse: true,
        keyFunc: (country) => this.apiValuesGrouped[country.code] ?? 0,
      });
    },
    series() {
      return [
        {
          data: this.sortedCountries.map((country) => {
            const fact = this.apiDataGrouped[country.code];

            return {
              fact,
              y: fact?.value || 0,
              name: country.display,
              color: colorForCountry(country),
            };
          }),
        },
      ];
    },
    chartOptions() {
      return {
        xAxis: {
          type: "category",
        },
      };
    },
  },
};
</script>
