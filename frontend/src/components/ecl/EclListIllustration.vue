<template>
  <div
    class="ecl-list-illustration"
    :class="{
      'ecl-list-illustration--zebra': zebra,
      [`ecl-list-illustration--col-${col}`]: col !== '1',
    }"
  >
    <div
      v-for="item in items"
      :key="item.id"
      class="ecl-list-illustration__item"
    >
      <component
        :is="item.to ? 'EclLink' : 'div'"
        :to="item.to"
        class="ecl-list-illustration__image"
        :class="{
          'ecl-list-illustration__image--square': square,
        }"
        role="img"
        :style="`background-image: url(${item.image});`"
        tabindex="-1"
      />

      <div class="ecl-list-illustration__detail">
        <ecl-label
          v-if="item.label"
          :text="item.label"
          :variant="item.labelVariant || 'low'"
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
              :label="item.title"
              no-visited
            />
            <template v-else>
              {{ item.title }}
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

/**
 * ECL List with illustrations component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/list-illustration/usage/
 *
 */
export default {
  name: "EclListIllustration",
  components: { EclLabel, EclLink, EclIcon },
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
     *     labelVariant: '', // (optional) default to 'low'
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
    square: {
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
  },
};
</script>

<style scoped></style>
