import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";

export const useDataSourceStore = defineStore("dataSource", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/data-sources/").then((r) => r.data),
        []
      ),
    };
  },
  getters: {
    dataSourceList() {
      return this.state;
    },
    dataSourceByCode() {
      const result = new Map();
      for (const item of this.dataSourceList) {
        result.set(item.code, item);
      }
      return result;
    },
  },
});
