<script>
import ColumnStackedCompareBreakdownsWeighted from "@/components/charts/column/ColumnStackedCompareBreakdownsWeighted.vue";

export default {
  name: "BarStackedCompareBreakdownsWeighted",
  extends: ColumnStackedCompareBreakdownsWeighted,
  computed: {
    chartType() {
      return "bar";
    },
  },
};
</script>
