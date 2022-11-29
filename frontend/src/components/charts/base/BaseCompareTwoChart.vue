<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";

export default {
  name: "BaseCompareTwoChart",
  extends: BaseChart,
  computed: {
    filterXComponents() {
      return [];
    },
    filterYComponents() {
      return [];
    },
    normalizedComponents() {
      return [
        ...this.filterXComponents.map((item) =>
          this.normalizeComponent(item, "X", "chart-filter-X")
        ),
        ...this.filterYComponents.map((item) =>
          this.normalizeComponent(item, "Y", "chart-filter-Y")
        ),
        ...this.filterComponents.map((item) =>
          this.normalizeComponent(item, "", "chart-filter-both")
        ),
      ];
    },
    defineEntries() {
      // Set the breakdowns to define them in the "Definitions and scopes"
      return {
        "(X) Indicator": this.filterStore.indicatorX,
        "(X) Breakdown": this.filterStore.breakdownX,
        "(X) Unit": this.filterStore.unitX,
        "(Y) Indicator": this.filterStore.indicatorY,
        "(Y) Breakdown": this.filterStore.breakdownY,
        "(Y) Unit": this.filterStore.unitY,
      };
    },
  },
};
</script>
