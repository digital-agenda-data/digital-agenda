<template>
  <nav
    v-ecl-init
    class="ecl-category-filter"
    data-ecl-category-filter=""
    data-ecl-auto-init="CategoryFilter"
  >
    <ecl-category-filter-list :items="items" />
  </nav>
</template>

<script>
import EclCategoryFilterList from "@/components/ecl/EclCategoryFilterList.vue";

/**
 * ECL Category Filter component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/category-filter/usage/
 */
export default {
  name: "EclCategoryFilter",
  components: { EclCategoryFilterList },
  props: {
    /**
     * See docs in EclCategoryFilterList for this prop
     */
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped></style>
