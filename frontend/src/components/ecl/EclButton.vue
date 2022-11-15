<template>
  <button
    class="ecl-button"
    :class="`ecl-button--${variant}`"
    :aria-label="ariaLabel || label"
  >
    <span class="ecl-button__container">
      <slot>
        <span v-if="label" class="ecl-button__label" data-ecl-label="true">
          {{ label }}
        </span>
        <ecl-icon
          v-if="icon"
          :icon="icon"
          :rotate="iconRotate"
          size="xs"
          class="ecl-button__icon"
          :class="{
            // Sets extra space if there is a label before
            'ecl-button__icon--after': !!label,
          }"
        />
      </slot>
    </span>
  </button>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";

/**
 * ECL Button component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/button/usage/
 *
 * Example usages:
 *
 *  <ecl-button label="Click me" icon="corner-arrow" variant="primary" />
 *
 *  <ecl-button variant="secondary">
 *    <span>Custom label template</span>
 *  </ecl-button>
 */
export default {
  name: "EclButton",
  components: { EclIcon },
  props: {
    variant: {
      type: String,
      required: false,
      default: "primary",
      validator(value) {
        return ["primary", "secondary", "call", "ghost", "search"].includes(
          value
        );
      },
    },
    label: {
      type: String,
      required: false,
      default: null,
    },
    ariaLabel: {
      type: String,
      required: false,
      default: null,
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    iconRotate: {
      type: [String, Number],
      required: false,
      default: 0,
    },
  },
};
</script>

<style scoped></style>
