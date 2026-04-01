<template>
  <div
    v-ecl-init
    class="ecl-tabs"
    data-ecl-tabs="true"
    data-ecl-auto-init="Tabs"
  >
    <div class="ecl-tabs__container">
      <div class="ecl-tabs__list" role="tablist">
        <router-link
          v-for="item in items"
          :key="item.id"
          v-slot="{ isActive }"
          :to="item.to"
          custom
        >
          <div class="ecl-tabs__item">
            <ecl-link
              :to="item.to"
              class="ecl-tabs__link"
              :class="{ 'ecl-tabs__link--active': isActive }"
              :label="item.text"
              role="tab"
              tabindex="-1"
              :aria-selected="isActive"
            />
          </div>
        </router-link>
        <div class="ecl-tabs__item ecl-tabs__item--more">
          <ecl-button
            v-show="!hideShowMore"
            class="ecl-tabs__toggle"
            variant="tertiary"
            label="Show more"
            icon="corner-arrow"
            icon-size="fluid"
            icon-rotate="180"
            tabindex="-1"
            type="button"
            aria-hidden="true"
          />
        </div>
      </div>
    </div>
    <div v-show="!hideControls" class="ecl-tabs__controls">
      <ecl-button
        variant="tertiary"
        icon-only
        icon="corner-arrow"
        icon-rotate="270"
        class="ecl-tabs__prev ecl-tabs__item--hidden"
        tabindex="-1"
        label="Previous"
        aria-hidden="true"
      />
      <ecl-button
        variant="tertiary"
        icon-only
        icon="corner-arrow"
        icon-rotate="90"
        class="ecl-tabs__next ecl-tabs__item--hidden"
        tabindex="-1"
        label="Next"
        aria-hidden="true"
      />
    </div>
  </div>
</template>

<script>
import EclButton from "@/components/ecl/EclButton.vue";
import EclIcon from "@/components/ecl/EclIcon.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "EclTabs",
  components: { EclLink, EclIcon, EclButton },
  props: {
    /**
     * Items must be in the following format:
     *
     *   {
     *     id: "",          // Unique ID for the item
     *     to: "",          // Link URL or Route Object
     *     text: "",        // Label for the item
     *   }
     */
    items: {
      type: Array,
      required: true,
      validator(value) {
        // The breadcrumbs list must not be empty
        return value.length > 0;
      },
    },
    hideControls: {
      type: Boolean,
      required: false,
      default: false,
    },
    hideShowMore: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
};
</script>

<style scoped></style>
