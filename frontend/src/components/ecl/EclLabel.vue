<template>
  <span class="ecl-label" :class="` ecl-label--${variant}`">
    {{ text }}
  </span>
</template>

<script>
/**
 * ECL Label component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/label/usage/
 *
 */
export default {
  name: "EclLabel",
  props: {
    text: {
      type: String,
      required: true,
    },
    variant: {
      type: String,
      required: false,
      default: "low",
      validator(value) {
        return ["low", "medium", "high", "highlight"].includes(value);
      },
    },
  },
};
</script>

<style scoped></style>
