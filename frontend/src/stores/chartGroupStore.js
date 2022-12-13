import { defineStore } from "pinia";
import { useRouteParams } from "@vueuse/router";

import { api } from "@/lib/api";
import { FILTERS } from "@/lib/constants";
import { camelToSnakeCase } from "@/lib/utils";

export const useChartGroupStore = defineStore("chartGroup", {
  state: () => {
    return {
      chartGroups: [],
      currentChartGroupCode: useRouteParams("chartGroupCode"),
    };
  },
  getters: {
    currentChartGroup(state) {
      return state.chartGroups.find(
        (item) => item.code === this.currentChartGroupCode
      );
    },
    currentLabels() {
      const result = {};
      for (const filterName of FILTERS) {
        result[filterName] =
          this.currentChartGroup[camelToSnakeCase(filterName) + "_label"];
      }
      return result;
    },
  },
  actions: {
    async getChartGroups() {
      this.chartGroups = (await api.get("/chart-groups/")).data;
    },
  },
});
