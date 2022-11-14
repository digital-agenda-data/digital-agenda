<template>
  <nav
    v-ecl-init
    class="ecl-breadcrumb"
    :class="{
      'ecl-breadcrumb--negative': negative,
    }"
    aria-label="You are here:"
    data-ecl-breadcrumb="true"
    data-ecl-auto-init="Breadcrumb"
  >
    <ol class="ecl-breadcrumb__container">
      <ecl-breadcrumb-segment
        :to="firstItem.to"
        :label="firstItem.label"
        :current-page="breadcrumbs.length === 0"
      />

      <ecl-breadcrumb-segment
        class="ecl-breadcrumb__segment--ellipsis"
        data-ecl-breadcrumb-ellipsis=""
      >
        <ecl-button
          variant="ghost"
          class="ecl-breadcrumb__ellipsis"
          data-ecl-breadcrumb-ellipsis-button=""
          aria-label="Click to expand"
        >
          …
        </ecl-button>
      </ecl-breadcrumb-segment>

      <ecl-breadcrumb-segment
        v-for="(crumb, index) in breadcrumbs"
        :key="crumb.id"
        :to="crumb.to"
        :label="crumb.label"
        :current-page="index === breadcrumbs.length - 1"
        :expandable="index < breadcrumbs.length - 1"
      />
    </ol>
  </nav>
</template>

<script>
import EclBreadcrumbSegment from "@/components/ecl/navigation/EclBreadcrumbSegment.vue";
import EclButton from "@/components/ecl/EclButton.vue";

/**
 * ECL Page Header component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/navigation/breadcrumb/usage/
 *
 */
export default {
  name: "EclBreadcrumbs",
  components: { EclButton, EclBreadcrumbSegment },
  props: {
    /**
     * Items must be in the following format:
     *
     *   {
     *     id: "",          // Unique ID for the item
     *     label: "",       // Label for the item
     *     to: "",          // Link URL or Route Object (optional)
     *   }
     */
    items: {
      type: Array,
      required: true,
      validator(value) {
        // The breadcrumbs list must not be empty
        return value.length > 0;
      },
    },
    negative: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    firstItem() {
      return this.items[0];
    },
    breadcrumbs() {
      return this.items.slice(1);
    },
  },
};
</script>

<style scoped></style>
