<template>
  <div class="ecl-social-media-share ecl-u-bg-transparent">
    <p class="ecl-social-media-share__description">Share this page</p>
    <ul class="ecl-social-media-share__list">
      <li
        v-for="item in items"
        :key="item.key"
        class="ecl-social-media-share__item"
      >
        <ecl-link
          :label="item.label"
          :to="item.to"
          :icon="item.icon"
          icon-left
          class="ecl-social-media-share__link"
        />
      </li>
    </ul>
  </div>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";
/**
 * ECL Social Media Share component. See full documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/social-media-share/usage/
 *
 */
export default {
  name: "EclSocialMediaShare",
  components: { EclLink },
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
    facebookShare() {
      const url = new URL("https://facebook.com/sharer/sharer.php");
      url.searchParams.set("u", this.currentUrl);
      return url.toString();
    },
    twitterShare() {
      const url = new URL("https://twitter.com/intent/tweet");
      url.searchParams.set("url", this.currentUrl);
      if (this.text) {
        url.searchParams.set("text", this.text);
      }

      return url.toString();
    },
    linkedinShare() {
      const url = new URL("https://www.linkedin.com/sharing/share-offsite/");
      url.searchParams.set("url", this.currentUrl);
      return url.toString();
    },
    items() {
      return [
        {
          key: "twitter",
          label: "Twitter",
          icon: "twitter-color",
          to: this.twitterShare,
        },
        {
          key: "facebook",
          label: "Facebook",
          icon: "facebook-color",
          to: this.facebookShare,
        },
        {
          key: "linkedin",
          label: "Linkedin",
          icon: "linkedin-color",
          to: this.linkedinShare,
        },
      ];
    },
  },
};
</script>

<style scoped></style>
