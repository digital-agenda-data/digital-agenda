<template>
  <div class="ecl-form-group">
    <label v-if="label" class="ecl-form-label">
      {{ label }}
      <span v-if="required" class="ecl-form-label__required">*</span>
      <span v-else class="ecl-form-label__optional">(optional)</span>
    </label>
    <div v-if="helpText" class="ecl-help-block">
      {{ helpText }}
    </div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "EclFormGroup",
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
      default: false,
    },
  },
};
</script>

<style scoped></style>
