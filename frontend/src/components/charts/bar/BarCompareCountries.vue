<script>
import ColumnCompareCountries from "@/components/charts/column/ColumnCompareCountries.vue";

export default {
  name: "BarCompareCountries",
  extends: ColumnCompareCountries,
  computed: {
    chartType() {
      return "bar";
    },
  },
};
</script>
