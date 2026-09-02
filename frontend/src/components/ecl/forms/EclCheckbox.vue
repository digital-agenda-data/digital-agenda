<template>
  <fieldset class="ecl-form-group">
    <legend
      v-if="groupLabel"
      :id="inputName + '-label'"
      class="ecl-form-label-wrapper"
    >
      <span
        class="ecl-form-label"
        :class="{ 'ecl-form-label--invalid': errors?.length > 0 }"
      >
        {{ groupLabel }}
      </span>
      <span v-if="helpText" class="ecl-help-block--hidden">{{ helpText }}</span>
      <span v-if="required" class="ecl-form-label__required">(required)</span>
      <span v-else class="ecl-form-label__optional">(optional)</span>
    </legend>
    <div
      v-if="helpText"
      :id="inputName + '-helper'"
      class="ecl-help-block"
      aria-hidden="true"
    >
      {{ helpText }}
    </div>
    <div
      class="ecl-checkbox ecl-checkbox--single"
      :class="{ 'ecl-checkbox--invalid': errors?.length > 0 }"
    >
      <input
        :id="inputName + '-1'"
        v-model="value"
        :name="inputName"
        class="ecl-checkbox__input"
        type="checkbox"
        :value="inputName"
        :checked="value"
        :required="required"
      />
      <label :for="inputName + '-1'" class="ecl-checkbox__label">
        <span class="ecl-checkbox__box">
          <ecl-icon icon="check" size="xs" class="ecl-checkbox__icon" />
        </span>
        <span class="ecl-checkbox__text">{{ label }}</span>
        <span v-if="required" class="ecl-form-label__required">(required)</span>
        <span v-else class="ecl-form-label__optional">(optional)</span>
      </label>
    </div>
    <div
      v-for="(msg, index) in errors ?? []"
      :id="inputName + '-invalid'"
      :key="index"
      class="ecl-feedback-message"
    >
      <ecl-icon icon="error" size="m" class="ecl-feedback-message__icon" />
      {{ msg }}
    </div>
  </fieldset>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";
// TODO: This only works in single checkbox mode, although ECL support
// TODO: checkbox group as well.
/**
 * ECL Checkbox component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/forms/checkbox/usage/
 */
export default {
  name: "EclCheckbox",
  components: { EclIcon },
  props: {
    modelValue: {
      type: Boolean,
      required: false,
      default: false,
    },
    label: {
      type: String,
      required: false,
      default: null,
    },
    groupLabel: {
      type: String,
      required: false,
      default: null,
    },
    inputName: {
      type: String,
      required: false,
      default: "",
    },
    helpText: {
      type: String,
      required: false,
      default: null,
    },
    errors: {
      type: Array,
      required: false,
      default: null,
    },
    required: {
      type: Boolean,
      required: false,
      default: null,
    },
  },
  emits: ["update:modelValue"],
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
};
</script>

<style scoped></style>
