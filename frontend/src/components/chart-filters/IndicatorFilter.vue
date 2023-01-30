<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";

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
  },
};
</script>
