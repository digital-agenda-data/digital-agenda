<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";

export default {
  name: "UnitFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "unit";
    },
    endpoint() {
      return (
        this.$route.query.indicator &&
        `/indicators/${this.$route.query.indicator}/units/`
      );
    },
    label() {
      return "Unit of measure";
    },
  },
};
</script>
