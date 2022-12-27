<script>
import ScatterCompareTwoIndicators from "@/components/charts/scatter/ScatterCompareTwoIndicators.vue";
import EclHeading from "@/components/ecl/EclHeading.vue";
import IndicatorGroupFilter from "@/components/chart-filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/chart-filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";

export default {
  name: "BubbleCompareThreeIndicators",
  extends: ScatterCompareTwoIndicators,
  computed: {
    chartType() {
      return "bubble";
    },
    filterZComponents() {
      return [
        {
          key: "z-heading",
          component: EclHeading,
          attrs: { size: 5, text: "Bubbles size (Z) proportional to:" },
        },
        { component: IndicatorGroupFilter, attrs: { size: "l" } },
        { component: IndicatorFilter, attrs: { size: "l" } },
        { component: BreakdownWithGroupsFilter, attrs: { size: "l" } },
        { component: UnitFilter, attrs: { size: "l" } },
      ];
    },
    endpointFilters() {
      return {
        X: ["indicatorX", "breakdownX", "unitX", "periodX"],
        Y: ["indicatorY", "breakdownY", "unitY", "periodX"],
        Z: ["indicatorZ", "breakdownZ", "unitZ", "periodX"],
      };
    },
    groupBy() {
      return ["country", "axis"];
    },
    chartSubtitle() {
      return (
        "Size of bubble (Z): " +
        this.makeTitle([
          this.filterStore.indicatorZ,
          this.filterStore.breakdownZ,
          this.filterStore.unitZ,
        ])
      );
    },
  },
};
</script>
