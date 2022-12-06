<script>
import BaseSelectFilter from "@/components/filters/base/BaseSelectFilter.vue";

export default {
  name: "PeriodFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "period";
    },
    endpoint() {
      return (
        this.filterStore.indicator &&
        `/indicators/${this.filterStore.indicator.code}/periods/`
      );
    },
    label() {
      return "Period";
    },
    defaultSingleValue() {
      // Default to the latest period instead of a random choice
      return this.items[0]?.id;
    },
  },
};
</script>
