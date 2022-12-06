<script>
import BaseSelectWithGroupFilter from "@/components/filters/base/BaseSelectWithGroupFilter.vue";

export default {
  name: "BreakdownWithGroupsFilter",
  extends: BaseSelectWithGroupFilter,
  data() {
    return {
      groups: [],
    };
  },
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
    label() {
      return "Breakdown";
    },
  },
};
</script>
