import { defineStore } from "pinia";
import { apiCall } from "@/lib/api";
import { useRoute } from "vue-router";

export const useChartGroupStore = defineStore("chartGroup", {
  state: () => {
    return {
      chartGroups: [],
    };
  },
  getters: {
    currentChartGroupCode() {
      return useRoute().params.chartGroupCode;
    },
    currentChartGroup(state) {
      return state.chartGroups.find(
        (item) => item.code === this.currentChartGroupCode
      );
    },
  },
  actions: {
    async getChartGroups() {
      this.chartGroups = await apiCall("GET", "/chart-groups/");
    },
  },
});
