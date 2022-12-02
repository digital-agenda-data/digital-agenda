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
  },
};
</script>
