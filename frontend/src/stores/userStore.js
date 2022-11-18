import { defineStore } from "pinia";
import { apiCall } from "@/lib/api";

export const useUserStore = defineStore("user", {
  state: () => {
    return {
      email: null,
    };
  },
  actions: {
    async getCurrentUser() {
      try {
        const resp = await apiCall("GET", "/auth/user/");
        this.email = resp.email;
      } catch (e) {
        switch (e.statusCode) {
          case 403:
          case 401:
            // Anonymous user
            break;
          default:
            console.error("Unexpected error from the API", e);
            throw e;
        }
      }
    },
  },
});
