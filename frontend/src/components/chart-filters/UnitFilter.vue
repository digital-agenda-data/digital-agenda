<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";

export default {
  name: "UnitFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "unit";
    },
    endpoint() {
      return "/units/";
    },
    endpointParams() {
      return {
        indicator: this.filterStore.indicator?.code,
      };
    },
  },
};
</script>
