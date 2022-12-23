import { defineStore } from "pinia";
import { FILTERS } from "@/lib/constants";

function getInit() {
  return Object.fromEntries(FILTERS.map((key) => [key, null]));
}

/**
 * Create getters for all filters and axis combinations. I.e:
 * indicator, indicatorX, indicatorY and so on.
 */

function makeGetters() {
  const result = {};

  for (const suffix of ["", "X", "Y", "Z"]) {
    for (const key of FILTERS) {
      result[key + suffix] = function (state) {
        return state[suffix][key];
      };
    }
  }

  return result;
}

/**
 * Store selected filter values in this global store. Even though they are
 * also (usually) synced with the route query, this store contains the entire
 * Object from the API instead of only the code.
 *
 * There is no two-way binding here, as changing something in this store will
 * not change the filters or the route!
 */
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
