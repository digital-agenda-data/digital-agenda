import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";
import { groupByUnique } from "@/lib/utils";

export const useDataSourceStore = defineStore("dataSource", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/data-sources/").then((r) => r.data),
        [],
      ),
    };
  },
  getters: {
    dataSourceList() {
      return this.state;
    },
    dataSourceByCode() {
      return groupByUnique(this.dataSourceList);
    },
  },
});
