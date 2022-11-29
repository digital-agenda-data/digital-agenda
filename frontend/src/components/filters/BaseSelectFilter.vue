<template>
  <ecl-select
    v-show="isVisible"
    v-model="modelValue"
    :items="items"
    :loading="loading"
    :multiple="multiple"
    :required="required"
    :label="labelWithAxis"
    :input-name="queryName"
  />
</template>

<script>
import EclSelect from "@/components/ecl/forms/EclSelect.vue";
import { apiCall } from "@/lib/api";
import { useFilterStore } from "@/stores/filterStore";
import { getDisplay, randomChoice } from "@/lib/utils";

export default {
  name: "BaseFilter",
  components: { EclSelect },
  props: {
    suffix: {
      type: String,
      required: false,
      default: "",
    },
  },
  emits: ["change"],
  data() {
    return {
      apiData: [],
      loading: false,
    };
  },
  computed: {
    filterStore() {
      return useFilterStore()[this.suffix];
    },
    modelValue: {
      get() {
        return this.$route.query[this.queryName + this.suffix];
      },
      set(value) {
        this.$router.replace({
          query: {
            ...this.$route.query,
            [this.queryName + this.suffix]: value,
          },
        });
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
      return "";
    },
    labelWithAxis() {
      if (!this.suffix) return this.label;

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
    allowedValues() {
      const result = new Set();
      for (const item of this.items) {
        if (!item.children) {
          result.add(item.id);
          continue;
        }

        for (const child of item.children) {
          result.add(child.id);
        }
      }
      return result;
    },
    defaultValue() {
      if (!this.items || this.items.length === 0) {
        return "";
      }

      const choice = randomChoice(this.items);

      return randomChoice(choice.children)?.id || choice.id;
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
  },
  watch: {
    endpoint() {
      this.modelValue = "";
      this.load();
    },
    selected() {
      this.filterStore[this.queryName] = this.selected;
      this.$emit("change", this.selected);
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    getDisplay,
    async load() {
      this.loading = true;

      try {
        if (this.endpoint) {
          await Promise.all([this.loadApiData(), this.loadExtra()]);
        }
        if (this.modelValue && !this.allowedValues.has(this.modelValue)) {
          // The current value set is not actually allowed. This will happen as the
          // allowed values change but the URL queries won't change automatically.
          if (this.required) {
            this.modelValue = this.defaultValue;
          } else {
            this.modelValue = "";
          }
        }

        if (!this.modelValue && this.required && this.defaultValue) {
          // A value is required, but none is set. Set the default value
          // automatically to avoid ambiguity;
          this.modelValue = this.defaultValue;
        }
      } finally {
        this.loading = false;
      }
    },
    async loadApiData() {
      this.apiData = await apiCall("GET", this.endpoint, this.endpointParams);
    },
    async loadExtra() {},
  },
};
</script>
