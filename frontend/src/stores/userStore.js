import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";

async function getCurrentUser() {
  try {
    return (await api.get("/auth/user/")).data;
  } catch (e) {
    switch (e.response?.status) {
      case 403:
      case 401:
        // Anonymous user
        break;
      default:
        console.error("Unexpected error from the API", e);
        throw e;
    }
  }
}

export const useUserStore = defineStore("user", {
  state: () => {
    return {
      ...useAsyncState(getCurrentUser(), null),
    };
  },
  getters: {
    user() {
      return this.state;
    },
  },
});
