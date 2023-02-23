<template>
  <div class="ecl-social-media-share ecl-u-bg-transparent">
    <p class="ecl-social-media-share__description">Share this page</p>
    <div v-ec-wt-render="socialMediaKit" />
  </div>
</template>

<script>
/**
 * ECL Social Media Share component. See full documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/social-media-share/usage/
 *
 */
export default {
  name: "EclSocialMediaShare",
  props: {
    text: {
      type: String,
      required: false,
      default: null,
    },
  },
  computed: {
    currentUrl() {
      return new URL(this.$route.href, window.location);
    },
    /**
     * EC Web Tools "Share Buttons" widget
     *
     *  https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/Social+bookmarking+and+networking
     */
    socialMediaKit() {
      return {
        service: "sbkm",
        popup: false,
        target: true,
        shortenurl: true,
        to: ["facebook", "twitter", "e-mail", "linkedin"],
        icon: true,
        link: this.currentUrl.href,
      };
    },
  },
};
</script>

<style scoped></style>
