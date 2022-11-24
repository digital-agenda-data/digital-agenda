<template>
  <ecl-select
    v-show="isVisible"
    v-model="modelValue"
    :items="items"
    :loading="loading"
    :multiple="multiple"
    :required="required"
    :label="label"
    :input-name="queryName"
  />
</template>

<script>
import EclSelect from "@/components/ecl/forms/EclSelect.vue";
import { apiCall } from "@/lib/api";

export default {
  name: "BaseFilter",
  components: { EclSelect },
  emits: ["change"],
  data() {
    return {
      apiData: [],
      loading: false,
    };
  },
  computed: {
    modelValue: {
      get() {
        return this.$route.query[this.queryName];
      },
      set(value) {
        this.$router.replace({
          query: {
            ...this.$route.query,
            [this.queryName]: value,
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
    items() {
      return this.apiData.map((item) => {
        return {
          id: item.code,
          text: item.alt_label || item.label || item.code,
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
      return new Set(this.items.map((item) => item.id));
    },
    defaultValue() {
      return this.items[0]?.id || "";
    },
    multiple() {
      return false;
    },
    required() {
      return true;
    },
    isVisible() {
      return true;
    },
  },
  watch: {
    endpoint() {
      this.modelValue = "";
      this.load();
    },
    selected() {
      this.$emit("change", this.selected);
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    async load() {
      this.loading = true;

      try {
        await this.loadData();
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
    async loadData() {
      if (this.endpoint) {
        this.apiData = await apiCall("GET", this.endpoint, this.endpointParams);
      }
    },
  },
};
</script>

<style scoped></style>
