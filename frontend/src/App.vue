<template>
  <div v-if="loaded">
    <ecl-site-header />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import { mapActions } from "pinia";
import { loadScript } from "vue-plugin-load-script";

import momentURL from "moment/min/moment.min.js?url";
import eclURL from "@ecl/preset-ec/dist/scripts/ecl-ec.js?url";

import userStore from "@/stores/userStore";
import EclSiteHeader from "@/components/ecl/site-wide/EclSiteHeader.vue";

export default {
  name: "App",
  components: { EclSiteHeader },
  data() {
    return {
      loaded: false,
    };
  },
  async mounted() {
    try {
      this.loaded = false;
      await Promise.all([this.loadInitialData(), this.loadECL()]);
    } finally {
      this.loaded = true;
    }
  },
  methods: {
    ...mapActions(userStore, ["getCurrentUser"]),
    async loadInitialData() {
      await Promise.all([this.getCurrentUser()]);
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
