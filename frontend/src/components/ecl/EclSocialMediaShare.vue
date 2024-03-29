<template>
  <div class="ecl-social-media-share ecl-u-bg-transparent">
    <p class="ecl-social-media-share__description">Share this page</p>
    <!-- <div v-ec-wt-render="socialMediaKit" />-->
    <ul class="ecl-social-media-share__list">
      <li
        v-for="item in items"
        :key="item.key"
        class="ecl-social-media-share__item"
      >
        <ecl-link
          :to="item.to"
          :icon="item.icon"
          icon-size="xl"
          icon-left
          class="ecl-social-media-share__link"
          rel="noreferrer noopener"
          no-visited
          :title="item.label"
          @click.capture="item.func"
        />
      </li>
    </ul>
    <ecl-text-field
      ref="shareTextField"
      :model-value="currentUrl.toString()"
      read-only
      copy-on-click
    />
  </div>
</template>

<script>
import EclTextField from "@/components/ecl/forms/EclTextField.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
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
  components: { EclTextField, EclLink },
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
      return this.url ?? new URL(this.$route.href, window.location);
    },
    /**
     * EC Web Tools "Share Buttons" widget
     *
     *  https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/Social+bookmarking+and+networking
     */
    // socialMediaKit() {
    //   return {
    //     service: "sbkm",
    //     popup: false,
    //     target: true,
    //     shortenurl: true,
    //     to: ["facebook", "twitter", "e-mail", "linkedin"],
    //     icon: true,
    //     link: this.currentUrl.href,
    //   };
    // },
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
    mailToShare() {
      return `mailto:?subject=${this.currentChart.name}&body=${this.currentUrl}`;
    },
    items() {
      return [
        {
          key: "twitter",
          label: "Twitter",
          icon: "twitter",
          to: this.twitterShare,
        },
        {
          key: "facebook",
          label: "Facebook",
          icon: "facebook",
          to: this.facebookShare,
        },
        {
          key: "linkedin",
          label: "Linkedin",
          icon: "linkedin",
          to: this.linkedinShare,
        },
        {
          key: "email",
          label: "Email",
          icon: "email",
          to: this.mailToShare,
        },
        {
          key: "copy",
          label: "Copy to clipboard",
          icon: "copy-share",
          to: "#",
          func: this.copyUrl,
        },
      ];
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

<style scoped lang="scss">
.ecl-social-media-share__list {
  flex-direction: row !important;
  margin-bottom: 1rem;
}

.ecl-social-media-share__item {
  margin-right: 0;
}

.ecl-social-media-share__link {
  color: white !important;
}
</style>
