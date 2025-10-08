<template>
  <div
    class="ecl-list-illustration"
    :class="{
      'ecl-list-illustration--zebra': zebra,
      [`ecl-list-illustration--col-${col}`]: col !== '1',
    }"
  >
    <ecl-spinner v-if="loading" size="large" centered class="ecl-u-ma-2xl" />
    <div
      v-for="(item, index) in items"
      v-else
      :key="item.id"
      class="ecl-list-illustration__item ecl-u-mv-s ecl-u-pa-s"
      :class="{
        'ecl-card': eclCard,
      }"
    >
      <component
        :is="item.to ? 'EclLink' : 'picture'"
        :to="item.to"
        class="ecl-picture ecl-list-illustration__picture"
        :title="item.title"
      >
        <img
          :src="item.image"
          alt=""
          class="ecl-list-illustration__image"
          :class="{
            'ecl-list-illustration__image--small': small,
            'ecl-list-illustration__image--square': square,
            'ecl-u-border-all ecl-u-border-width-1 ecl-u-border-color-grey-10':
              !eclCard,
          }"
        />
      </component>

      <div class="ecl-list-illustration__detail ecl-u-width-100">
        <ecl-label
          v-if="item.label"
          :text="item.label.text"
          :variant="item.label.variant || 'low'"
          class="ecl-u-f-r"
        />

        <div v-if="item.title" class="ecl-list-illustration__title-container">
          <div class="ecl-list-illustration__title">
            <ecl-icon
              v-if="item.icon && !item.image"
              :icon="item.icon"
              size="icon"
              class="ecl-list-illustration__icon"
            />

            <ecl-link
              v-if="item.to"
              :to="item.to"
              :label="getTitle(item, index)"
              no-visited
            />
            <template v-else>
              {{ getTitle(item, index) }}
            </template>
          </div>
        </div>
        <div class="ecl-list-illustration__description">
          <slot name="description" :item="item">
            {{ item.description }}
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclLabel from "@/components/ecl/EclLabel.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";

/**
 * ECL List with illustrations component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/list-illustration/usage/
 *
 */
export default {
  name: "EclListIllustration",
  components: { EclSpinner, EclLabel, EclLink, EclIcon },
  props: {
    /**
     * Items must be in the following format:
     *
     *   {
     *     id: '',           // unique ID for this item
     *     description: '',  // text to include in the body of the item
     *     title: '',        // (optional) text to use in the title
     *     image: '',        // (optional) image url for this item
     *     icon: '',         // (optional) cannot be used with image
     *     to: {},           // (optional) router link for this item
     *     label: '',        // (optional) add a label to the item
     *   }
     */
    items: {
      type: Array,
      required: true,
    },
    zebra: {
      type: Boolean,
      required: false,
      default: false,
    },
    eclCard: {
      type: Boolean,
      required: false,
      default: false,
    },
    square: {
      type: Boolean,
      required: false,
      default: false,
    },
    small: {
      type: Boolean,
      required: false,
      default: false,
    },
    showIndex: {
      type: Boolean,
      required: false,
      default: false,
    },
    col: {
      type: String,
      required: false,
      default: "1",
      validator(value) {
        return ["1", "2", "3", "4"].includes(value);
      },
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    getTitle(item, index) {
      if (!this.showIndex) {
        return item.title;
      }

      return `${index + 1}. ${item.title}`;
    },
  },
};
</script>

<style scoped lang="scss">
// Hide images on small screens
.ecl-list-illustration__image {
  display: none;

  @media (min-width: 768px) {
    display: block;
  }
}

// Add extra class "small" that keeps the image ratio, but
// makes it smaller.
@media screen and (min-width: 768px) {
  .ecl-list-illustration__image--small:not(
    .ecl-list-illustration__image--square
  ) {
    width: 9rem;
  }
}
</style>
