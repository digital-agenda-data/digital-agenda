<template>
  <div class="ecl-site-footer__row ecl-site-footer__row--specific">
    <div class="ecl-site-footer__section ecl-site-footer__section--site-info">
      <div class="ecl-site-footer__title">
        <ecl-link
          to="https://digital-strategy.ec.europa.eu/en"
          icon="arrow-right"
          label="Shaping Europe’s digital future"
          class="ecl-site-footer__title-link"
          variant=""
          inverted
        />
      </div>
      <div class="ecl-site-footer__description">
        This site is managed by:
        <br />
        Directorate-General for Communications Networks, Content and Technology
      </div>
      <ecl-social-media-follow
        class="ecl-site-footer__social-media"
        :items="socialMediaLinks"
        horizontal
      />
    </div>
    <div class="ecl-site-footer__section ecl-site-footer__section--links">
      <div class="ecl-site-footer__row">
        <div class="ecl-site-footer__section ecl-site-footer__section--contact">
          <div class="ecl-site-footer__title">Contact us</div>
          <ecl-site-footer-list :items="contactUsLinks" />
        </div>
        <div class="ecl-site-footer__section ecl-site-footer__section--about">
          <div class="ecl-site-footer__title">About us</div>
          <ecl-site-footer-list :items="aboutUsLinks" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EclSocialMediaFollow from "@/components/ecl/EclSocialMediaFollow.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclSiteFooterList from "@/components/ecl/site-wide/EclSiteFooterList.vue";
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclSiteFooterSpecific",
  components: { EclSiteFooterList, EclSocialMediaFollow, EclLink },
  data() {
    return {
      socialMediaLinks: [
        {
          link: "https://www.facebook.com/DigitalEU",
          label: "Digital EU on Facebook",
          icon: "networks--facebook",
        },
        {
          link: "https://www.instagram.com/DigitalEU/",
          label: "Digital EU on Instagram",
          icon: "networks--instagram",
        },
        {
          link: "https://www.linkedin.com/showcase/digital-eu/",
          label: "Digital EU on LinkedIn",
          icon: "networks--linkedin",
        },
        {
          link: "https://www.youtube.com/c/DigitalEU",
          label: "Digital EU on YouTube",
          icon: "networks--youtube",
        },
        {
          link: "https://x.com/DigitalEU",
          label: "DigitalEU on X",
          icon: "networks--x",
        },
      ],
      contactUsLinks: [
        {
          link: "https://digital-strategy.ec.europa.eu/en/write-us",
          label: "Contact DG CONNECT",
        },
      ],
      aboutUsLinks: [
        {
          link: "https://digital-strategy.ec.europa.eu/en/pages/legal-notice",
          label: "Privacy statement",
          icon: "external",
        },
        {
          link: "https://digital-strategy.ec.europa.eu/en/pages/legal-notice",
          label: "Copyright notice",
          icon: "external",
        },
        {
          link: "https://ec.europa.eu/info/departments/communications-networks-content-and-technology_en",
          label: "About Directorate-General CONNECT",
          icon: "external",
        },
        {
          link: "https://digital-strategy.ec.europa.eu/en/pages/legal-notice",
          label: "Language Policy",
          icon: "external",
        },
        {
          link: "/page/accessibility-statement",
          label: "Accessibility statement",
          icon: "external",
        },
      ],
    };
  },
});
</script>
