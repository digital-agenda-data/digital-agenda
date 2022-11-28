<script>
import BaseCompareBreakdownChart from "@/components/charts/BaseCompareBreakdownChart.vue";
import CountryMultiFilter from "@/components/filters/CountryMultiFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import { colorForCountry } from "@/lib/utils";

export default {
  name: "ColumnCompareBreakdowns",
  extends: BaseCompareBreakdownChart,
  computed: {
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownGroupFilter,
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
      return this.apiDataBreakdowns.map((breakdown, seriesIndex) => {
        return {
          name: this.getDisplay(breakdown),
          data: this.countries.map((country) => {
            return {
              y: this.apiValuesGrouped[breakdown.code][country.code] || 0,
              apiValue: this.apiValuesGrouped[breakdown.code][country.code],
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
          enabled: this.apiDataBreakdowns.length > 1,
        },
        xAxis: {
          type: "category",
        },
      };
    },
  },
};
</script>
