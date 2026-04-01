<template>
  <button :class="classList" :aria-label="ariaLabel || label">
    <span class="ecl-button__container">
      <slot>
        <ecl-icon
          v-if="icon"
          :icon="icon"
          :rotate="iconRotate"
          :size="iconSize"
          class="ecl-button__icon"
        />
        <span v-if="label" class="ecl-button__label" data-ecl-label="true">
          {{ label }}
        </span>
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
        return ["primary", "secondary", "call", "ghost", "neutral"].includes(
          value,
        );
      },
    },
    size: {
      type: String,
      required: false,
      default: null,
      validator(value) {
        return ["s", "m", "l"].includes(value);
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
    iconSize: {
      type: String,
      required: false,
      default: "xs",
      validator(value) {
        return ["2xs", "xs", "s", "m", "l", "xl", "2xl", "fluid"].includes(
          value,
        );
      },
    },
    iconOnly: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    classList() {
      const result = ["ecl-button", `ecl-button--${this.variant}`];
      if (this.iconOnly) {
        result.push("ecl-button--icon-only");
      }
      if (this.size) {
        result.push(`ecl-button--${this.size}`);
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
