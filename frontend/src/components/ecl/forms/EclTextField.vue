<template>
  <ecl-form-group
    v-bind="{ label, helpText, required, errors }"
    :class="{
      'copy-on-click': copyOnClick,
    }"
  >
    <ecl-popover
      ref="popover"
      :content-id="inputName + '-popover'"
      manual-control
    >
      <template #toggle>
        <input
          ref="input"
          v-model="value"
          :type="type"
          :name="inputName"
          :class="classList"
          :placeholder="placeholderText"
          :disabled="disabled"
          :readonly="readOnly"
          :required="required"
          :minlength="minLength"
          :maxlength="maxLength"
          @click="copyToClipboard"
        />
      </template>

      <template #default>Link copied to clipboard</template>
    </ecl-popover>
  </ecl-form-group>
</template>

<script>
import EclPopover from "@/components/ecl/EclPopover.vue";
import BaseInputField from "@/components/ecl/forms/BaseInputField.vue";
import EclFormGroup from "@/components/ecl/forms/EclFormGroup.vue";
import { useMessagesStore } from "@/stores/messagesStore";
import { mapActions } from "pinia";

/**
 * ECL Text Field component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/forms/text-field/usage/
 *
 */
export default {
  name: "EclTextField",
  components: { EclPopover, EclFormGroup },
  extends: BaseInputField,
  props: {
    type: {
      type: String,
      required: false,
      default: "text",
    },
    copyOnClick: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    className() {
      return "ecl-text-input";
    },
  },
  methods: {
    ...mapActions(useMessagesStore, ["addMessage"]),
    copyToClipboard() {
      if (!this.copyOnClick) return;

      const el = this.$refs.input;
      el.setSelectionRange(0, el.value.length);

      this.copyURL(el.value);
    },
    async copyURL(text) {
      try {
        await navigator.clipboard.writeText(text);
        this.$refs.popover.openPopover();
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style scoped>
.copy-on-click input {
  cursor: copy;
}
</style>
