<script>
import ScatterCompareTwoIndicators from "@/components/charts/scatter/ScatterCompareTwoIndicators.vue";
import EclHeading from "@/components/ecl/EclHeading.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";

export default {
  name: "BubbleCompareThreeIndicators",
  extends: ScatterCompareTwoIndicators,
  computed: {
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
    chartType() {
      return "bubble";
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
