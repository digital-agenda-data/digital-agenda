<script>
import BaseSelectFilter from "@/components/filters/base/BaseSelectFilter.vue";

export default {
  name: "UnitFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "unit";
    },
    endpoint() {
      return (
        this.filterStore.indicator &&
        `/indicators/${this.filterStore.indicator.code}/units/`
      );
    },
    label() {
      return "Unit of measure";
    },
  },
};
</script>
