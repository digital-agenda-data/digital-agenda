<template>
  <div class="ecl-form-group">
    <label v-if="label" class="ecl-form-label">
      {{ label }}
      <span v-if="required === true" class="ecl-form-label__required">*</span>
      <span v-else-if="required === false" class="ecl-form-label__optional">
        (optional)
      </span>
    </label>
    <div v-if="helpText" class="ecl-help-block">
      {{ helpText }}
    </div>
    <div v-if="error" class="ecl-feedback-message">
      <ecl-icon icon="error" size="m" class="ecl-feedback-message__icon" />
      {{ error }}
    </div>
    <slot></slot>
  </div>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";

export default {
  name: "EclFormGroup",
  components: { EclIcon },
  props: {
    label: {
      type: String,
      required: false,
      default: "",
    },
    helpText: {
      type: String,
      required: false,
      default: "",
    },
    required: {
      type: Boolean,
      required: false,
      default: null,
    },
    error: {
      type: String,
      required: false,
      default: "",
    },
  },
};
</script>

<style scoped></style>
