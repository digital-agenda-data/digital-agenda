<template>
  <div
    class="ecl app-wrapper"
    :class="{ 'digital-agenda-embedded': $route.query.embed === 'true' }"
  >
    <template v-if="isReady">
      <ecl-site-header />
      <main class="ecl-container">
        <ecl-page-header />
        <router-view />
      </main>
      <ecl-site-footer />
    </template>
    <ecl-spinner v-else size="large" centered />
  </div>
</template>

<script>
import { mapStores } from "pinia";
import { useScriptTag } from "@vueuse/core";

import eclURL from "@ecl/preset-ec/dist/scripts/ecl-ec.js?url";

import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclSiteHeader from "@/components/ecl/site-wide/EclSiteHeader.vue";
import EclSiteFooter from "@/components/ecl/site-wide/EclSiteFooter.vue";
import EclPageHeader from "@/components/ecl/site-wide/EclPageHeader.vue";

import { getRouteMeta } from "@/lib/utils";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";

const DEFAULT_TITLE = "Digital Scoreboard - Data & Indicators";

export default {
  name: "App",
  components: { EclPageHeader, EclSpinner, EclSiteFooter, EclSiteHeader },
  data() {
    return {
      eclIsReady: false,
    };
  },
  computed: {
    ...mapStores(useChartGroupStore, useChartStore),
    isReady() {
      // Only display the app after the chartGroups and the charts
      // have been loaded to avoid layout shifts.
      return (
        this.eclIsReady &&
        this.chartGroupStore.isReady &&
        this.chartStore.isReady
      );
    },
  },
  watch: {
    $route() {
      this.setTitle();
    },
  },
  async mounted() {
    await this.loadECL();
    this.setTitle();
  },
  methods: {
    /**
     * Load the ECL component library JavaScript by inserting script tags
     * into the document.
     *
     * The library doesn't support modern imports, so we do this here instead
     * of using a CDN as we want to serve them ourselves.
     */
    async loadECL() {
      try {
        // ECL.js also requires moment loaded in the global scope.
        // However, it's only used for the DatePicker component which we have
        // no need for, so simply mock it here to prevent failure.
        window.moment = { "": "Moment JS mock" };
        await useScriptTag(eclURL).load();
      } finally {
        this.eclIsReady = true;
      }
    },
    setTitle() {
      if (!this.isReady) return;

      this.$nextTick(() => {
        const pageTitle = getRouteMeta(this.$route, "title");
        if (pageTitle) {
          document.title = `${pageTitle} - ${DEFAULT_TITLE}`;
        } else {
          document.title = DEFAULT_TITLE;
        }
      });
    },
  },
};
</script>

<style>
@import "@ecl/preset-reset/dist/styles/optional/ecl-reset.css";

@import "@ecl/preset-ec/dist/styles/optional/ecl-ec-default.css" screen;
@import "@ecl/preset-ec/dist/styles/ecl-ec.css" screen;

@import "@ecl/preset-ec/dist/styles/optional/ecl-ec-default-print.css" print;
@import "@ecl/preset-ec/dist/styles/ecl-ec-print.css" print;

@import "vue-multiselect/dist/vue-multiselect.css";
</style>
