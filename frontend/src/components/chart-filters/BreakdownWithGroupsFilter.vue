<script>
import BaseSelectWithGroupFilter from "@/components/chart-filters/base/BaseSelectWithGroupFilter.vue";

export default {
  name: "BreakdownWithGroupsFilter",
  extends: BaseSelectWithGroupFilter,
  computed: {
    queryName() {
      return "breakdown";
    },
    endpoint() {
      return (
        this.filterStore.indicator &&
        `/indicators/${this.filterStore.indicator.code}/breakdowns/`
      );
    },
    groupEndpoint() {
      return (
        this.filterStore.indicator &&
        `/indicators/${this.filterStore.indicator.code}/breakdown-groups/`
      );
    },
    defaultSingleValue() {
      // Default to the first item, as that will likely be the "total"
      return this.items[0]?.children[0]?.id;
    },
  },
};
</script>
