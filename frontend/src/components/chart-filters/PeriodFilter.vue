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
      return "/periods/";
    },
    apiData() {
      const periodStart = this.currentChartGroup.period_start ?? -Infinity;
      const periodEnd = this.currentChartGroup.period_end ?? Infinity;

      return this.super(BaseSelectFilter)
        .apiData()
        .filter((item) => periodStart <= parseInt(item.code) <= periodEnd);
    },
    defaultSingleValue() {
      // Default to the latest period instead of a random choice
      return this.items[0]?.id;
    },
  },
};
</script>
