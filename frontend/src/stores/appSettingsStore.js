import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";
import { defineStore } from "pinia";

export const useAppSettings = defineStore("appSettings", {
  state: () => {
    const promise = api.get("/app-settings/").then((r) => r.data);
    return {
      promise,
      ...useAsyncState(promise, {}, { immediate: false }),
    };
  },
  getters: {
    appSettings() {
      return this.state;
    },
  },
});
