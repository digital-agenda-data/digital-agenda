<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";

export default {
  name: "PeriodFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "period";
    },
    endpoint() {
      return (
        this.$route.query.indicator &&
        `/indicators/${this.$route.query.indicator}/periods/`
      );
    },
    label() {
      return "Period";
    },
    defaultValue() {
      // Default to the latest period instead of a random choice
      return this.items[0]?.id;
    },
  },
};
</script>
