<template>
  <ecl-form-group v-bind="{ label, helpText, required }">
    <input
      v-model="value"
      type="range"
      class="ecl-range"
      :class="`ecl-range--${size}`"
      :name="inputName"
      :max="max"
      :min="min"
      :step="step"
      :aria-label="arialLabel ?? label"
    />
  </ecl-form-group>
</template>

<script>
import EclFormGroup from "@/components/ecl/forms/EclFormGroup.vue";

/**
 * ECL Range component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/forms/range/usage/
 *
 */
export default {
  name: "EclRange",
  components: { EclFormGroup },
  props: {
    modelValue: {
      type: [Number, String],
      required: false,
      default: 0,
    },
    label: {
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
    required: {
      type: Boolean,
      required: false,
      default: false,
    },
    size: {
      type: String,
      required: false,
      default: null,
      validator(value) {
        return ["s", "m", "l"].includes(value);
      },
    },
    max: {
      type: Number,
      required: true,
    },
    min: {
      type: Number,
      required: false,
      default: 0,
    },
    step: {
      type: Number,
      required: false,
      default: 1,
    },
    arialLabel: {
      type: String,
      required: false,
      default: "",
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
