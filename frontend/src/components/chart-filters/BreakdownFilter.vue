<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";

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
    defaultSingleValue() {
      // Default to the first item, as that will likely be the "total"
      return this.items[0]?.id;
    },
  },
};
</script>
