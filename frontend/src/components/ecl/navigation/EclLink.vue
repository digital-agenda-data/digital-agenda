<template>
  <a :href="href" :class="classList" :target="target" :rel="rel">
    <ecl-icon
      v-if="icon && iconLeft"
      :icon="icon"
      size="fluid"
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
      size="fluid"
      class="ecl-link__icon"
    />
  </a>
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
  },
  computed: {
    classList() {
      const result = ["ecl-link", `ecl-link--${this.variant}`];

      if (this.icon) {
        result.push("ecl-link--icon");

        if (this.iconLeft) {
          result.push("ecl-link--icon-before");
        } else {
          result.push("ecl-link--icon-after");
        }
      }
      return result;
    },
    isExternalLink() {
      return (
        typeof this.to === "string" &&
        (this.to.startsWith("http://") || this.to.startsWith("https://"))
      );
    },
    href() {
      if (this.isExternalLink) return this.to;
      return this.$router.resolve(this.to).fullPath;
    },
    target() {
      return this.isExternalLink ? "_blank" : undefined;
    },
    rel() {
      return this.isExternalLink ? "noreferrer noopener" : undefined;
    },
  },
};
</script>

<style scoped></style>
