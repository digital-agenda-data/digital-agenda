import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";
import { defineStore } from "pinia";

export const useAppSettings = defineStore("appSettings", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/app-settings/").then((r) => r.data),
        {}
      ),
    };
  },
  getters: {
    appSettings() {
      return this.state;
    },
  },
});
