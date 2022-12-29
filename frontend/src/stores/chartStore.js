import { defineStore } from "pinia";

import { api } from "@/lib/api";
import { FILTERS, placeholderImageURL } from "@/lib/constants";
import {
  camelToSnakeCase,
  groupBy,
  groupByUnique,
  htmlToText,
} from "@/lib/utils";
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
    };
  },
  getters: {
    chartList() {
      return this.state;
    },
    chartByCode() {
      return groupByUnique(this.chartList);
    },
    currentChartCode() {
      return this.$route.params?.chartCode;
    },
    currentChart() {
      return this.chartByCode.get(this.currentChartCode) ?? {};
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
          title: chart.name,
          image:
            chart.image ||
            chartDefaultImages[chart.chart_type] ||
            placeholderImageURL,
          description: chart.description,
          plaintextDescription: htmlToText(chart.description),
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
    chartsPerGroup() {
      return groupBy(this.chartList, "chart_group");
    },
    defaultChartForGroup() {
      const result = {};

      for (const chartGroupCode in this.chartsPerGroup) {
        // Assume the first chart that has the indicator filter available
        // is the one we want to display as a link in the search results:
        result[chartGroupCode] = this.chartsPerGroup[chartGroupCode].find(
          (chart) => !chart.indicator_filter_hidden
        );
      }

      return result;
    },
  },
});
