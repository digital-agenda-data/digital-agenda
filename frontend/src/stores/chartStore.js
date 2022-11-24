import { defineStore } from "pinia";
import { apiCall } from "@/lib/api";
import { useRoute } from "vue-router";

export const useChartStore = defineStore("chart", {
  state: () => {
    return {
      charts: [],
    };
  },
  getters: {
    currentChartCode() {
      return useRoute().params.chartCode;
    },
    currentChart(state) {
      return state.charts.find((item) => item.code === this.currentChartCode);
    },
  },
  actions: {
    async getCharts() {
      this.charts = await apiCall("GET", "/charts/");
    },
  },
});
