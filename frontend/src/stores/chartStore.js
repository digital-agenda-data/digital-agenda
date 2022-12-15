import { defineStore } from "pinia";
import { useRouteParams } from "@vueuse/router";

import { api } from "@/lib/api";
import { FILTERS, placeholderImageURL } from "@/lib/constants";
import { camelToSnakeCase } from "@/lib/utils";
import { useAsyncState } from "@vueuse/core";
import chartDefaultImages from "@/lib/chartDefaultImages";
import { useChartGroupStore } from "@/stores/chartGroupStore";

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
    chartNavItems() {
      return this.chartList.map((chart) => {
        return {
          id: chart.code,
          code: chart.code,
          title: chart.name,
          image:
            chart.image ||
            chartDefaultImages[chart.chart_type] ||
            placeholderImageURL,
          description: chart.description,
          to: {
            name: "chart-view",
            params: {
              chartGroupCode: chart.chart_group,
              chartCode: chart.code,
            },
          },
          label: chart.is_draft ? { text: "draft", variant: "high" } : null,
          chartGroupCode: chart.chart_group,
        };
      });
    },
    chartNavForCurrentGroup() {
      const code = useChartGroupStore().currentChartGroupCode;

      return this.chartNavItems.filter((item) => item.chartGroupCode === code);
    },
  },
});
