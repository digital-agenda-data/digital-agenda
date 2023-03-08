<template>
  <div v-if="eclIsReady" class="ecl app-wrapper">
    <ecl-site-header />
    <main class="ecl-container">
      <ecl-page-header />
      <router-view />
    </main>
    <ecl-site-footer />
  </div>
</template>

<script>
import { useScriptTag } from "@vueuse/core";

import EclPageHeader from "@/components/ecl/site-wide/EclPageHeader.vue";
import EclSiteFooter from "@/components/ecl/site-wide/EclSiteFooter.vue";
import EclSiteHeader from "@/components/ecl/site-wide/EclSiteHeader.vue";

import eclURL from "@ecl/preset-ec/dist/scripts/ecl-ec.js?url";

export default {
  name: "MainLayout",
  components: { EclSiteFooter, EclPageHeader, EclSiteHeader },
  data() {
    return {
      eclIsReady: false,
    };
  },
  async mounted() {
    await this.loadECL();
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
