<template>
  <div
    class="ecl app-wrapper"
    :class="{ 'digital-agenda-embedded': $route.query.embed === 'true' }"
  >
    <template v-if="loaded">
      <ecl-site-header />
      <main class="ecl-container">
        <ecl-page-header />
        <router-view />
      </main>
      <ecl-site-footer />
    </template>
    <main
      v-else
      class="ecl-u-d-flex ecl-u-align-items-center ecl-u-justify-content-center"
    >
      <ecl-spinner size="large" />
    </main>
  </div>
</template>

<script>
import { mapActions } from "pinia";
import { loadScript } from "vue-plugin-load-script";

import momentURL from "moment/min/moment.min.js?url";
import eclURL from "@ecl/preset-ec/dist/scripts/ecl-ec.js?url";

import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclSiteHeader from "@/components/ecl/site-wide/EclSiteHeader.vue";
import EclSiteFooter from "@/components/ecl/site-wide/EclSiteFooter.vue";
import EclPageHeader from "@/components/ecl/site-wide/EclPageHeader.vue";

import { useUserStore } from "@/stores/userStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useChartStore } from "@/stores/chartStore";
import { getRouteMeta } from "@/lib/utils";

const DEFAULT_TITLE = "Digital Scoreboard - Data & Indicators";

export default {
  name: "App",
  components: { EclPageHeader, EclSpinner, EclSiteFooter, EclSiteHeader },
  data() {
    return {
      loaded: false,
    };
  },
  watch: {
    $route() {
      this.setTitle();
    },
  },
  async mounted() {
    try {
      this.loaded = false;
      await Promise.allSettled([this.loadECL(), this.loadInitialData()]);
    } finally {
      this.loaded = true;
    }
    this.setTitle();
  },
  methods: {
    ...mapActions(useUserStore, ["getCurrentUser"]),
    ...mapActions(useChartStore, ["getCharts"]),
    ...mapActions(useChartGroupStore, ["getChartGroups"]),
    async loadInitialData() {
      await Promise.all([
        // this.getCurrentUser(),
        this.getChartGroups(),
        this.getCharts(),
      ]);
    },
    /**
     * Load the ECL component library JavaScript by inserting script tags
     * into the document.
     *
     * The library doesn't support modern imports, so we do this here instead
     * of using a CDN as we want to serve them ourselves.
     */
    async loadECL() {
      // ECL.js also requires moment loaded in the global scope. (i.e. window)
      // So we also load moment.js here in the same way before loading ECL.js
      await loadScript(momentURL);
      await loadScript(eclURL);
    },
    setTitle() {
      if (!this.loaded) return;

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
