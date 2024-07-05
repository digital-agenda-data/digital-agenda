<template>
  <ecl-form-group v-bind="{ label, helpText, required }">
    <div :class="classList">
      <vue-multiselect
        ref="multiselect"
        v-model="value"
        :options="items"
        :limit="limitDisplaySelected"
        :placeholder="placeholderText"
        :loading="loading"
        :multiple="multiple"
        :disabled="disabled || loading"
        :close-on-select="!multiple"
        :allow-empty="allowedEmpty"
        :name="inputName"
        :data-name="inputName"
        :data-loading="loading"
        label="text"
        track-by="id"
        :group-label="hasGroups ? 'text' : undefined"
        :group-values="hasGroups ? 'children' : undefined"
        select-label=""
        selected-label=""
        deselect-label=""
        select-group-label=""
        deselect-group-label=""
        @open="onOpen"
      >
        <template #limit>
          <strong class="multiselect__tag">
            {{ modelValueSet.size }} out of {{ itemsById.size }} selected
          </strong>
        </template>

        <template v-if="multiple" #beforeList>
          <li class="multiselect__element" @click="toggleAll">
            <span class="multiselect__option">
              <ecl-checkbox
                :label="`Select all (${itemsById.size})`"
                :model-value="modelValueSet.size === itemsById.size"
              />
            </span>
          </li>
        </template>

        <template #option="{ option }">
          <template v-if="option.$groupLabel">
            {{ option.$groupLabel }}
          </template>
          <ecl-checkbox
            v-else-if="multiple"
            :label="option.text"
            :model-value="modelValueSet.has(option.id)"
          />
          <template v-else>
            {{ option.text }}
          </template>
        </template>
      </vue-multiselect>
    </div>
  </ecl-form-group>
</template>

<script>
import VueMultiselect from "vue-multiselect";
import EclFormGroup from "@/components/ecl/forms/EclFormGroup.vue";
import EclCheckbox from "@/components/ecl/forms/EclCheckbox.vue";
import { forceArray } from "@/lib/utils";

/**
 * ECL Select adaptation based on vue-multiselect. The regular ECL select component
 * doesn't play nice with Vue components, as it manually triggers native events
 * confusing v-model bindings.
 */
export default {
  name: "EclSelect",
  components: { EclCheckbox, EclFormGroup, VueMultiselect },
  props: {
    /**
     * Items must be in the following format:
     *
     *   {
     *     id: "",          // Unique ID for the item or grop
     *     text: "",        // Label for the item or group
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
      default: null,
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
      default: null,
      validator(value) {
        return ["s", "m", "l"].includes(value);
      },
    },
    placeholderText: {
      type: String,
      required: false,
      default: "Select an item",
    },
    modelValue: {
      type: [String, Array, Object],
      required: false,
      default: "",
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  computed: {
    allowedEmpty() {
      return this.multiple || this.required === false;
    },
    hasGroups() {
      return this.items.some((item) => !!item.children);
    },
    modelValueSet() {
      return new Set(forceArray(this.modelValue));
    },
    value: {
      get() {
        if (Array.isArray(this.modelValue)) {
          return this.modelValue
            .map((val) => this.itemsById.get(val))
            .filter((item) => !!item);
        } else {
          return this.itemsById.get(this.modelValue);
        }
      },
      set(value) {
        if (!this.multiple) {
          this.$emit("update:modelValue", value?.id);
        } else {
          this.$emit(
            "update:modelValue",
            value.map((item) => item.id),
          );
        }
      },
    },
    itemsById() {
      const result = new Map();

      for (const item of this.items) {
        for (const child of item.children || []) {
          result.set(child.id, child);
        }

        result.set(item.id, item);
      }
      return result;
    },
    classList() {
      const result = ["ecl-select__container"];

      if (this.size) {
        result.push(`ecl-select__container--${this.size}`);
      }
      if (this.disabled) {
        result.push("ecl-select__container--disabled");
      }
      if (this.multiple) {
        result.push("ecl-select__container--multiple");
      }
      if (this.hasGroups) {
        result.push("ecl-select__container--grouped");
      }
      return result;
    },
    // Controls how many selected items are displayed
    limitDisplaySelected() {
      if (!this.multiple) {
        return 1;
      }

      if (this.value && this.value.length > 2) {
        // Don't show any and have the #limit slot
        // take over to show the count out of text
        return 0;
      }

      return 2;
    },
  },
  methods: {
    toggleAll() {
      if (this.modelValueSet.size === this.itemsById.size) {
        this.$emit("update:modelValue", []);
      } else {
        this.$emit("update:modelValue", Array.from(this.itemsById.keys()));
      }
    },
    onOpen() {
      this.$nextTick(() => {
        this.$el
          .querySelector(".multiselect__option--selected")
          ?.scrollIntoView({ block: "nearest" });
      });
    },
  },
};
</script>

<style scoped></style>
