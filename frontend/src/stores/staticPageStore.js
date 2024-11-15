import { defineStore } from "pinia";
import { api } from "@/lib/api";
import { useAsyncState } from "@vueuse/core";
import { groupByUnique } from "@/lib/utils";

export const useStaticPageStore = defineStore("staticPage", {
  state: () => {
    return {
      ...useAsyncState(
        api.get("/static-pages/").then((r) => r.data),
        [],
        { immediate: false },
      ),
    };
  },
  getters: {
    staticPageList() {
      return this.state;
    },
    staticPageByCode() {
      return groupByUnique(this.staticPageList);
    },
    currentStaticPageCode() {
      return this.$route.params?.staticPageCode;
    },
    currentStaticPage() {
      return this.staticPageByCode.get(this.currentStaticPageCode) ?? {};
    },
  },
});
