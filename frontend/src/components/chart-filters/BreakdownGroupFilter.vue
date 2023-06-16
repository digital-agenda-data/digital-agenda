<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";

export default {
  name: "BreakdownGroupFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "breakdownGroup";
    },
    endpoint() {
      return "/breakdown-groups/";
    },
    defaultSingleValue() {
      // Default to the first item, as that will likely be the "total"
      return this.items[0]?.id;
    },
  },
};
</script>
