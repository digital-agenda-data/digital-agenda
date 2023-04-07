<template>
  <footer class="ecl-site-footer">
    <div class="ecl-container ecl-site-footer__container">
      <div class="ecl-site-footer__row">
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <h2 class="ecl-site-footer__title">
              <ecl-link
                :to="{ name: 'home' }"
                label="Data Visualisation Tool"
                class="ecl-site-footer__title-link"
              />
            </h2>
            <div class="ecl-site-footer__description">
              <div>
                This site is managed by the Directorate-General for
                Communications Networks, Content and Technology
              </div>
              <div class="ecl-u-mt-l">
                <ecl-link
                  class="ecl-site-footer__link ecl-link--icon-before"
                  to="https://creativecommons.org/licenses/by/4.0/"
                  aria-label="Creative Commons Attribution License"
                >
                  <img
                    src="@/assets/cc_icon_white_x2.png"
                    alt=""
                    class="ecl-icon--fluid ecl-u-mr-xs"
                  />
                  <span class="ecl-link__label">Creative commons license</span>
                </ecl-link>
              </div>
            </div>
          </div>
        </div>
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <h2
              class="ecl-site-footer__title ecl-site-footer__title--separator"
            >
              Follow us on
            </h2>
            <ul class="ecl-site-footer__list ecl-site-footer__list--inline">
              <li
                v-for="social in socialMediaLinks"
                :key="social.icon"
                class="ecl-site-footer__list-item"
              >
                <ecl-link
                  class="ecl-site-footer__link"
                  :to="social.link"
                  :icon="social.icon"
                  :label="social.label"
                  icon-left
                />
              </li>
            </ul>
            <div class="ecl-site-footer__section">
              <h2
                class="ecl-site-footer__title ecl-site-footer__title--separator"
              >
                Related links
              </h2>
              <ul class="ecl-site-footer__list ecl-site-footer__list--inline">
                <li class="ecl-site-footer__list-item">
                  <ecl-link
                    class="ecl-site-footer__link"
                    :to="loginLink"
                    aria-label="Link to Login Page"
                    label="Log in"
                  />
                </li>
                <li class="ecl-site-footer__list-item">
                  <ecl-link
                    to="https://github.com/digital-agenda-data/"
                    label="Source code"
                    class="ecl-site-footer__link"
                    icon="external"
                  />
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <h2
              class="ecl-site-footer__title ecl-site-footer__title--separator"
            >
              About us
            </h2>
            <ul class="ecl-site-footer__list">
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  class="ecl-site-footer__link"
                  :to="{ name: 'about' }"
                  aria-label="Link to Information about the Digital Agenda"
                  label="About this website"
                />
              </li>
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  class="ecl-site-footer__link"
                  :to="{ name: 'feedback' }"
                  aria-label="Link to Submit feedback"
                  label="Submit feedback"
                />
              </li>
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  class="ecl-site-footer__link"
                  to="https://ec.europa.eu/info/about-european-commission/contact_en"
                  aria-label="Link to Contact the European Commission"
                  label="Contact us"
                />
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="ecl-site-footer__row">
        <div class="ecl-site-footer__column">
          <div class="ecl-site-footer__section">
            <ecl-link
              to="https://ec.europa.eu/info/index_en"
              class="ecl-site-footer__logo-link"
              aria-label="European Commission"
            >
              <img
                alt="European Commission logo"
                title="European Commission"
                class="ecl-site-footer__logo-image-desktop"
                :src="logoURL"
              />
            </ecl-link>

            <h2 class="ecl-site-footer__title">
              <ecl-link
                class="ecl-site-footer__title-link"
                to="https://ec.europa.eu/info/index_en"
                label="European Commission"
              />
            </h2>
          </div>
        </div>

        <div class="ecl-site-footer__column">
          <div
            class="ecl-site-footer__section ecl-footer-standardised__section--split-list"
          >
            <ul class="ecl-site-footer__list">
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  to="https://ec.europa.eu/info/about-european-commission/contact_en"
                  class="ecl-site-footer__link"
                  aria-label="Link to Contact the European Commission"
                  label="Contact the European Commission"
                />
              </li>
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  to="https://european-union.europa.eu/contact-eu/social-media-channels_en#/search?page=0&amp;institutions=european_commission"
                  class="ecl-site-footer__link"
                  label="Follow the European Commission on social media"
                />
              </li>
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  to="https://ec.europa.eu/info/resources-partners_en"
                  class="ecl-site-footer__link"
                  label="Resources for partners"
                />
              </li>
            </ul>
          </div>
        </div>
        <div class="ecl-site-footer__column">
          <div
            class="ecl-site-footer__section ecl-footer-standardised__section--split-list"
          >
            <ul class="ecl-site-footer__list">
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  to="https://ec.europa.eu/info/language-policy_en"
                  class="ecl-site-footer__link"
                  aria-label="Link to Languages on our websites"
                  label="Languages on our websites"
                />
              </li>
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  to="https://ec.europa.eu/info/cookies_en"
                  class="ecl-site-footer__link"
                  aria-label="Link to Cookies"
                  label="Cookies"
                />
              </li>
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  to="https://ec.europa.eu/info/privacy-policy_en"
                  class="ecl-site-footer__link"
                  aria-label="Link to Privacy policy"
                  label="Privacy policy"
                />
              </li>
              <li class="ecl-site-footer__list-item">
                <ecl-link
                  to="https://ec.europa.eu/info/legal-notice_en"
                  class="ecl-site-footer__link"
                  aria-label="Link to Legal notice"
                  label="Legal notice"
                />
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
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
  components: { EclLink },
  data() {
    return {
      logoURL,
      loginLink,
      socialMediaLinks: [
        {
          link: "https://www.facebook.com/DigitalEU",
          icon: "facebook-negative",
          label: "Facebook",
        },
        {
          link: "https://www.youtube.com/c/DigitalEU",
          icon: "youtube-negative",
          label: "Youtube",
        },
        {
          link: "https://www.linkedin.com/showcase/digital-eu/",
          icon: "linkedin-negative",
          label: "Linkedin",
        },
        {
          link: "https://www.instagram.com/DigitalEU/",
          icon: "instagram-negative",
          label: "Instagram",
        },
        {
          link: "https://twitter.com/DigitalEU",
          icon: "twitter-negative",
          label: "Twitter",
        },
      ],
    };
  },
};
</script>

<style scoped></style>
