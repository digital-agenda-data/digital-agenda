<template>
  <ecl-form-group v-bind="{ label, helpText, required, errors }">
    <textarea
      v-model="value"
      :rows="rows"
      :name="inputName"
      :class="classList"
      :placeholder="placeholderText"
      :disabled="disabled"
      :readonly="readOnly"
      :required="required"
      :minlength="minLength"
      :maxlength="maxLength"
    />
  </ecl-form-group>
</template>

<script>
import BaseInputField from "@/components/ecl/forms/BaseInputField.vue";
import EclFormGroup from "@/components/ecl/forms/EclFormGroup.vue";

/**
 * ECL Text Area component, see documentation here:
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
      type: [Number, String],
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
