<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import CountryMultiFilter from "@/components/filters/CountryMultiFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import BreakdownMultiFilter from "@/components/filters/BreakdownMultiFilter.vue";
import { colorForCountry } from "@/lib/utils";

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
      return this.breakdown || [];
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
      return Array.from(this.countries).sort((country1, country2) => {
        return (
          this.totalsByCountry[country2.code] -
          this.totalsByCountry[country1.code]
        );
      });
    },
    series() {
      return this.breakdownList.map((breakdown, seriesIndex) => {
        return {
          name: this.getDisplay(breakdown),
          data: this.sortedCountries.map((country) => {
            const apiValue =
              this.apiValuesGrouped[breakdown.code]?.[country.code];

            const weight = this.getWeight(breakdown);

            return {
              apiValue,
              y: apiValue * weight || 0,
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
