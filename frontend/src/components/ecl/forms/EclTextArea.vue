<template>
  <ecl-form-group v-bind="{ label, helpText, required, error }">
    <textarea
      v-model="value"
      :rows="rows"
      :name="inputName"
      :class="classList"
      :placeholder="placeholderText"
      :disabled="disabled"
    />
  </ecl-form-group>
</template>

<script>
import BaseInputField from "@/components/ecl/forms/BaseInputField.vue";
import EclFormGroup from "@/components/ecl/forms/EclFormGroup.vue";

/**
 * ECL Range component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/forms/text-area/usage/
 *
 */
export default {
  name: "EclTextArea",
  components: { EclFormGroup },
  extends: BaseInputField,
  props: {
    rows: {
      type: Number,
      required: false,
      default: 5,
    },
  },
  computed: {
    className() {
      return "ecl-text-area";
    },
  },
};
</script>

<style scoped></style>
