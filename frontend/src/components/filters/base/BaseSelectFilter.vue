<template>
  <ecl-select
    v-show="!hidden && isVisible"
    v-model="modelValue"
    :items="items"
    :loading="loading"
    :multiple="multiple"
    :required="required"
    :label="labelWithAxis"
    :input-name="queryName"
    :size="size"
  />
</template>

<script>
import EclSelect from "@/components/ecl/forms/EclSelect.vue";
import { api } from "@/lib/api";
import { useFilterStore } from "@/stores/filterStore";
import { getDisplay, randomChoice } from "@/lib/utils";
import { mapState } from "pinia";
import { useChartGroupStore } from "@/stores/chartGroupStore";

/**
 * Base component for all filters. Extend this component and
 * override various computed properties to create a new filter.
 */
export default {
  name: "BaseFilter",
  components: { EclSelect },
  props: {
    /**
     * The axis used for:
     *  - storing data in the filterStore
     *  - getting data from the filterStore
     *  - appending to the query parameter name in the Route
     *    (e.g. "period", becomes "periodX" if specified)
     */
    axis: {
      type: String,
      required: false,
      default: "",
      validator(value) {
        return ["", "X", "Y", "Z"].includes(value);
      },
    },
    /**
     * Set "display: none" on the component. Useful for loading
     * extra data that doesn't require the user to select.
     */
    hidden: {
      type: Boolean,
      required: false,
      default: false,
    },
    /**
     * If true syncs the selected value to the query parameter in
     * the Route. (Two way binding)
     */
    syncRoute: {
      type: Boolean,
      required: false,
      default: true,
    },
    /**
     * Size passed directly to EclSelect (see docs there)
     */
    size: {
      type: String,
      required: false,
      default: null,
    },
    /**
     * If True includes the axis name in the input's label.
     *
     *  E.g (X) Period
     */
    showAxisLabel: {
      type: Boolean,
      required: false,
      default: true,
    },
    /**
     * When using a multi-choice select filter, set the default to
     * ALL possible values.
     */
    allInitial: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      internalValue: null,
      apiData: [],
      loading: false,
    };
  },
  computed: {
    ...mapState(useChartGroupStore, ["currentLabels"]),
    filterStore() {
      return useFilterStore()[this.axis];
    },
    modelValue: {
      get() {
        if (!this.syncRoute) {
          return this.internalValue || this.emptyValue;
        }

        return this.$route.query[this.queryName + this.axis] || this.emptyValue;
      },
      set(value) {
        this.internalValue = value;

        if (this.syncRoute) {
          this.$router.replace({
            query: {
              ...this.$route.query,
              [this.queryName + this.axis]: value,
            },
          });
        }
      },
    },
    queryName() {
      return this.errorMustImplement("queryName");
    },
    endpoint() {
      return this.errorMustImplement("endpoint");
    },
    endpointParams() {
      return {};
    },
    label() {
      return this.currentLabels[this.queryName] || this.queryName;
    },
    labelWithAxis() {
      if (!this.axis || !this.showAxisLabel) return this.label;

      return `(${this.axis}) ${this.label}`;
    },
    items() {
      return this.apiData.map((item) => {
        return {
          id: item.code,
          text: this.getDisplay(item),
          apiProps: item,
        };
      });
    },
    selected() {
      if (!this.multiple) {
        return this.apiData.find((item) => item.code === this.modelValue);
      }

      const values = new Set(this.modelValue);
      return this.apiData.filter((item) => values.has(item.code));
    },
    allowedValuesArray() {
      const result = [];
      for (const item of this.items) {
        if (!item.children) {
          result.push(item.id);
          continue;
        }

        for (const child of item.children) {
          result.push(child.id);
        }
      }
      return result;
    },
    allowedValues() {
      return new Set(this.allowedValuesArray);
    },
    isModelEmpty() {
      return this.multiple
        ? this.modelValue.length === 0
        : this.modelValue === "";
    },
    emptyValue() {
      return this.multiple ? [] : "";
    },
    defaultValue() {
      if (!this.items || this.items.length === 0) {
        return this.emptyValue;
      }

      if (this.multiple) {
        return this.allInitial
          ? this.allowedValuesArray
          : this.defaultMultiValue;
      } else {
        return this.defaultSingleValue;
      }
    },
    defaultSingleValue() {
      const choiceGroup = randomChoice(this.items);

      return randomChoice(choiceGroup.children)?.id || choiceGroup.id;
    },
    defaultMultiValue() {
      return [randomChoice(this.items).id];
    },
    multiple() {
      return false;
    },
    required() {
      return true;
    },
    isVisible() {
      // Only show this filter if there are more than one indicator group
      return this.items.length > 1;
    },
    modelValueAllowed() {
      const iter = Array.isArray(this.modelValue)
        ? this.modelValue
        : [this.modelValue];

      for (const val of iter) {
        if (!this.allowedValues.has(val)) {
          return false;
        }
      }
      return true;
    },
  },
  watch: {
    endpoint() {
      this.load();
    },
    selected() {
      this.filterStore[this.queryName] = this.selected;
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    getDisplay,
    async load() {
      if (!this.endpoint) return;
      this.loading = true;

      try {
        await Promise.all([this.loadApiData(), this.loadExtra()]);

        if (
          (!this.isModelEmpty && !this.modelValueAllowed) ||
          !this.syncRoute
        ) {
          // The current value set is not actually allowed. This will happen as the
          // allowed values change but the URL queries won't change automatically.
          if (this.required) {
            this.modelValue = this.defaultValue;
          } else {
            this.modelValue = this.emptyValue;
          }
        }

        if (this.isModelEmpty && this.required && this.defaultValue) {
          // A value is required, but none is set. Set the default value
          // automatically to avoid ambiguity;
          this.modelValue = this.defaultValue;
        }
      } finally {
        this.loading = false;
      }
    },
    async loadApiData() {
      this.apiData = (
        await api.get(this.endpoint, {
          params: this.endpointParams,
        })
      ).data;
    },
    async loadExtra() {},
  },
};
</script>
