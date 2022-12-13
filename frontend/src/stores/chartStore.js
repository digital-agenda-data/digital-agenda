import { defineStore } from "pinia";
import { useRouteParams } from "@vueuse/router";

import { api } from "@/lib/api";
import { FILTERS } from "@/lib/constants";
import { camelToSnakeCase } from "@/lib/utils";

export const useChartStore = defineStore("chart", {
  state: () => {
    return {
      charts: [],
      currentChartCode: useRouteParams("chartCode"),
    };
  },
  getters: {
    currentChart(state) {
      return (
        state.charts.find((item) => item.code === this.currentChartCode) || {}
      );
    },
    currentFilterOptions() {
      const result = {};

      for (const key of ["hidden", "defaults", "ignored"]) {
        result[key] = {};

        for (const filterName of FILTERS) {
          result[key][filterName] =
            this.currentChart?.[
              camelToSnakeCase(filterName) + "_filter_" + key
            ];
        }
      }
      return result;
    },
  },
  actions: {
    async getCharts() {
      this.charts = (await api.get("/charts/")).data;
    },
  },
});
