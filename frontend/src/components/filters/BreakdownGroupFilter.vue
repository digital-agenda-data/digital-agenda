<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";

export default {
  name: "BreakdownGroupFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "breakdownGroup";
    },
    endpoint() {
      return (
        this.$route.query.indicator &&
        `/indicators/${this.$route.query.indicator}/breakdown-groups/`
      );
    },
    label() {
      return "Breakdown Group";
    },
  },
};
</script>
