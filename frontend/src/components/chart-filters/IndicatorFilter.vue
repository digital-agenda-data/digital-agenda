<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { mapState } from "pinia";

export default {
  name: "IndicatorFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "indicator";
    },
    endpoint() {
      return (
        this.filterStore.indicatorGroup &&
        `/indicator-groups/${this.filterStore.indicatorGroup.code}/indicators/`
      );
    },
    endpointParams() {
      if (this.currentChartGroup.periods?.length > 0) {
        return {
          period_in: this.currentChartGroup.periods.join(","),
        };
      }
      return {};
    },
  },
};
</script>
