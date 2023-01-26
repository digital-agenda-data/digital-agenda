<template>
  <article class="ecl-card">
    <div
      v-if="image"
      class="ecl-card__image"
      aria-label="card image"
      role="img"
      :style="`background-image: url(${image});`"
    />

    <div class="ecl-card__body">
      <div class="ecl-content-block ecl-card__content-block">
        <ul v-if="labels" class="ecl-content-block__label-container">
          <li
            v-for="label in normalizedLabels"
            :key="label.id"
            class="ecl-content-block__label-item"
          >
            <ecl-label :text="label.text" :variant="label.variant" />
          </li>
        </ul>
        <div v-if="title" class="ecl-content-block__title">
          <component :is="to ? 'EclLink' : 'span'" :to="to" no-visited>
            {{ title }}
          </component>
        </div>
        <div v-if="description" class="ecl-content-block__description">
          {{ description }}
        </div>
      </div>
    </div>
  </article>
</template>

<script>
import EclLabel from "@/components/ecl/EclLabel.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { forceArray } from "@/lib/utils";

/**
 * ECL Card component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/card/usage/
 *
 * NOTE! Not all features are implemented, only the bare minimum required.
 */
export default {
  name: "EclCard",
  components: { EclLink, EclLabel },
  props: {
    image: {
      type: String,
      required: false,
      default: null,
    },
    to: {
      type: [Object, String],
      required: false,
      default: null,
    },
    title: {
      type: String,
      required: false,
      default: null,
    },
    description: {
      type: String,
      required: false,
      default: null,
    },
    labels: {
      type: [Object, Array, String],
      required: false,
      default: null,
    },
  },
  computed: {
    normalizedLabels() {
      const result = [];

      for (let item of forceArray(this.labels)) {
        if (!item) {
          continue;
        }

        if (typeof item === "string") {
          item = { text: item };
        }

        item.id ??= item.text;
        result.push(item);
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
