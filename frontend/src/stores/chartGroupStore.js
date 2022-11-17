import { defineStore } from "pinia";
import { apiCall } from "@/lib/api";

export default defineStore("dataset", {
  state: () => {
    return {
      chartGroups: [],
    };
  },
  actions: {
    async getChartGroups() {
      this.chartGroups = await apiCall("GET", "/chart-groups/");
    },
  },
});
