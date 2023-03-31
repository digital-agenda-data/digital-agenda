<script>
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import BaseChart from "@/components/charts/base/BaseChart.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import BreakdownGroupFilter from "@/components/chart-filters/BreakdownGroupFilter.vue";
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import BreakdownMultiFilter from "@/components/chart-filters/BreakdownMultiFilter.vue";

export default {
  name: "SplineCompareBreakdowns",
  extends: BaseChart,
  computed: {
    chartType() {
      return "spline";
    },
    filterComponents() {
      return [
        IndicatorWithGroupsFilter,
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
          name: breakdown.display,
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
          text: this.country?.display,
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
