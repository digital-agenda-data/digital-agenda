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

export default {
  name: "BaseFilter",
  components: { EclSelect },
  props: {
    suffix: {
      type: String,
      required: false,
      default: "",
    },
    hidden: {
      type: Boolean,
      required: false,
      default: false,
    },
    syncRoute: {
      type: Boolean,
      required: false,
      default: true,
    },
    size: {
      type: String,
      required: false,
      default: null,
    },
    showAxisLabel: {
      type: Boolean,
      required: false,
      default: true,
    },
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
      return useFilterStore()[this.suffix];
    },
    modelValue: {
      get() {
        if (!this.syncRoute) {
          return this.internalValue || this.emptyValue;
        }

        return (
          this.$route.query[this.queryName + this.suffix] || this.emptyValue
        );
      },
      set(value) {
        this.internalValue = value;

        if (this.syncRoute) {
          this.$router.replace({
            query: {
              ...this.$route.query,
              [this.queryName + this.suffix]: value,
            },
          });
        }
      },
    },
    endpoint() {
      return "";
    },
    endpointParams() {
      return {};
    },
    queryName() {
      return "";
    },
    label() {
      return this.currentLabels[this.queryName] || this.queryName;
    },
    labelWithAxis() {
      if (!this.suffix || !this.showAxisLabel) return this.label;

      return `(${this.suffix}) ${this.label}`;
    },
    items() {
      return this.apiData.map((item) => {
        return {
          id: item.code,
          text: this.getDisplay(item),
          item,
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
