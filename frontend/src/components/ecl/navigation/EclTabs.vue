<template>
  <nav
    v-ecl-init
    class="ecl-tabs"
    data-ecl-tabs="true"
    data-ecl-auto-init="Tabs"
  >
    <div class="ecl-tabs__container">
      <ul class="ecl-tabs__list" role="tablist">
        <li
          v-for="item in items"
          :key="item.id"
          class="ecl-tabs__item"
          role="presentation"
        >
          <router-link
            :to="item.to"
            class="ecl-link ecl-tabs__link"
            active-class="ecl-tabs__link--active"
            role="tab"
            tabindex="-1"
          >
            {{ item.text }}
          </router-link>
        </li>
        <li class="ecl-tabs__item ecl-tabs__item--more" role="presentation">
          <ecl-button
            class="ecl-tabs__toggle"
            variant="secondary"
            label="More (%d)"
            icon="corner-arrow"
            icon-rotate="180"
            tabindex="-1"
            type="button"
          />
        </li>
      </ul>
    </div>
    <div v-show="!hideControls" class="ecl-tabs__controls">
      <button class="ecl-tabs__prev" aria-hidden="true">
        <ecl-icon
          icon="corner-arrow"
          color="inverted"
          rotate="270"
          class="ecl-u-d-block"
          focusable="false"
          aria-hidden="true"
        />
        <span class="ecl-u-sr-only"></span>
      </button>
      <button class="ecl-tabs__next" aria-hidden="true">
        <ecl-icon
          icon="corner-arrow"
          color="inverted"
          rotate="90"
          class="ecl-u-d-block"
          focusable="false"
          aria-hidden="true"
        />
        <span class="ecl-u-sr-only"></span>
      </button>
    </div>
  </nav>
</template>

<script>
import EclButton from "@/components/ecl/EclButton.vue";
import EclIcon from "@/components/ecl/EclIcon.vue";

export default {
  name: "EclTabs",
  components: { EclIcon, EclButton },
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
  },
};
</script>

<style scoped></style>
