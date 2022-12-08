<script>
import ColumnCompareBreakdowns from "@/components/charts/column/ColumnCompareBreakdowns.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import BreakdownMultiFilter from "@/components/filters/BreakdownMultiFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import CountryMultiFilter from "@/components/filters/CountryMultiFilter.vue";
import IndicatorWithGroupsFilter from "@/components/filters/IndicatorWithGroupsFilter.vue";

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
          component: CountryMultiFilter,
          attrs: { allInitial: true, hidden: true, syncRoute: false },
        },
      ];
    },
    chartOptions() {
      return {
        legend: {
          enabled: (this.breakdown || []).length > 1,
        },
        xAxis: {
          type: "category",
        },
        plotOptions: {
          column: {
            stacking: "normal",
          },
        },
      };
    },
  },
};
</script>
