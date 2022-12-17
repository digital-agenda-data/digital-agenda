import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";
import { groupByUnique } from "@/lib/utils";

export const useCountryStore = defineStore("country", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/countries/").then((r) => r.data),
        []
      ),
    };
  },
  getters: {
    countryList() {
      return this.state;
    },
    countryByCode() {
      return groupByUnique(this.countryList);
    },
  },
});
