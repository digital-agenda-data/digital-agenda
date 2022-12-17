<script>
import ColumnStackedCompareBreakdowns from "@/components/charts/column/ColumnStackedCompareBreakdowns.vue";
import IndicatorWithGroupsFilter from "@/components/filters/IndicatorWithGroupsFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import CountryMultiFilter from "@/components/filters/CountryMultiFilter.vue";
import BreakdownWeightsFilter from "@/components/filters/BreakdownWeightsFilter.vue";

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
    weights() {
      const result = {};

      for (const breakdown of this.breakdownList) {
        result[breakdown.code] = parseInt(
          this.$route.query[breakdown.code] ?? 5
        );
      }
      return result;
    },
    totalWeights() {
      return Object.values(this.weights).reduce((a, b) => a + b, 0);
    },
  },
  methods: {
    getWeight(breakdown) {
      // Normalize the weights as a percentage of the total, so
      // we don't change the scale of the chart.
      return this.weights[breakdown.code] / this.totalWeights;
    },
  },
};
</script>

<style scoped></style>
