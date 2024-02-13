<script>
import BreakdownFilter from "@/components/chart-filters/BreakdownFilter.vue";

export default {
  name: "BreakdownMultiFilter",
  extends: BreakdownFilter,
  computed: {
    queryName() {
      return "breakdown";
    },
    multiple() {
      return true;
    },
  },
};
</script>
