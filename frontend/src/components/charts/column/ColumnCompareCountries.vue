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
    chartType() {
      return "column";
    },
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
    sortedCountries() {
      return Array.from(this.countries).sort(
        (country1, country2) =>
          (this.apiValuesGrouped[country2.code] ?? 0) -
          (this.apiValuesGrouped[country1.code] ?? 0)
      );
    },
    series() {
      return [
        {
          data: this.sortedCountries.map((country) => {
            const fact = this.apiDataGrouped[country.code];

            return {
              fact,
              y: fact?.value || 0,
              name: this.getDisplay(country),
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
