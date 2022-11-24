<template>
  <div class="ecl-page-header">
    <ecl-breadcrumbs
      v-if="breadcrumbs.length > 1"
      class="ecl-page-header__breadcrumb"
      :items="breadcrumbs"
    />

    <div v-if="pageTitle" class="ecl-page-header__title-container">
      <h1 class="ecl-page-header__title">
        {{ pageTitle }}
      </h1>
    </div>
  </div>
</template>

<script>
import EclBreadcrumbs from "@/components/ecl/navigation/EclBreadcrumbs.vue";
import { getRouteMeta } from "@/lib/utils";

/**
 * ECL Page Header component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/site-wide/page-header/usage/
 *
 */
export default {
  name: "EclPageHeader",
  components: { EclBreadcrumbs },
  computed: {
    pageTitle() {
      return getRouteMeta(this.$route, "title");
    },
    breadcrumbs() {
      const result = [
        {
          id: "home",
          text: "Home",
          to: { name: "home" },
        },
      ];

      for (const match of this.$route.matched) {
        let label = getRouteMeta(match, "breadcrumb");
        if (!label) {
          continue;
        }

        const newParams = {};
        for (const paramsKey in this.$route.params) {
          if (match.path.includes(`/:${paramsKey}`)) {
            newParams[paramsKey] = this.$route.params[paramsKey];
          }
        }

        result.push({
          id: match.name,
          text: label,
          to: {
            name: match.name,
            params: newParams,
          },
        });
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
