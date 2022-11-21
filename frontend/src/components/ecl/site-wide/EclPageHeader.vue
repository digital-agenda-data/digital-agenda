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
      if (typeof this.$route.meta.title === "function") {
        return this.$route.meta.title(this.$route);
      }
      return this.$route.meta.title;
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
        let label = "";
        if (!match.meta.breadcrumb) {
          continue;
        } else if (typeof match.meta.breadcrumb === "function") {
          label = match.meta.breadcrumb();
        } else {
          label = match.meta.breadcrumb;
        }

        result.push({
          id: match.name,
          text: label,
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
