<script>
import ColumnStackedCompareBreakdowns from "@/components/charts/column/ColumnStackedCompareBreakdowns.vue";

export default {
  name: "BarStackedCompareBreakdowns",
  extends: ColumnStackedCompareBreakdowns,
  computed: {
    chartType() {
      return "bar";
    },
  },
};
</script>
