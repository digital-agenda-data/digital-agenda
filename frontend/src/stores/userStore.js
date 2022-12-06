import { defineStore } from "pinia";
import { api } from "@/lib/api";

export const useUserStore = defineStore("user", {
  state: () => {
    return {
      email: null,
    };
  },
  actions: {
    async getCurrentUser() {
      try {
        const resp = (await api.get("/auth/user/")).data;
        this.email = resp.email;
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
    },
  },
});
