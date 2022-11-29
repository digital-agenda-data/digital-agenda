<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";

export default {
  name: "BreakdownFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "breakdown";
    },
    endpoint() {
      return (
        this.filterStore.indicator &&
        this.filterStore.breakdownGroup &&
        `/indicators/${this.filterStore.indicator.code}/breakdown-groups/${this.filterStore.breakdownGroup.code}/breakdowns/`
      );
    },
    label() {
      return "Breakdown";
    },
  },
};
</script>
