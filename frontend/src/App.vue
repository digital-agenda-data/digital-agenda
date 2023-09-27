<template>
  <simple-spinner v-if="!isReady" />
  <interactive-chart v-else-if="isEmbedded" />
  <main-layout v-else />
</template>

<script>
import { setHighchartsDefaults } from "@/initHighchart";
import { mapStores } from "pinia";
import { defineAsyncComponent } from "vue";

import { getRouteMeta } from "@/lib/utils";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useAppSettings } from "@/stores/appSettingsStore";

import SimpleSpinner from "@/components/SimpleSpinner.vue";

const DEFAULT_TITLE = "Digital Decade DESI visualisation tool";

export default {
  name: "App",
  components: {
    SimpleSpinner,
    // Define async components (instead of regular ones) to avoid loading
    // extra CSS/JS while in embed mode
    MainLayout: defineAsyncComponent({
      loader: () => import("@/views/MainLayout.vue"),
      loadingComponent: SimpleSpinner,
    }),
    InteractiveChart: defineAsyncComponent({
      loader: () => import("@/components/charts/InteractiveChart.vue"),
      loadingComponent: SimpleSpinner,
    }),
  },
  computed: {
    ...mapStores(useChartGroupStore, useChartStore, useAppSettings),
    isEmbedded() {
      return new URL(window.location).searchParams.get("embed") === "true";
    },
    isReady() {
      // Only display the app after the chartGroups and the charts
      // have been loaded to avoid layout shifts.
      return (
        this.chartGroupStore.isReady &&
        this.chartStore.isReady &&
        this.appSettingsStore.isReady
      );
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
    isReady() {
      setHighchartsDefaults();
    },
  },
  mounted() {
    if (this.isEmbedded) {
      document.body.classList.add("digital-agenda-embedded");
    }
  },
};
</script>
