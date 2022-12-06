<script>
import BaseSelectFilter from "@/components/filters/base/BaseSelectFilter.vue";

export default {
  name: "IndicatorGroupFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "indicatorGroup";
    },
    endpoint() {
      return (
        this.$route.params.chartGroupCode &&
        `/chart-groups/${this.$route.params.chartGroupCode}/indicator-groups/`
      );
    },
    label() {
      return "Indicator Group";
    },
  },
};
</script>
