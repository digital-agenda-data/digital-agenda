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
        this.$route.query.indicator &&
        this.$route.query.breakdownGroup &&
        `/indicators/${this.$route.query.indicator}/breakdown-groups/${this.$route.query.breakdownGroup}/breakdowns/`
      );
    },
    label() {
      return "Breakdown";
    },
  },
};
</script>
