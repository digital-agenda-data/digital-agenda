<template>
  <skip-list />
  <div v-if="isReady" class="ecl app-wrapper">
    <header>
      <div
        v-if="appSettings.global_banner_enabled"
        v-ec-wt-render="{ service: 'globan' }"
      />
      <div v-if="appSettings.cck_enabled" v-ec-wt-render="{ utility: 'cck' }" />
      <div
        v-if="appSettings.analytics_site_id"
        v-ec-wt-render="{
          utility: 'analytics',
          siteID: appSettings.analytics_site_id,
          sitePath: [host],
          instance: 'ec',
          mode: 'default',
        }"
      />
      <ecl-site-header />
    </header>
    <main class="ecl-container">
      <ecl-page-header />
      <section id="main">
        <router-view />
      </section>
    </main>
    <ecl-site-footer />
  </div>
</template>

<script>
import SkipList from "@/components/SkipList.vue";
import { mapState } from "pinia";
import { useScriptTag } from "@vueuse/core";

import EclPageHeader from "@/components/ecl/site-wide/EclPageHeader.vue";
import EclSiteFooter from "@/components/ecl/site-wide/EclSiteFooter.vue";
import EclSiteHeader from "@/components/ecl/site-wide/EclSiteHeader.vue";

import { useAppSettings } from "@/stores/appSettingsStore";

import eclURL from "@ecl/preset-ec/dist/scripts/ecl-ec.js?url";

export default {
  name: "MainLayout",
  components: { SkipList, EclSiteFooter, EclPageHeader, EclSiteHeader },
  data() {
    return {
      host: window.location.host,
      isReady: false,
    };
  },
  computed: {
    ...mapState(useAppSettings, ["appSettings"]),
  },
  watch: {
    $route(to, from) {
      if (
        window.$wt?.analytics.isTrackable() &&
        window.$wt?.analytics.isActive &&
        to.path !== from.path
      ) {
        // Log a new view manually when the route changes.
        window.$wt.trackPageView();
      }
    },
  },
  async mounted() {
    await this.loadECL();
    this.isReady = true;
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
