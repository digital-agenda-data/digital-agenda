import { defineStore } from "pinia";
import { useRouteParams } from "@vueuse/router";

import { api } from "@/lib/api";
import { FILTERS } from "@/lib/constants";
import { camelToSnakeCase } from "@/lib/utils";
import { useAsyncState } from "@vueuse/core";

export const useChartStore = defineStore("chart", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/charts/").then((r) => r.data),
        []
      ),
      currentChartCode: useRouteParams("chartCode"),
    };
  },
  getters: {
    chartList() {
      return this.state;
    },
    currentChart() {
      return (
        this.chartList.find((item) => item.code === this.currentChartCode) ?? {}
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
});
