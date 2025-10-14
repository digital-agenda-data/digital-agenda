<template>
  <div
    class="ecl-notification"
    :class="`ecl-notification--${type}`"
    data-ecl-notification=""
    role="alert"
  >
    <ecl-icon :icon="icons[type]" size="l" class="ecl-notification__icon" />

    <div class="ecl-notification__content">
      <ecl-button
        class="ecl-notification__close"
        data-ecl-notification-close=""
        variant="ghost"
        label="Close"
        icon="close-filled"
        @click="$emit('close')"
      />

      <div v-if="title" class="ecl-notification__title">
        {{ title }}
      </div>
      <div v-if="description" class="ecl-notification__description">
        {{ description }}
      </div>
    </div>
  </div>
</template>

<script>
import EclButton from "@/components/ecl/EclButton.vue";
import EclIcon from "@/components/ecl/EclIcon.vue";

/**
 * ECL Notification component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/notification/usage/
 */
export default {
  name: "EclNotification",
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
