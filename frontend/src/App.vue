<template>
  <div class="ecl app-wrapper">
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

export default {
  name: "App",
  components: { EclPageHeader, EclSpinner, EclSiteFooter, EclSiteHeader },
  data() {
    return {
      loaded: false,
    };
  },
  async mounted() {
    try {
      this.loaded = false;
      await Promise.allSettled([this.loadECL(), this.loadInitialData()]);
    } finally {
      this.loaded = true;
    }
  },
  methods: {
    ...mapActions(useUserStore, ["getCurrentUser"]),
    ...mapActions(useChartGroupStore, ["getChartGroups"]),
    async loadInitialData() {
      await Promise.all([this.getCurrentUser(), this.getChartGroups()]);
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
  },
};
</script>

<style>
@import "@ecl/preset-reset/dist/styles/optional/ecl-reset.css";

@import "@ecl/preset-ec/dist/styles/optional/ecl-ec-default.css" screen;
@import "@ecl/preset-ec/dist/styles/ecl-ec.css" screen;

@import "@ecl/preset-ec/dist/styles/optional/ecl-ec-default-print.css" print;
@import "@ecl/preset-ec/dist/styles/ecl-ec-print.css" print;
</style>
