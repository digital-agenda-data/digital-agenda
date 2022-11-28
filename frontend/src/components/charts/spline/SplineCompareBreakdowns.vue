<script>
import BaseCompareBreakdownChart from "@/components/charts/BaseCompareBreakdownChart.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";

export default {
  name: "SplineCompareBreakdowns",
  extends: BaseCompareBreakdownChart,
  computed: {
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownGroupFilter,
        UnitFilter,
        CountryFilter,
      ];
    },
    initialCountries() {
      // No need to set initial countries since we are always filtering
      // on a single country for this chart
      return [];
    },
    endpointFilters() {
      return ["breakdownGroup", "indicator", "unit", "country"];
    },
    groupBy() {
      return ["breakdown", "period"];
    },
    series() {
      return this.apiDataBreakdowns.map((breakdown) => {
        return {
          name: this.getDisplay(breakdown),
          data: this.apiDataPeriods.map((periodCode) => {
            return {
              y: this.apiValuesGrouped[breakdown.code][periodCode] || 0,
              apiValue: this.apiValuesGrouped[breakdown.code][periodCode],
              x: parseInt(periodCode),
              name: periodCode,
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        chart: {
          type: "spline",
        },
        subtitle: {
          text: this.getDisplay(this.country),
        },
        legend: {
          enabled: this.apiDataBreakdowns.length > 1,
        },
      };
    },
  },
};
</script>
