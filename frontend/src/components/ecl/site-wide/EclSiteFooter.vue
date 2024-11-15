<template>
  <footer id="footer" class="ecl-site-footer">
    <div class="ecl-container ecl-site-footer__container">
      <div class="ecl-site-footer__row">
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <h2 class="ecl-site-footer__title">
              <ecl-link
                to="https://digital-strategy.ec.europa.eu/en"
                class="ecl-site-footer__title-link"
              >
                Shaping Europe’s digital future
              </ecl-link>
            </h2>
            <div class="ecl-site-footer__description">
              This site is managed by: Directorate-General for Communications
              Networks, Content and Technology
            </div>
          </div>
        </div>
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <h2
              class="ecl-site-footer__title ecl-site-footer__title--separator"
            >
              Contact us
            </h2>
            <ul class="ecl-site-footer__list">
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  to="https://digital-strategy.ec.europa.eu/en/write-us"
                  class="ecl-site-footer__link"
                >
                  Contact DG CONNECT
                </ecl-link>
              </li>
            </ul>
          </div>
          <div class="ecl-site-footer__section">
            <h2
              class="ecl-site-footer__title ecl-site-footer__title--separator"
            >
              Follow us
            </h2>
            <ecl-site-footer-list
              :items="socialMediaLinks"
              class="ecl-site-footer__list--inline"
            />
          </div>
        </div>
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <h2
              class="ecl-site-footer__title ecl-site-footer__title--separator"
            >
              About us
            </h2>
            <ecl-site-footer-list :items="aboutUsLinks" />
          </div>
        </div>
      </div>
      <div class="ecl-site-footer__row">
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <ecl-link
              to="https://commission.europa.eu/index_en"
              class="ecl-site-footer__logo-link"
              aria-label="Home - European Commission"
            >
              <img
                :src="logoURL"
                title="European Commission"
                alt="European Commission logo"
              />
            </ecl-link>
          </div>
        </div>
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <ecl-site-footer-list :items="extraLinks1" />
          </div>
        </div>
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <ecl-site-footer-list :items="extraLinks2" />
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import EclSiteFooterList from "@/components/ecl/site-wide/EclSiteFooterList.vue";
import logoURL from "@ecl/preset-ec/dist/images/logo/negative/logo-ec--en.svg?url";

import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { loginLink } from "@/lib/api";
/**
 * ECL Site Footer component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/site-wide/site-footer/usage/
 *
 */
export default {
  name: "EclSiteFooter",
  components: { EclSiteFooterList, EclLink },
  data() {
    return {
      logoURL,
      loginLink,
      socialMediaLinks: [
        {
          id: "facebook-negative",
          link: "https://www.facebook.com/DigitalEU",
          label: "Digital EU on Facebook",
        },
        {
          id: "instagram-negative",
          link: "https://www.instagram.com/DigitalEU/",
          label: "Digital EU on Instagram",
        },
        {
          id: "linkedin-negative",
          link: "https://www.linkedin.com/showcase/digital-eu/",
          label: "Digital EU on LinkedIn",
        },
        {
          id: "youtube-negative",
          link: "https://www.youtube.com/c/DigitalEU",
          label: "Digital EU on Youtube",
        },
        {
          id: "twitter-negative",
          link: "https://twitter.com/DigitalEU",
          label: "@DigitalEU on Twitter",
        },
      ],
      aboutUsLinks: [
        {
          id: "copyright",
          link: "https://digital-strategy.ec.europa.eu/en/pages/legal-notice#ecl-inpage-km0gezfs",
          label: "Copyright notice",
        },
        {
          id: "about",
          link: "https://commission.europa.eu/about-european-commission/departments-and-executive-agencies/communications-networks-content-and-technology_en",
          label: "About Directorate-General CONNECT",
        },
        {
          id: "accessibility",
          link: "https://digital-strategy.ec.europa.eu/en/pages/accessibility",
          label: "Accessibility statement",
        },
      ],
      extraLinks1: [
        {
          id: "contact",
          link: "https://commission.europa.eu/about-european-commission/contact_en",
          label: "Contact the European Commission",
        },
        {
          id: "follow",
          link: "https://european-union.europa.eu/contact-eu/social-media-channels_en#/search?page=0&institutions=european_commission",
          label: "Follow the European Commission on social media",
        },
        {
          id: "resources",
          link: "https://commission.europa.eu/resources-partners_en",
          label: "Resources for partners",
        },
        {
          id: "security",
          link: "https://commission.europa.eu/legal-notice/vulnerability-disclosure-policy_en",
          label: "Report an IT vulnerability",
        },
      ],
      extraLinks2: [
        {
          id: "language-policy",
          link: "https://commission.europa.eu/language-policy_en",
          label: "Language policy",
        },
        {
          id: "cookies",
          link: "https://commission.europa.eu/cookies_en",
          label: "Cookies",
        },
        {
          id: "privacy-policy",
          link: "https://commission.europa.eu/privacy-policy_en",
          label: "Privacy policy",
        },
        {
          id: "legal-notice",
          link: "https://commission.europa.eu/legal-notice_en",
          label: "Legal notice",
        },
      ],
    };
  },
};
</script>

<style scoped></style>
