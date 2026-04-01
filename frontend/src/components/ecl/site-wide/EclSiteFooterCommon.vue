<template>
  <div class="ecl-site-footer__row ecl-site-footer__section--common">
    <div class="ecl-site-footer__section ecl-site-footer__section--common">
      <ecl-link
        to="https://commission.europa.eu/index_en"
        class="ecl-site-header__logo-link"
        aria-label="European Commission"
        inverted
      >
        <picture
          class="ecl-picture ecl-site-footer__picture"
          title="European Commission"
        >
          <img
            class="ecl-site-footer__logo-image"
            :src="logoURL"
            alt="European Commission logo"
          />
        </picture>
      </ecl-link>
      <div class="ecl-site-footer__extra-links-container">
        <ecl-social-media-follow
          class="ecl-site-footer__social-media"
          :items="socialMediaLinks"
          description="Follow the European Commission"
        />
        <ecl-site-footer-list :items="contactUsLinks" inline />
      </div>
      <ecl-site-footer-list :items="otherLinks" inline />
    </div>
  </div>
</template>

<script>
import EclSiteFooterList from "@/components/ecl/site-wide/EclSiteFooterList.vue";
import { defineComponent } from "vue";
import logoURL from "@ecl/preset-ec/dist/images/logo/negative/logo-ec--en.svg?url";
import EclSocialMediaFollow from "@/components/ecl/EclSocialMediaFollow.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default defineComponent({
  name: "EclSiteFooterCommon",
  components: { EclSiteFooterList, EclSocialMediaFollow, EclLink },
  data() {
    return {
      logoURL,
      socialMediaLinks: [
        {
          link: "https://www.facebook.com/EuropeanCommission",
          label: "Facebook",
          icon: "networks--facebook",
        },
        {
          link: "https://www.instagram.com/europeancommission",
          label: "Instagram",
          icon: "networks--instagram",
        },
        {
          link: "https://x.com/EU_Commission",
          label: "X",
          icon: "networks--x",
        },
        {
          link: "https://www.linkedin.com/company/european-commission",
          label: "Linkedin",
          icon: "networks--linkedin",
        },
        {
          link: "https://european-union.europa.eu/contact-eu/social-media-channels_en",
          label: "Other",
          icon: "networks--chain",
        },
      ],
      contactUsLinks: [
        {
          link: "https://commission.europa.eu/about/contact_en",
          label: "Contact us",
        },
      ],
      otherLinks: [
        {
          link: "https://commission.europa.eu/legal-notice/vulnerability-disclosure-policy_en",
          label: "Report an IT vulnerability",
        },
        {
          link: "https://commission.europa.eu/languages-our-websites_en",
          label: "Languages on our websites",
        },
        {
          link: "https://commission.europa.eu/cookies-policy_en",
          label: "Cookies",
        },
        {
          link: "https://commission.europa.eu/privacy-policy-websites-managed-european-commission_en",
          label: "Privacy policy",
        },
        {
          link: "https://commission.europa.eu/legal-notice_en",
          label: "Legal notice",
        },
        {
          link: "https://digital-strategy.ec.europa.eu/en/pages/accessibility",
          label: "Accessibility",
        },
      ],
    };
  },
});
</script>
