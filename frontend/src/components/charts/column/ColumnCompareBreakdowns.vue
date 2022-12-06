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
    series() {
      return (this.breakdown || []).map((breakdown, seriesIndex) => {
        return {
          name: this.getDisplay(breakdown),
          data: this.countries.map((country) => {
            const apiValue =
              this.apiValuesGrouped[breakdown.code] &&
              this.apiValuesGrouped[breakdown.code][country.code];

            return {
              apiValue,
              y: apiValue || 0,
              name: this.getDisplay(country),
              color: colorForCountry(country.code, seriesIndex),
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        chart: {
          type: "column",
        },
        legend: {
          enabled: (this.breakdown || []).length > 1,
        },
        xAxis: {
          type: "category",
        },
      };
    },
  },
};
</script>
