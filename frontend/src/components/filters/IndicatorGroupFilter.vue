<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";

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
    isVisible() {
      // Only show this filter if there are more than one indicator group
      return this.loading || this.items.length > 1;
    },
  },
};
</script>
