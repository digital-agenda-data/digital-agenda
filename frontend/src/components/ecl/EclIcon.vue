<template>
  <span :class="classList" aria-hidden="true" data-ecl-icon=""></span>
</template>

<script>
/**
 * ECL icon component. See full documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/icon/usage/
 *
 * Example usages:
 *
 *  <ecl-icon icon="rss" size="m" color="inverted" rotate="90" flip-vertical />
 *
 *  <ecl-icon icon="hamburger" size="l" color="primary" />
 *
 */
export default {
  name: "EclIcon",
  props: {
    // Icon name (e.g. "hamburger"). See full list here:
    // https://ec.europa.eu/component-library/ec/guidelines/iconography/
    icon: {
      type: String,
      required: true,
    },
    size: {
      type: String,
      required: false,
      default: "m",
      validator(value) {
        return ["2xs", "xs", "s", "m", "l", "xl", "2xl", "fluid"].includes(
          value,
        );
      },
    },
    color: {
      type: String,
      required: false,
      default: null,
      validator(value) {
        return ["none", "primary", "inverted"].includes(value);
      },
    },
    rotate: {
      type: [String, Number],
      required: false,
      default: "0",
      validator(value) {
        return ["0", "90", "180", "270"].includes(value.toString());
      },
    },
    flipVertical: {
      type: Boolean,
      required: false,
      default: false,
    },
    flipHorizontal: {
      type: Boolean,
      required: false,
      default: false,
    },
    inverted: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    classList() {
      const result = [
        `wt-icon-${this.icon}`,
        "ecl-icon",
        `ecl-icon--${this.size}`,
        `ecl-icon--rotate-${this.rotate}`,
        `ecl-icon--${this.icon}`,
      ];

      if (this.color) {
        result.push(`ecl-icon--${this.color}`);
      }

      if (this.flipHorizontal) {
        result.push("ecl-icon--flip-horizontal");
      }

      if (this.flipVertical) {
        result.push("ecl-icon--flip-vertical");
      }

      if (this.inverted) {
        result.push("wt-icon--inverted");
      }

      return result;
    },
  },
};
</script>

<style scoped></style>
