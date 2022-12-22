<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";
import BreakdownMultiFilter from "@/components/filters/BreakdownMultiFilter.vue";

export default {
  name: "SplineCompareBreakdowns",
  extends: BaseChart,
  computed: {
    chartType() {
      return "spline";
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
        UnitFilter,
        CountryFilter,
      ];
    },
    endpointFilters() {
      return ["breakdownGroup", "indicator", "unit", "country"];
    },
    groupBy() {
      return ["breakdown", "period"];
    },
    series() {
      return (this.breakdown || []).map((breakdown) => {
        return {
          name: this.getDisplay(breakdown),
          data: this.apiDataPeriods.map((periodCode) => {
            const fact = this.apiDataGrouped[breakdown.code]?.[periodCode];

            return {
              fact,
              y: fact?.value || null,
              x: parseInt(periodCode),
              name: periodCode,
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        subtitle: {
          text: this.getDisplay(this.country),
        },
        legend: {
          enabled: (this.breakdown || []).length > 1,
        },
        yAxis: {
          min: 0,
        },
        plotOptions: {
          series: {
            connectNulls: true,
            dataLabels: {
              enabled: false,
            },
          },
        },
      };
    },
  },
};
</script>
