<template>
  <div class="ecl-page-header">
    <nav
      v-if="breadcrumbs.length > 0"
      v-ecl-init
      class="ecl-breadcrumb ecl-page-header__breadcrumb"
      aria-label="You are here:"
      data-ecl-breadcrumb="true"
      data-ecl-auto-init="Breadcrumb"
    >
      <ol class="ecl-breadcrumb__container">
        <li class="ecl-breadcrumb__segment" data-ecl-breadcrumb-item="static">
          <ecl-link
            :to="{ name: 'home' }"
            no-visited
            class="ecl-breadcrumb__link"
          >
            Home
          </ecl-link>
          <ecl-icon
            icon="corner-arrow"
            size="2xs"
            rotate="90"
            class="ecl-breadcrumb__icon"
            aria-hidden="true"
            role="presentation"
          />
        </li>
        <li
          v-for="(crumb, index) in breadcrumbs"
          :key="crumb.key"
          class="ecl-breadcrumb__segment"
          :class="{
            'ecl-breadcrumb__current-page': index === breadcrumbs.length - 1,
          }"
          data-ecl-breadcrumb-item="static"
        >
          <template v-if="index < breadcrumbs.length - 1">
            <ecl-link :to="crumb.to" no-visited class="ecl-breadcrumb__link">
              {{ crumb.label }}
            </ecl-link>
            <ecl-icon
              icon="corner-arrow"
              size="2xs"
              rotate="90"
              class="ecl-breadcrumb__icon"
              aria-hidden="true"
              role="presentation"
            />
          </template>
          <template v-else>
            {{ crumb.label }}
          </template>
        </li>
      </ol>
    </nav>

    <div v-if="pageTitle" class="ecl-page-header__title-container">
      <h1 class="ecl-page-header__title">
        {{ pageTitle }}
      </h1>
    </div>
  </div>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclIcon from "@/components/ecl/EclIcon.vue";

/**
 * ECL Page Header component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/site-wide/page-header/usage/
 *
 */
export default {
  name: "EclPageHeader",
  components: { EclIcon, EclLink },
  computed: {
    pageTitle() {
      if (typeof this.$route.meta.title === "function") {
        return this.$route.meta.title(this.$route);
      }
      return this.$route.meta.title;
    },
    breadcrumbs() {
      const result = [];
      for (const match of this.$route.matched) {
        let label = "";
        if (!match.meta.breadcrumb) {
          continue;
        } else if (typeof match.meta.breadcrumb === "function") {
          label = match.meta.breadcrumb(this.$route);
        } else {
          label = match.meta.breadcrumb;
        }

        result.push({
          label,
          key: match.name,
          to: {
            name: match.name,
            params: this.$route.params,
          },
        });
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
