<script>
import BaseSelectFilter from "@/components/filters/base/BaseSelectFilter.vue";

export default {
  name: "BreakdownGroupFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "breakdownGroup";
    },
    endpoint() {
      return (
        this.filterStore.indicator &&
        `/indicators/${this.filterStore.indicator.code}/breakdown-groups/`
      );
    },
    label() {
      return "Breakdown Group";
    },
  },
};
</script>
