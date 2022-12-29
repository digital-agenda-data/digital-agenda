import { defineStore } from "pinia";

/**
 * Syncs route to store, making current route usable outside of
 * components.
 */
export const useRoute = defineStore("route", {
  getters: {
    name() {
      return this.$route.name;
    },
    params() {
      return this.$route.params;
    },
    query() {
      return this.$route.query;
    },
  },
});
