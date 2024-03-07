<script>
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import ScatterCompareTwoIndicators from "@/components/charts/scatter/ScatterCompareTwoIndicators.vue";
import EclHeading from "@/components/ecl/EclHeading.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import {
  getBreakdownLabel,
  getIndicatorLabel,
  getPeriodLabel,
  getUnitLabel,
} from "@/lib/utils";

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
        { component: IndicatorWithGroupsFilter, attrs: { size: "l" } },
        { component: BreakdownWithGroupsFilter, attrs: { size: "l" } },
        { component: UnitFilter, attrs: { size: "l" } },
        { component: PeriodFilter, attrs: { size: "l" } },
      ];
    },
    endpointFilters() {
      return {
        X: ["indicatorX", "breakdownX", "unitX", "periodX"],
        Y: ["indicatorY", "breakdownY", "unitY", "periodY"],
        Z: ["indicatorZ", "breakdownZ", "unitZ", "periodZ"],
      };
    },
    groupBy() {
      return ["country", "axis"];
    },
    chartSubtitle() {
      return (
        "Size of bubble (Z): " +
        this.joinStrings([
          getIndicatorLabel(this.filterStore.indicatorZ, "label"),
          getBreakdownLabel(this.filterStore.breakdownZ, "label"),
          getUnitLabel(this.filterStore.unitZ, "label"),
          getPeriodLabel(this.filterStore.periodZ, "label"),
        ])
      );
    },
  },
};
</script>
