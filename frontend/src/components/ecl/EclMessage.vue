<template>
  <div
    class="ecl-message"
    :class="`ecl-message--${type}`"
    data-ecl-message=""
    role="alert"
  >
    <ecl-icon :icon="icons[type]" size="l" class="ecl-message__icon" />

    <div class="ecl-message__content">
      <ecl-button
        class="ecl-message__close"
        data-ecl-message-close=""
        variant="ghost"
        label="Close"
        icon="close-filled"
        @click="$emit('close')"
      />

      <div v-if="title" class="ecl-message__title">
        {{ title }}
      </div>
      <div v-if="description" class="ecl-message__description">
        {{ description }}
      </div>
    </div>
  </div>
</template>

<script>
import EclButton from "@/components/ecl/EclButton.vue";
import EclIcon from "@/components/ecl/EclIcon.vue";

/**
 * ECL Message component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/message/usage/
 */
export default {
  name: "EclMessage",
  components: { EclButton, EclIcon },
  props: {
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
    type: {
      type: String,
      required: false,
      default: "info",
      validator(value) {
        return ["info", "success", "warning", "error"].includes(value);
      },
    },
  },
  emits: ["close"],
  data() {
    return {
      icons: {
        info: "information",
        success: "success",
        warning: "warning",
        error: "error",
      },
    };
  },
};
</script>

<style scoped></style>
