<template>
  <ecl-form-group v-bind="{ label, helpText, required, error }">
    <input
      v-model="value"
      :type="type"
      :name="inputName"
      :class="classList"
      :placeholder="placeholderText"
      :disabled="disabled"
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
 * ECL Range component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/forms/text-field/usage/
 *
 */
export default {
  name: "EclTextField",
  components: { EclFormGroup },
  extends: BaseInputField,
  props: {
    type: {
      type: String,
      required: false,
      default: "text",
    },
  },
  computed: {
    className() {
      return "ecl-text-input";
    },
  },
};
</script>

<style scoped></style>
