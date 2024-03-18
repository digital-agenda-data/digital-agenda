import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";
import { groupByUnique } from "@/lib/utils";

export const usePeriodStore = defineStore("period", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/periods/").then((r) =>
          r.data.map((period) => {
            return {
              ...period,
              date: new Date(period.date),
            };
          }),
        ),
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
