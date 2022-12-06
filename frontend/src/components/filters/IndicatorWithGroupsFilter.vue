<script>
import BaseSelectWithGroupFilter from "@/components/filters/base/BaseSelectWithGroupFilter.vue";

export default {
  name: "IndicatorFilter",
  extends: BaseSelectWithGroupFilter,
  computed: {
    queryName() {
      return "indicator";
    },
    endpoint() {
      return (
        this.$route.params.chartGroupCode &&
        `/chart-groups/${this.$route.params.chartGroupCode}/indicators/`
      );
    },
    groupEndpoint() {
      return (
        this.$route.params.chartGroupCode &&
        `/chart-groups/${this.$route.params.chartGroupCode}/indicator-groups/`
      );
    },
    label() {
      return "Indicator";
    },
  },
};
</script>
