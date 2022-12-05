<template>
  <div class="ecl-checkbox">
    <input
      v-model="value"
      :name="inputName"
      type="checkbox"
      class="ecl-checkbox__input"
      :value="inputName"
    />

    <label class="ecl-checkbox__label">
      <span class="ecl-checkbox__box">
        <ecl-icon icon="check" size="m" class="ecl-checkbox__icon" />
      </span>

      <span class="ecl-checkbox__text">
        {{ label }}
      </span>
    </label>

    <div id="helper-default-1" class="ecl-checkbox__help">
      {{ helpText }}
    </div>
  </div>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";

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
