<script>
import ColumnCompareBreakdowns from "@/components/charts/column/ColumnCompareBreakdowns.vue";
import BreakdownGroupFilter from "@/components/chart-filters/BreakdownGroupFilter.vue";
import BreakdownMultiFilter from "@/components/chart-filters/BreakdownMultiFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";

export default {
  name: "ColumnStackedCompareBreakdowns",
  extends: ColumnCompareBreakdowns,
  computed: {
    filterComponents() {
      return [
        IndicatorWithGroupsFilter,
        BreakdownGroupFilter,
        {
          component: BreakdownMultiFilter,
          attrs: { allInitial: true, hidden: true, syncRoute: false },
        },
        PeriodFilter,
        UnitFilter,
        {
          component: CountryFilter,
          attrs: { allInitial: true, hidden: true, syncRoute: false },
        },
      ];
    },
    chartOptions() {
      return {
        legend: {
          enabled: this.breakdownList.length > 1,
        },
        xAxis: {
          type: "category",
        },
        plotOptions: {
          [this.chartType]: {
            stacking: "normal",
          },
        },
      };
    },
  },
};
</script>
