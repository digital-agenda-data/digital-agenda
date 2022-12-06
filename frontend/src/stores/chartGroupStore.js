import { defineStore } from "pinia";
import { api } from "@/lib/api";
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
    currentLabels() {
      return {
        indicatorGroup: this.currentChartGroup.indicator_group_label,
        indicator: this.currentChartGroup.indicator_label,
        breakdownGroup: this.currentChartGroup.breakdown_group_label,
        breakdown: this.currentChartGroup.breakdown_label,
        period: this.currentChartGroup.period_label,
        unit: this.currentChartGroup.unit_label,
      };
    },
  },
  actions: {
    async getChartGroups() {
      this.chartGroups = (await api.get("/chart-groups/")).data;
    },
  },
});
