<script>
import BreakdownFilter from "@/components/filters/BreakdownFilter.vue";

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
