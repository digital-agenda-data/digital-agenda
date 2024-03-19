import { defineStore } from "pinia";
import { FILTER_SUFFIXES, FILTERS } from "@/lib/constants";

function getInit() {
  const result = Object.fromEntries(FILTERS.map((key) => [key, null]));
  result.loadingCounter = 0;
  return result;
}

/**
 * Create getters for all filters and axis combinations. I.e:
 * indicator, indicatorX, indicatorY and so on.
 */

function makeGetters() {
  const result = {};

  for (const suffix of FILTER_SUFFIXES) {
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
  getters: {
    ...makeGetters(),
    totalLoadingCounter(state) {
      return FILTER_SUFFIXES.map(
        (suffix) => state[suffix].loadingCounter,
      ).reduce((a, b) => a + b, 0);
    },
    allFiltersLoaded() {
      return this.totalLoadingCounter === 0;
    },
    dimensionsByCode(state) {
      const result = {};
      for (const key of FILTERS) {
        result[key] = new Map();
        for (const suffix of FILTER_SUFFIXES) {
          const obj = state[suffix][key];
          if (!obj) continue;

          result[key].set(obj.code, obj);
        }
      }
      return result;
    },
  },
});
