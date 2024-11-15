import { defineStore } from "pinia";

import { api } from "@/lib/api";
import { FILTERS, placeholderImageURL } from "@/lib/constants";
import { camelToSnakeCase, groupByUnique, htmlToText } from "@/lib/utils";
import { useAsyncState } from "@vueuse/core";

export const useChartGroupStore = defineStore("chartGroup", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/chart-groups/").then((r) => r.data),
        [],
        { immediate: false },
      ),
    };
  },
  getters: {
    chartGroupList() {
      return this.state;
    },
    chartGroupByCode() {
      return groupByUnique(this.chartGroupList);
    },
    currentChartGroupCode() {
      return this.$route.params?.chartGroupCode;
    },
    currentChartGroup() {
      return this.chartGroupByCode.get(this.currentChartGroupCode) ?? {};
    },
    currentLabels() {
      const result = {};
      for (const filterName of FILTERS) {
        result[filterName] =
          this.currentChartGroup?.[camelToSnakeCase(filterName) + "_label"];
      }
      return result;
    },
    chartGroupNavItems() {
      return this.chartGroupList.map((chartGroup) => {
        return {
          id: chartGroup.code,
          title: chartGroup.name,
          image: chartGroup.image || placeholderImageURL,
          description: chartGroup.description,
          plaintextDescription: htmlToText(chartGroup.description),
          to: {
            name: "chart-group",
            params: {
              chartGroupCode: chartGroup.code,
            },
          },
          label: chartGroup.is_draft
            ? { text: "draft", variant: "high" }
            : null,
        };
      });
    },
  },
});
