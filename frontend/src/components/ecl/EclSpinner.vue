<template>
  <transition name="fade-delayed" appear>
    <div :class="classList">
      <svg class="ecl-spinner__loader" viewBox="25 25 50 50">
        <circle
          class="ecl-spinner__circle"
          cx="50"
          cy="50"
          r="20"
          fill="none"
          stroke-width="4px"
          stroke-miterlimit="10"
          vector-effect="non-scaling-stroke"
        ></circle>
      </svg>
      <div class="ecl-spinner__text">
        {{ text }}
      </div>
    </div>
  </transition>
</template>

<script>
/**
 * ECL Spinner component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/spinner/usage/
 *
 */
export default {
  name: "EclSpinner",
  props: {
    size: {
      type: String,
      required: false,
      default: "medium",
      validator(value) {
        return ["small", "medium", "large"].includes(value);
      },
    },
    color: {
      type: String,
      required: false,
      default: "primary",
      validator(value) {
        return ["primary", "negative"].includes(value);
      },
    },
    text: {
      type: String,
      required: false,
      default: "Loading...",
    },
    centered: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    classList() {
      const result = [
        "ecl-spinner",
        `ecl-spinner--${this.color}`,
        `ecl-spinner--${this.size}`,
        "ecl-spinner--visible",
      ];

      if (this.centered) {
        result.push("ecl-spinner--centered");
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
