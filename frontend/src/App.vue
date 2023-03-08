<template>
  <interactive-chart v-if="isEmbedded && isReady" />
  <main-layout v-else-if="isReady" />
</template>

<script>
import { mapStores } from "pinia";

import { getRouteMeta } from "@/lib/utils";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { defineAsyncComponent } from "vue";

const DEFAULT_TITLE = "Digital Scoreboard - Data & Indicators";

export default {
  name: "App",
  components: {
    // Define async components (instead of regular ones) to avoid loading
    // extra CSS/JS while in embed mode
    MainLayout: defineAsyncComponent(() => import("@/views/MainLayout.vue")),
    InteractiveChart: defineAsyncComponent(() =>
      import("@/components/charts/InteractiveChart.vue")
    ),
  },
  computed: {
    ...mapStores(useChartGroupStore, useChartStore),
    isEmbedded() {
      return new URL(window.location).searchParams.get("embed") === "true";
    },
    isReady() {
      // Only display the app after the chartGroups and the charts
      // have been loaded to avoid layout shifts.
      return this.chartGroupStore.isReady && this.chartStore.isReady;
    },
    pageTitle() {
      return getRouteMeta(this.$route, "title");
    },
    docTitle() {
      return [
        this.isEmbedded ? "(EMBEDDED)" : null,
        this.pageTitle,
        DEFAULT_TITLE,
      ]
        .filter((i) => !!i)
        .join(" - ");
    },
  },
  watch: {
    docTitle() {
      document.title = this.docTitle;
    },
    $route(to, from) {
      if (window._paq && to.path !== from.path) {
        // Log a new view manually when the route changes.
        window._paq.push(["trackPageView"]);
      }
    },
  },
  mounted() {
    if (this.isEmbedded) {
      document.body.classList.add("digital-agenda-embedded");
    }
  },
};
</script>
