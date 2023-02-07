<script>
import BaseSelectWithGroupFilter from "@/components/chart-filters/base/BaseSelectWithGroupFilter.vue";

export default {
  name: "IndicatorFilter",
  extends: BaseSelectWithGroupFilter,
  computed: {
    queryName() {
      return "indicator";
    },
    endpoint() {
      return "/indicators/";
    },
    groupEndpoint() {
      return "/indicator-groups/";
    },
    endpointParams() {
      return {
        chart_group: this.$route.params.chartGroupCode,
      };
    },
  },
};
</script>
