<script>
import ColumnStackedCompareBreakdowns from "@/components/charts/column/ColumnStackedCompareBreakdowns.vue";
import IndicatorWithGroupsFilter from "@/components/filters/IndicatorWithGroupsFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import CountryMultiFilter from "@/components/filters/CountryMultiFilter.vue";
import BreakdownWeightsFilter from "@/components/filters/BreakdownWeightsFilter.vue";

// XXX THIS IS NOT COMPLETE
// XXX Still needs the "drill-down" figured out and implemented

export default {
  name: "ColumnStackedCompareBreakdownsWeighted",
  extends: ColumnStackedCompareBreakdowns,
  computed: {
    filterComponents() {
      return [
        {
          component: BreakdownWeightsFilter,
          attrs: {
            allInitial: true,
            syncRoute: false,
            class: ["chart-filter-full"],
          },
        },
        IndicatorWithGroupsFilter,
        BreakdownGroupFilter,
        PeriodFilter,
        UnitFilter,
        {
          component: CountryMultiFilter,
          attrs: { allInitial: true, hidden: true, syncRoute: false },
        },
      ];
    },
  },
  methods: {
    getWeight(breakdown) {
      return parseInt(this.$route.query[breakdown.code] ?? 5);
    },
  },
};
</script>

<style scoped></style>
