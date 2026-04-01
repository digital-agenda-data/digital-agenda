<template>
  <div :class="classList">
    <p v-if="description" class="ecl-social-media-follow__description">
      {{ description }}
    </p>
    <ul class="ecl-social-media-follow__list">
      <li
        v-for="item in items"
        :key="item.link"
        class="ecl-social-media-follow__item"
      >
        <ecl-link
          :to="item.link"
          :icon="item.icon"
          icon-size="s"
          class="ecl-social-media-follow__link"
          inverted
          :alt="item.label"
        />
      </li>
    </ul>
  </div>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "EclSocialMediaFollow",
  components: { EclLink },
  props: {
    /**
     * Requires an array with the following keys: link, label, icon
     */
    items: {
      type: Array,
      required: true,
    },
    description: {
      type: String,
      required: false,
      default: null,
    },
    horizontal: {
      type: Boolean,
      required: false,
      default: false,
    },
    vertical: {
      type: Boolean,
      required: false,
      default: false,
    },
    position: {
      type: String,
      required: false,
      default: "left",
    },
  },
  computed: {
    classList() {
      const result = [
        "ecl-social-media-follow",
        `ecl-social-media-follow--${this.position}`,
      ];
      if (this.horizontal) {
        result.push("ecl-social-media-follow--horizontal");
      }
      if (this.vertical) {
        result.push("ecl-social-media-follow--vertical");
      }
      if (this.description) {
        result.push("ecl-social-media-follow--description_inline");
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
