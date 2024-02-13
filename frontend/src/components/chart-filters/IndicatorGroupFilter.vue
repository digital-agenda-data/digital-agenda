<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";

export default {
  name: "IndicatorGroupFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "indicatorGroup";
    },
    endpoint() {
      return "/indicator-groups/";
    },
  },
};
</script>
