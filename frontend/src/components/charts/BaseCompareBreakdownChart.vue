<script>
import BaseChart from "@/components/charts/BaseChart.vue";
import { apiCall } from "@/lib/api";

export default {
  name: "BaseCompareBreakdownChart",
  extends: BaseChart,
  data() {
    return {
      breakdownList: [],
    };
  },
  computed: {
    apiDataBreakdowns() {
      const codes = new Set(this.apiData.map((item) => item.breakdown));
      // Preserve the order from the API
      return this.breakdownList.filter((item) => codes.has(item.code));
    },
    defineEntries() {
      // Set the breakdowns to define them in the "Definitions and scopes"
      return {
        Indicator: this.indicator,
        Breakdown: this.apiDataBreakdowns,
        Unit: this.unit,
      };
    },
  },

  methods: {
    async loadExtra() {
      if (!this.breakdownGroup) return;

      this.breakdownList = await apiCall(
        "GET",
        `/breakdown-groups/${this.breakdownGroup.code}/breakdowns/`
      );
    },
  },
};
</script>
