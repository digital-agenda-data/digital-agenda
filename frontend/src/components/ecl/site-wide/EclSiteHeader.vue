<template>
  <div
    id="header"
    v-ecl-init
    class="ecl-site-header"
    data-ecl-auto-init="SiteHeader"
    data-ecl-has-menu
  >
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
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="ecl-site-header__banner">
      <div class="ecl-container">
        <div class="ecl-site-header__site-name">
          Shaping Europe’s digital future
        </div>
      </div>
    </div>
    <ecl-menu :items="menuItems" />
  </div>
  <div class="ecl-site-header__message">
    <div class="ecl-container ecl-u-mt-m">
      <ecl-notification
        v-for="(message, index) in messagesStore.messageList"
        v-bind="message"
        :key="'message' + index"
        @close="messagesStore.removeMessage(index)"
      />
    </div>
  </div>
</template>

<script>
import EclNotification from "@/components/ecl/EclNotification.vue";
import EclMenu from "@/components/ecl/navigation/EclMenu.vue";
import { useMessagesStore } from "@/stores/messagesStore";
import logoURL from "@ecl/preset-ec/dist/images/logo/positive/logo-ec--en.svg?url";
import EclButton from "@/components/ecl/EclButton.vue";
import EclSearchForm from "@/components/ecl/forms/EclSearchForm.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { useRouteQuery } from "@vueuse/router";
import { mapStores } from "pinia";

/**
 * ECL Site Header component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/site-wide/site-header/usage/
 *
 */
export default {
  name: "EclSiteHeader",
  components: { EclMenu, EclNotification, EclLink, EclButton, EclSearchForm },
  data() {
    return {
      logoURL,
      searchQuery: useRouteQuery("q"),
      menuItems: [
        {
          id: "home",
          link: "https://digital-strategy.ec.europa.eu/en",
          label: "Home",
        },
        {
          id: "policies",
          link: "https://digital-strategy.ec.europa.eu/en/policies",
          label: "Policies",
        },
        {
          id: "activities",
          link: "https://digital-strategy.ec.europa.eu/en/activities",
          label: "Activities",
        },
        {
          id: "news",
          link: "https://digital-strategy.ec.europa.eu/en/news",
          label: "News",
        },
        {
          id: "library",
          link: "https://digital-strategy.ec.europa.eu/en/library",
          label: "Library",
        },
        {
          id: "funding",
          link: "https://digital-strategy.ec.europa.eu/en/funding",
          label: "Funding",
        },
        {
          id: "calendar",
          link: "https://digital-strategy.ec.europa.eu/en/events",
          label: "Calendar",
        },
        {
          id: "consultations",
          link: "https://digital-strategy.ec.europa.eu/en/consultations",
          label: "Consultations",
        },
        {
          id: "aioffice",
          link: "https://digital-strategy.ec.europa.eu/en/policies/ai-office",
          label: "AI Office",
        },
      ],
    };
  },
  computed: {
    ...mapStores(useMessagesStore),
  },
};
</script>

<style scoped></style>
