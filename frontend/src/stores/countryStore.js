import { defineStore } from "pinia";
import { api } from "@/lib/api";

export const useCountryStore = defineStore("country", {
  state() {
    return {
      countryList: [],
    };
  },
  actions: {
    async getCountryList() {
      this.countryList = (await api.get("/countries/")).data;
    },
  },
  getters: {
    countryByCode(state) {
      const result = new Map();
      for (const country of state.countryList) {
        result.set(country.code, country);
      }
      return result;
    },
  },
});
