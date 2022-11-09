<template>
  <router-link :to="to" :class="classList">
    <slot>
      <span v-if="label" class="ecl-link__label">
        {{ label }}
      </span>
    </slot>
    <ecl-icon v-if="icon" :icon="icon" size="fluid" class="ecl-link__icon" />
  </router-link>
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
      default: "default",
      validator(value) {
        return [
          "default",
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
  },
  computed: {
    classList() {
      const result = ["ecl-link", `ecl-link--${this.variant}`];

      if (this.icon) {
        result.push("ecl-link--icon");
        result.push("ecl-link--icon-after");
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
