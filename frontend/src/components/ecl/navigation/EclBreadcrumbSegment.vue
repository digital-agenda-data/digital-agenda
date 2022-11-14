<template>
  <li
    class="ecl-breadcrumb__segment"
    :data-ecl-breadcrumb-item="expandable ? 'expandable' : 'static'"
    :class="{
      'ecl-breadcrumb__current-page': currentPage,
    }"
  >
    <slot>
      <ecl-link
        v-if="to && !currentPage"
        :to="to"
        no-visited
        class="ecl-breadcrumb__link"
        :label="label"
      />
      <template v-else>
        {{ label }}
      </template>
    </slot>

    <ecl-icon
      v-if="!currentPage"
      icon="corner-arrow"
      size="2xs"
      rotate="90"
      class="ecl-breadcrumb__icon"
      aria-hidden="true"
      role="presentation"
    />
  </li>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclIcon from "@/components/ecl/EclIcon.vue";

/**
 * ECL Breadcrumb Segment, part of the ECL Breadcrumb component, see docs here:
 *
 *  https://ec.europa.eu/component-library/ec/components/navigation/breadcrumb/usage/
 *
 */
export default {
  name: "EclBreadcrumbSegment",
  components: { EclIcon, EclLink },
  props: {
    to: {
      type: [String, Object],
      required: false,
      default: null,
    },
    label: {
      type: String,
      required: false,
      default: null,
    },
    currentPage: {
      type: Boolean,
      required: false,
      default: false,
    },
    expandable: {
      type: Boolean,
      required: false,
      default: false,
    },
    noIcon: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
};
</script>

<style scoped></style>
