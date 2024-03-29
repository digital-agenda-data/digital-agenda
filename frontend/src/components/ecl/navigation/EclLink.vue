<template>
  <component
    :is="isExternalLink ? 'a' : 'RouterLink'"
    :class="classList"
    v-bind="bindAttrs"
    :download="downloadClass ? '' : undefined"
  >
    <ecl-icon
      v-if="icon && iconLeft"
      :icon="icon"
      :rotate="iconRotate"
      :size="iconSize"
      class="ecl-link__icon"
    />
    <slot>
      <span v-if="label" class="ecl-link__label">
        {{ label }}
      </span>
    </slot>
    <ecl-icon
      v-if="icon && !iconLeft"
      :icon="icon"
      :rotate="iconRotate"
      :size="iconSize"
      class="ecl-link__icon"
    />
  </component>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";

/**
 * ECL Link component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/navigation/link/usage/
 *
 * Example usages:
 *
 *  <ecl-link to="http://example.com" icon="external" label="External link" />
 *
 *  <ecl-link
 *    :to="{ name: 'home' }"
 *    variant="primary"
 *    label="Home"
 *    aria-label="Home Page"
 *  />
 *
 *  <ecl-link to="/foo">
 *    <img src="#" />
 *  </ecl-link>
 */
export default {
  name: "EclLink",
  components: { EclIcon },
  props: {
    to: {
      type: [Object, String],
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: null,
    },
    variant: {
      type: String,
      required: false,
      default: "standalone",
      validator(value) {
        return [
          "standalone",
          "cta",
          "primary",
          "secondary",
          "negative",
          "none",
        ].includes(value);
      },
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    iconLeft: {
      type: Boolean,
      required: false,
      default: false,
    },
    iconRotate: {
      type: [String, Number],
      required: false,
      default: "0",
    },
    iconSize: {
      type: String,
      required: false,
      default: "fluid",
      validator(value) {
        return ["2xs", "xs", "s", "m", "l", "xl", "2xl", "fluid"].includes(
          value,
        );
      },
    },
    noVisited: {
      type: Boolean,
      required: false,
      default: false,
    },
    // Add tracking download class if set
    downloadClass: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    classList() {
      const result = [];
      if (this.downloadClass) {
        // Class used to track download links with Europa Analytics
        result.push("piwik_download");
      }

      if (this.variant !== "none") {
        result.push("ecl-link");
        result.push(`ecl-link--${this.variant}`);
      }

      if (this.icon) {
        result.push("ecl-link--icon");

        if (this.iconLeft) {
          result.push("ecl-link--icon-before");
        } else {
          result.push("ecl-link--icon-after");
        }
      }

      if (this.noVisited) {
        result.push("ecl-link--no-visited");
      }

      return result;
    },
    isExternalLink() {
      return (
        typeof this.to === "string" &&
        (this.to.startsWith("http://") ||
          this.to.startsWith("https://") ||
          this.to.startsWith("mailto:"))
      );
    },
    bindAttrs() {
      if (this.isExternalLink) {
        return {
          target: "_blank",
          rel: "noreferrer noopener",
          href: this.to,
        };
      }

      return {
        to: this.to,
      };
    },
  },
};
</script>

<style scoped></style>
