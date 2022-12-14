import { defineStore } from "pinia";
import { useRouteParams } from "@vueuse/router";

import { api } from "@/lib/api";
import { FILTERS } from "@/lib/constants";
import { camelToSnakeCase } from "@/lib/utils";
import { useAsyncState } from "@vueuse/core";

export const useChartGroupStore = defineStore("chartGroup", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/chart-groups/").then((r) => r.data),
        []
      ),
      currentChartGroupCode: useRouteParams("chartGroupCode"),
    };
  },
  getters: {
    chartGroupList() {
      return this.state;
    },
    currentChartGroup() {
      return (
        this.chartGroupList.find(
          (item) => item.code === this.currentChartGroupCode
        ) ?? {}
      );
    },
    currentLabels() {
      const result = {};
      for (const filterName of FILTERS) {
        result[filterName] =
          this.currentChartGroup?.[camelToSnakeCase(filterName) + "_label"];
      }
      return result;
    },
  },
});
