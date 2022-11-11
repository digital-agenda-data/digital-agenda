<template>
  <div class="ecl-form-group">
    <label v-if="label" class="ecl-form-label">
      {{ label }}
      <span v-if="required" class="ecl-form-label__required">*</span>
    </label>
    <div v-if="helpText" class="ecl-help-block">
      {{ helpText }}
    </div>
    <div :class="classList">
      <select
        v-model="value"
        v-ecl-init="multiple"
        class="ecl-select"
        :required="required"
        :multiple="multiple"
        v-bind="dataAttrs"
      >
        <option
          v-if="placeholderText && !multiple"
          value=""
          :disabled="required"
        >
          {{ placeholderText }}
        </option>

        <template v-for="item in items" :key="item.id">
          <optgroup
            v-if="item.children"
            :label="item.text"
            :disabled="item.disabled"
          >
            <option
              v-for="child in item.children"
              :key="child.id"
              :value="child.id"
              :disabled="child.disabled"
            >
              {{ child.text }}
            </option>
          </optgroup>
          <option v-else :value="item.id" :disabled="item.disabled">
            {{ item.text }}
          </option>
        </template>
      </select>
      <div class="ecl-select__icon">
        <ecl-icon
          size="s"
          icon="corner-arrow"
          rotate="180"
          class="ecl-select__icon-shape"
        />
      </div>
    </div>
  </div>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";
/**
 * ECL Select component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/forms/select/usage/
 *
 */
export default {
  name: "EclSelect",
  components: { EclIcon },
  props: {
    /**
     * Items must be in the following format:
     *
     *   {
     *     id: "",          // Unique ID for the item or grop
     *     text: "",        // Label for the item or group
     *     disabled: false, // Disable an item or a group
     *     children: [],    // If present will form an optgroup
     *   }
     */
    items: {
      type: Array,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: null,
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
    multiple: {
      type: Boolean,
      required: false,
      default: false,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    size: {
      type: String,
      required: false,
      default: "m",
      validator(value) {
        return ["s", "m", "l"].includes(value);
      },
    },
    placeholderText: {
      type: String,
      required: false,
      default: "Select an item",
    },
    searchText: {
      type: String,
      required: false,
      default: "Enter keyword",
    },
    noResultsText: {
      type: String,
      required: false,
      default: "No results found",
    },
    modelValue: {
      type: [String, Array],
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
    classList() {
      const result = [
        "ecl-select__container",
        `ecl-select__container--${this.size}`,
      ];
      if (this.disabled) {
        result.push("ecl-select__container--disabled");
      }
      return result;
    },
    dataAttrs() {
      if (!this.multiple) return {};

      // Only the multiselect requires all of these and requires init.
      return {
        "data-ecl-auto-init": "Select",
        "data-ecl-select-default": this.placeholderText,
        "data-ecl-select-search": this.searchText,
        "data-ecl-select-no-results": this.noResultsText,
        "data-ecl-select-all": "Select all",
        "data-ecl-select-clear-all": "Clear all",
        "data-ecl-select-close": "Close",
      };
    },
  },
};
</script>

<style scoped></style>
