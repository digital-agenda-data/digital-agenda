<template>
  <header v-ecl-init class="ecl-site-header" data-ecl-auto-init="SiteHeader">
    <div class="ecl-site-header__header">
      <div class="ecl-site-header__container ecl-container">
        <div class="ecl-site-header__top">
          <ecl-link
            :to="{ name: 'home' }"
            class="ecl-site-header__logo-link"
            aria-label="European Commission"
          >
            <img
              alt="European Commission logo"
              title="European Commission"
              class="ecl-site-header__logo-image ecl-site-header__logo-image-desktop"
              :src="logoURL"
            />
          </ecl-link>
          <div class="ecl-site-header__action">
            <div class="ecl-site-header__login-container">
              <a
                class="ecl-button ecl-button--ghost ecl-site-header__login-toggle"
                :href="loginLink"
              >
                <ecl-icon
                  icon="log-in"
                  size="s"
                  class="ecl-site-header__icon"
                />
                Log in
              </a>
            </div>
            <div class="ecl-site-header__search-container">
              <ecl-button
                variant="ghost"
                data-ecl-search-toggle="true"
                aria-controls="search-form-id"
                aria-expanded="false"
                icon="search"
                class="ecl-site-header__search-toggle"
                label="Search"
              />

              <ecl-search-form
                id="search-form-id"
                :model-value="searchQuery"
                class="ecl-site-header__search"
                data-ecl-search-form=""
                placeholder="e.g. social media"
                help-text="Search for indicators"
                :action="searchAction"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="ecl-site-header__banner">
      <div class="ecl-container">
        <div class="ecl-site-header__site-name">
          Data Visualisation Tool - Data & Indicators
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";
import { loginLink } from "@/lib/api";
import logoURL from "@ecl/preset-ec/dist/images/logo/positive/logo-ec--en.svg?url";
import EclButton from "@/components/ecl/EclButton.vue";
import EclSearchForm from "@/components/ecl/forms/EclSearchForm.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { useRouteQuery } from "@vueuse/router";

/**
 * ECL Site Header component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/site-wide/site-header/usage/
 *
 */
export default {
  name: "EclSiteHeader",
  components: { EclIcon, EclLink, EclButton, EclSearchForm },
  data() {
    return {
      logoURL,
      loginLink,
      searchQuery: useRouteQuery("q"),
    };
  },
  computed: {
    searchAction() {
      return this.$router.resolve({ name: "search" }).fullPath;
    },
  },
};
</script>

<style scoped></style>
