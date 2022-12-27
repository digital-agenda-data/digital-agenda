<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";

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
    apiData() {
      let result = this.super(BaseSelectFilter).apiData();

      if (this.currentChartGroup.periods?.length > 0) {
        const allowedPeriods = new Set(this.currentChartGroup.periods);
        result = result.filter((item) => allowedPeriods.has(item.code));
      }

      return result;
    },
    defaultSingleValue() {
      // Default to the latest period instead of a random choice
      return this.items[0]?.id;
    },
  },
};
</script>
