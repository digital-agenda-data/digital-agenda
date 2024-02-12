import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";
import { groupByUnique } from "@/lib/utils";

export const usePeriodStore = defineStore("period", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/periods/").then((r) => r.data),
        [],
      ),
    };
  },
  getters: {
    periodList() {
      return this.state;
    },
    periodByCode() {
      return groupByUnique(this.periodList);
    },
  },
});
