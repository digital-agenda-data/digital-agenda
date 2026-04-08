<template>
  <ecl-form-group v-bind="{ label, helpText, required, errors }">
    <div
      v-for="item in items"
      :key="item.value"
      class="ecl-radio"
      :class="{ 'ecl-radio--binary': binary }"
    >
      <input
        :id="`${inputName}-${item.value}`"
        :name="`${inputName}-${item.value}`"
        class="ecl-radio__input"
        type="radio"
        :value="item.value"
        :checked="value === item.value"
        required
        @click="value = item.value"
      />
      <label class="ecl-radio__label" :for="`${inputName}-${item.value}`">
        <span class="ecl-radio__box">
          <span class="ecl-radio__box-inner"></span>
        </span>
        <span class="ecl-radio__text">
          {{ item.label }}
        </span>
      </label>
    </div>
  </ecl-form-group>
</template>

<script>
import BaseInputField from "@/components/ecl/forms/BaseInputField.vue";
import EclFormGroup from "@/components/ecl/forms/EclFormGroup.vue";
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclRadioGroup",
  components: { EclFormGroup },
  extends: BaseInputField,
  props: {
    binary: {
      type: Boolean,
      required: false,
      default: false,
    },
    items: {
      type: Array,
      required: true,
    },
  },
});
</script>
