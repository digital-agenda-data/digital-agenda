import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";

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
      const result = new Map();
      for (const country of this.countryList) {
        result.set(country.code, country);
      }
      return result;
    },
  },
});
