import { defineStore } from "pinia";

const FILTER_KEYS = [
  "indicatorGroup",
  "indicator",
  "breakdownGroup",
  "breakdown",
  "period",
  "unit",
  "country",
];

function getInit() {
  return Object.fromEntries(FILTER_KEYS.map((key) => [key, null]));
}

function makeGetters() {
  const result = {};

  for (const suffix of ["", "X", "Y"]) {
    for (const key of FILTER_KEYS) {
      result[key + suffix] = function (state) {
        return state[suffix][key];
      };
    }
  }

  return result;
}

export const useFilterStore = defineStore("filter", {
  state: () => {
    return {
      "": getInit(),
      X: getInit(),
      Y: getInit(),
      Z: getInit(),
    };
  },
  getters: { ...makeGetters() },
});
