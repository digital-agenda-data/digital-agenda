<template>
  <div class="ecl-social-media-share ecl-u-bg-transparent">
    <p class="ecl-social-media-share__description">Share this page</p>
    <div v-ec-wt-render="socialMediaKit" />
    <ecl-text-field
      ref="shareTextField"
      :model-value="currentUrl"
      read-only
      copy-on-click
    />
  </div>
</template>

<script>
import EclTextField from "@/components/ecl/forms/EclTextField.vue";
import { useChartStore } from "@/stores/chartStore";
import { mapState } from "pinia";

/**
 * ECL Social Media Share component. See full documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/social-media-share/usage/
 *
 */
export default {
  name: "EclSocialMediaShare",
  components: { EclTextField },
  props: {
    url: {
      type: String,
      required: false,
      default: null,
    },
    text: {
      type: String,
      required: false,
      default: null,
    },
  },
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    currentUrl() {
      return (
        this.url ?? new URL(this.$route.href, window.location)
      ).toString();
    },
    /**
     * EC Web Tools "Share Buttons" widget
     *
     *  https://webgate.ec.europa.eu/fpfis/wikis/pages/viewpage.action?spaceKey=webtools&title=Social+bookmarking+and+networking
     */
    socialMediaKit() {
      return {
        service: "share",
        version: "2.0",
        shortenurl: false,
        networks: ["facebook", "twitter", "linkedin", "email", "more"],
        display: "icons",
        target: "_blank",
        link: this.currentUrl,
        title: this.text,
      };
    },
  },
  methods: {
    copyUrl(e) {
      e.preventDefault();
      e.stopPropagation();
      this.$refs.shareTextField.copyToClipboard();
    },
  },
};
</script>

<style scoped lang="scss"></style>
