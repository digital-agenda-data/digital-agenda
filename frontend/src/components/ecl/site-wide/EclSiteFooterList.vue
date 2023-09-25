<template>
  <ul class="ecl-site-footer__list">
    <li v-for="item in items" :key="item.id" class="ecl-site-footer__list-item">
      <ecl-link
        :to="item.link"
        :label="item.label"
        class="ecl-site-footer__link"
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
     * Requires an array with the following keys: id, link, label
     */
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped></style>
