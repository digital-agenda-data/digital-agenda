<template>
  <ul
    class="ecl-site-footer__list"
    :class="{ 'ecl-site-footer__list--inline': inline }"
  >
    <li
      v-for="item in items"
      :key="item.label"
      class="ecl-site-footer__list-item"
    >
      <ecl-link
        :to="item.link"
        :label="item.label"
        class="ecl-site-footer__link"
        :icon="item.icon"
        inverted
      />
    </li>
  </ul>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "EclSiteFooterList",
  components: { EclLink },
  props: {
    /**
     * Requires an array with the following keys: link, label, icon
     */
    items: {
      type: Array,
      required: true,
    },
    inline: {
      type: Boolean,
      require: false,
      default: false,
    },
  },
};
</script>

<style scoped></style>
