<template>
  <ul class="ecl-category-filter__list">
    <li
      v-for="item in items"
      :key="item.id"
      class="ecl-category-filter__list-item"
      aria-expanded="false"
    >
      <router-link
        :to="item.to"
        class="ecl-category-filter__item"
        :class="{
          'ecl-category-filter__item--has-children': item.children?.length > 0,
          [`ecl-category-filter__item--level-${level}`]: true,
        }"
        active-class="ecl-category-filter__item--current"
      >
        <ecl-icon
          v-if="level > 1 && item.children?.length > 0"
          icon="solid-arrow"
          class="ecl-category-filter__item-icon"
          size="m"
          rotate="90"
        />

        {{ item.text }}

        <ecl-icon
          v-if="level === 1 && item.children?.length > 0"
          icon="corner-arrow"
          class="ecl-category-filter__item-icon"
          size="xs"
          rotate="180"
        />
      </router-link>

      <!-- Recursive call for children -->
      <ecl-category-filter-list
        v-if="item.children?.length > 0"
        :items="item.children"
        :level="level + 1"
      />
    </li>
  </ul>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";

/**
 * ECL Category Filter List component, part of the Category Filter component see
 * documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/category-filter/usage/
 */
export default {
  name: "EclCategoryFilterList",
  components: { EclIcon },
  props: {
    /**
     * Items must be in the following format:
     *
     *   {
     *     id: "",          // Unique ID for the item
     *     to: "",          // Link URL or Route Object
     *     text: "",        // Label for the item
     *     children: [],    // (optional) Sub items for this item, up to 4 levels deep
     *   }
     */
    items: {
      type: Array,
      required: true,
    },
    /**
     * Keep track of the depth while in the recursion
     */
    level: {
      type: Number,
      required: false,
      default: 1,
      validator(value) {
        return 1 <= value <= 4;
      },
    },
  },
};
</script>

<style scoped></style>
