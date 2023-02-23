<script>
import ColumnCompareBreakdowns from "@/components/charts/column/ColumnCompareBreakdowns.vue";

export default {
  name: "BarCompareBreakdowns",
  extends: ColumnCompareBreakdowns,
  computed: {
    chartType() {
      return "bar";
    },
  },
};
</script>
