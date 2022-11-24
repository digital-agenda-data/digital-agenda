import { defineStore } from "pinia";

export const useFilterStore = defineStore("filter", {
  state: () => {
    return {
      indicatorGroup: [],
      indicator: [],
      breakdownGroup: [],
      breakdown: [],
      period: [],
      unit: [],
      country: [],
    };
  },
});
