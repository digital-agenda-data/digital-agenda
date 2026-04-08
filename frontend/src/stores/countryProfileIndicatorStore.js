import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";

export const useCountryProfileIndicatorStore = defineStore(
  "countryProfileIndicator",
  {
    state: () => {
      return {
        ...useAsyncState(
          api.get("/country-profile-indicators/").then((r) => r.data),
          [],
        ),
      };
    },
    getters: {
      countryProfileIndicatorList() {
        return this.state;
      },
    },
  },
);
