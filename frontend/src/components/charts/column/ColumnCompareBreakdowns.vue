<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import CountryMultiFilter from "@/components/chart-filters/CountryMultiFilter.vue";
import BreakdownGroupFilter from "@/components/chart-filters/BreakdownGroupFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import IndicatorFilter from "@/components/chart-filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/chart-filters/IndicatorGroupFilter.vue";
import BreakdownMultiFilter from "@/components/chart-filters/BreakdownMultiFilter.vue";
import { colorForCountry, forceArray, sortNumeric } from "@/lib/utils";

export default {
  name: "ColumnCompareBreakdowns",
  extends: BaseChart,
  computed: {
    chartType() {
      return "column";
    },
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownGroupFilter,
        {
          component: BreakdownMultiFilter,
          attrs: { allInitial: true, hidden: true, syncRoute: false },
        },
        PeriodFilter,
        UnitFilter,
        CountryMultiFilter,
      ];
    },
    endpointFilters() {
      return ["breakdownGroup", "period", "indicator", "unit"];
    },
    groupBy() {
      return ["breakdown", "country"];
    },
    breakdownList() {
      return forceArray(this.breakdown);
    },
    totalsByCountry() {
      const result = {};

      for (const country of this.countries) {
        result[country.code] = this.breakdownList
          .map(
            (breakdown) =>
              this.apiValuesGrouped[breakdown.code]?.[country.code] ?? 0
          )
          .reduce((a, b) => a + b, 0);
      }
      return result;
    },
    sortedCountries() {
      return sortNumeric(this.countries, {
        reverse: true,
        keyFunc: (country) => this.totalsByCountry[country.code],
      });
    },
    series() {
      return this.breakdownList.map((breakdown, seriesIndex) => {
        return {
          name: this.getDisplay(breakdown),
          data: this.sortedCountries.map((country) => {
            const weight = this.getWeight(breakdown);
            const fact = this.apiDataGrouped[breakdown.code]?.[country.code];

            return {
              fact,
              y: fact?.value * weight || 0,
              name: this.getDisplay(country),
              color: colorForCountry(country, seriesIndex),
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        legend: {
          enabled: this.breakdownList.length > 1,
        },
        xAxis: {
          type: "category",
        },
      };
    },
  },
  methods: {
    getWeight() {
      return 1;
    },
  },
};
</script>
