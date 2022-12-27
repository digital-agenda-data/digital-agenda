<script>
import BreakdownFilter from "@/components/chart-filters/BreakdownFilter.vue";

export default {
  name: "BreakdownMultiFilter",
  extends: BreakdownFilter,
  computed: {
    multiple() {
      return true;
    },
  },
};
</script>
