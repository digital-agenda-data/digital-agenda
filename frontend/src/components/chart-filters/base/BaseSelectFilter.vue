<template>
  <ecl-select
    v-show="isVisible"
    v-model="modelValue"
    :items="items"
    :loading="loading"
    :multiple="multiple"
    :label="labelWithAxis"
    :input-name="queryName + axis"
    :size="size"
  />
</template>

<script>
import EclSelect from "@/components/ecl/forms/EclSelect.vue";
import { api } from "@/lib/api";
import { FILTER_SUFFIXES } from "@/lib/constants";
import { useFilterStore } from "@/stores/filterStore";
import { forceArray, randomChoice, toAPIKey } from "@/lib/utils";
import { mapState } from "pinia";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useChartStore } from "@/stores/chartStore";
import { useRouteQuery } from "@vueuse/router";
import { ref } from "vue";

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
        return FILTER_SUFFIXES.includes(value);
      },
    },
    /**
     * Additional params to send as API filters.
     * For example:
     *
     *  ["breakdown", "unit"]
     */
    extraParams: {
      type: Array,
      required: false,
      default: null,
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
      apiDataRaw: [],
      loading: false,
      abortController: null,
    };
  },
  computed: {
    ...mapState(useChartGroupStore, ["currentLabels", "currentChartGroup"]),
    ...mapState(useChartStore, ["currentFilterOptions"]),
    filterStore() {
      return useFilterStore()[this.axis];
    },
    model() {
      if (this.syncRoute) {
        return useRouteQuery(this.queryName + this.axis, this.emptyValue, {
          router: this.$router,
          route: this.$route,
        });
      }

      return ref(this.emptyValue);
    },
    modelValue: {
      // Makes sure that the model is an array if this is a multiselect
      // and a single value otherwise.
      get() {
        if (this.multiple) {
          return forceArray(this.model.value.split(","));
        } else if (Array.isArray(this.model.value)) {
          return this.model.value[0];
        } else {
          return this.model.value;
        }
      },
      set(value) {
        if (this.multiple) {
          value = forceArray(value).join(",");
        } else if (Array.isArray(value)) {
          value = value[0];
        }

        this.model.value = value;
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
    ignoredCodes() {
      return new Set(this.currentFilterOptions.ignored[this.queryName]);
    },
    apiData() {
      return this.apiDataRaw.filter(
        (apiItem) => !this.ignoredCodes.has(apiItem.code),
      );
    },
    items() {
      return this.apiData.map((item) => {
        return {
          id: item.code,
          text: item.display,
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
      return "";
    },
    defaultValue() {
      if (!this.items || this.items.length === 0) {
        return this.emptyValue;
      }

      if (this.multiple) {
        if (this.defaultBackendMultiValue.length > 0) {
          return this.defaultBackendMultiValue;
        } else if (this.allInitial) {
          return this.allowedValuesArray;
        } else {
          return this.defaultMultiValue;
        }
      } else {
        if (this.defaultBackendSingleValue) {
          return this.defaultBackendSingleValue;
        } else {
          return this.defaultSingleValue;
        }
      }
    },
    defaultBackendSingleValue() {
      return this.currentFilterOptions.defaults[this.queryName]?.find((code) =>
        this.allowedValues.has(code),
      );
    },
    defaultSingleValue() {
      const choiceGroup = randomChoice(this.items);

      return randomChoice(choiceGroup.children)?.id || choiceGroup.id;
    },
    defaultBackendMultiValue() {
      return (this.currentFilterOptions.defaults[this.queryName] ?? []).filter(
        (code) => this.allowedValues.has(code),
      );
    },
    defaultMultiValue() {
      return [randomChoice(this.items).id];
    },
    multiple() {
      return false;
    },
    isVisible() {
      if (this.currentFilterOptions.hidden[this.queryName]) {
        // Forced hidden from the backend options
        return false;
      }
      return !this.hidden;
    },
    modelValueAllowed() {
      for (const val of forceArray(this.modelValue)) {
        if (!this.allowedValues.has(val)) {
          return false;
        }
      }
      return true;
    },
    mergedEndpointParams() {
      const result = {
        chart_group: this.currentChartGroup.code,
        ...this.endpointParams,
      };
      for (const key of forceArray(this.extraParams)) {
        result[toAPIKey(key)] = this.filterStore[key]?.code;
      }
      return result;
    },
  },
  watch: {
    currentFilterOptions() {
      // Reload if the filter options have changed (for example, if the
      // selected chart has changed).
      this.load();
    },
    mergedEndpointParams(newValue, oldValue) {
      if (JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
        this.load();
      }
    },
    selected() {
      this.filterStore[this.queryName] = this.selected;
    },
  },
  mounted() {
    this.load();
  },
  unmounted() {
    this.filterStore[this.queryName] = null;
  },
  methods: {
    async load() {
      if (!this.endpoint) return;
      if (!Object.values(this.mergedEndpointParams).every((item) => !!item))
        return;

      this.loading = true;
      this.filterStore.loadingCounter += 1;

      try {
        await Promise.all([this.loadApiData(), this.loadExtra()]);

        if (
          (!this.isModelEmpty && !this.modelValueAllowed) ||
          !this.syncRoute
        ) {
          this.modelValue = this.defaultValue;
        }
        if (this.isModelEmpty && this.defaultValue) {
          // A value is required, but none is set. Set the default value
          // automatically to avoid ambiguity;
          this.modelValue = this.defaultValue;
        }
      } finally {
        this.loading = false;
        this.filterStore.loadingCounter -= 1;
      }
    },
    async loadApiData() {
      if (this.abortController) {
        this.abortController.abort();
      }

      this.abortController = new AbortController();
      try {
        this.apiDataRaw = (
          await api.get(this.endpoint, {
            signal: this.abortController.signal,
            params: this.mergedEndpointParams,
          })
        ).data;
      } catch (e) {
        // Ignore canceled error since that is on purpose.
        if (e.code !== "ERR_CANCELED") {
          throw e;
        }
      }
    },
    async loadExtra() {},
  },
};
</script>
