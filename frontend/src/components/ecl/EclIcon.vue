<template>
  <svg :class="classList" focusable="false" aria-hidden="true">
    <use :href="href"></use>
  </svg>
</template>

<script>
import iconSpritesURL from "@ecl/preset-ec/dist/images/icons/sprites/icons.svg?url";
import socialMediaSpritesURL from "@ecl/preset-ec/dist/images/icons-social-media/sprites/icons-social-media.svg";

import spritesValidIcons from "@ecl/preset-ec/dist/images/icons/lists/all.json";
import socialMediaValidIcons from "@ecl/preset-ec/dist/images/icons-social-media/lists/social-media.json";

const allIcons = Object.fromEntries([
  ...spritesValidIcons.map((icon) => [icon, iconSpritesURL]),
  ...socialMediaValidIcons.map((icon) => [icon, socialMediaSpritesURL]),
]);

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
      validator(value) {
        return !!allIcons[value];
      },
    },
    size: {
      type: String,
      required: false,
      default: "m",
      validator(value) {
        return ["2xs", "xs", "s", "m", "l", "xl", "2xl", "fluid"].includes(
          value
        );
      },
    },
    color: {
      type: String,
      required: false,
      default: "none",
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
  },
  computed: {
    href() {
      return allIcons[this.icon] + "#" + this.icon;
    },
    classList() {
      const result = [
        "ecl-icon",
        `ecl-icon--${this.size}`,
        `ecl-icon--${this.color}`,
        `ecl-icon--rotate-${this.rotate}`,
      ];

      if (this.flipHorizontal) {
        result.push("ecl-icon--flip-horizontal");
      }

      if (this.flipVertical) {
        result.push("ecl-icon--flip-vertical");
      }

      return result;
    },
  },
};
</script>

<style scoped></style>
