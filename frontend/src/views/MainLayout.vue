<template>
  <div v-if="appSettings.global_banner_enabled" id="globan-here" />
  <div v-if="isReady" class="ecl app-wrapper">
    <ecl-site-header />
    <main class="ecl-container">
      <ecl-page-header />
      <router-view />
    </main>
    <ecl-site-footer />
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useScriptTag } from "@vueuse/core";

import EclPageHeader from "@/components/ecl/site-wide/EclPageHeader.vue";
import EclSiteFooter from "@/components/ecl/site-wide/EclSiteFooter.vue";
import EclSiteHeader from "@/components/ecl/site-wide/EclSiteHeader.vue";

import { useAppSettings } from "@/stores/appSettingsStore";

import eclURL from "@ecl/preset-ec/dist/scripts/ecl-ec.js?url";

export default {
  name: "MainLayout",
  components: { EclSiteFooter, EclPageHeader, EclSiteHeader },
  data() {
    return {
      isReady: false,
    };
  },
  computed: {
    ...mapState(useAppSettings, ["appSettings"]),
  },
  watch: {
    $route(to, from) {
      if (window._paq && to.path !== from.path) {
        // Log a new view manually when the route changes.
        window._paq.push(["trackPageView"]);
      }
    },
  },
  async mounted() {
    try {
      await Promise.all([this.loadECL(), this.initGloban()]);
    } finally {
      this.isReady = true;
      // Always attempt to load analytics but do it after the "important"
      // libraries are loaded.
      await this.initAnalytics();
    }
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
      // ECL.js also requires moment loaded in the global scope.
      // However, it's only used for the DatePicker component which we have
      // no need for, so simply mock it here to prevent failure.
      window.moment = { "": "Moment JS mock" };
      await useScriptTag(eclURL).load();
    },
    async initAnalytics() {
      const siteId = this.appSettings.analytics_site_id;
      let server = this.appSettings.analytics_server;

      if (!siteId || !server) return;
      if (!server.endsWith("/")) server += "/";

      const _paq = (window._paq = window._paq || []);
      _paq.push(["trackPageView"]);
      _paq.push(["setTrackerUrl", server + "matomo.php"]);
      _paq.push(["setSiteId", siteId]);
      const d = document,
        g = d.createElement("script"),
        s = d.getElementsByTagName("script")[0];
      g.async = true;
      g.src = server + "matomo.js";
      s.parentNode.insertBefore(g, s);
    },
    async initGloban() {
      if (!this.appSettings.global_banner_enabled) return;

      await useScriptTag(
        "https://europa.eu/webtools/load.js?globan=1010"
      ).load();
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

#globan-here {
  min-height: 28px;
}
</style>
