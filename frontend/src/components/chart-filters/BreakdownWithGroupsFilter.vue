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
      return "/breakdowns/";
    },
    groupEndpoint() {
      return "/breakdown-groups/";
    },
    endpointParams() {
      return {
        indicator: this.filterStore.indicator?.code,
      };
    },
    defaultSingleValue() {
      // Default to the first item, as that will likely be the "total"
      return this.items[0]?.children[0]?.id;
    },
  },
};
</script>
