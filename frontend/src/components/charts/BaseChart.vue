<template>
  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m ecl-u-screen-only hide-embedded chart-filters"
  >
    <component
      :is="filterComponent"
      v-for="filterComponent in filterComponents"
      :key="filterComponent.name"
    />
  </div>
  <div
    class="ecl-u-mt-m ecl-u-mb-m ecl-u-border-width-1 ecl-u-border-style-solid ecl-u-border-color-grey-10"
  >
    <div v-if="!loaded" class="ecl-u-type-align-center ecl-u-pa-2xl">
      <ecl-spinner />
    </div>
    <highcharts
      v-else-if="apiData.length > 0"
      :options="chartOptions"
      :callback="highchartsCallback"
    />
    <div v-else class="ecl-u-type-align-center ecl-u-pa-2xl">
      No data available
    </div>
  </div>

  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m hide-embedded"
  >
    <h2>Definition and scopes:</h2>

    <div class="ecl-row">
      <div class="ecl-col-12 ecl-col-l-8">
        <div v-html="currentChart.description" />
        <chart-definitions />
      </div>

      <div class="ecl-col-12 ecl-col-l-4 ecl-u-screen-only">
        <chart-actions :chart="chart" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { Chart } from "highcharts-vue";

import { apiCall } from "@/lib/api";

import { useChartStore } from "@/stores/chartStore";
import { useFilterStore } from "@/stores/filterStore";

import EclSpinner from "@/components/ecl/EclSpinner.vue";

import ChartDefinitions from "@/components/charts/ChartDefinitions.vue";
import ChartActions from "@/components/charts/ChartActions.vue";
import { camelToSnakeCase } from "@/lib/utils";

export default {
  name: "BaseChart",
  components: {
    highcharts: Chart,
    ChartActions,
    ChartDefinitions,
    EclSpinner,
  },
  data() {
    return {
      loaded: false,
      apiData: [],
      chart: null,
    };
  },
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    ...mapState(useFilterStore, [
      "indicatorGroup",
      "indicator",
      "breakdownGroup",
      "breakdown",
      "period",
      "unit",
      "country",
    ]),
    filterComponents() {
      return [];
    },
    endpoint() {
      return null;
    },
    endpointFilters() {
      return [];
    },
    chartOptions() {
      return {};
    },
    groupBy() {
      return [];
    },
    endpointParams() {
      const result = {};

      for (const key of this.endpointFilters) {
        result[camelToSnakeCase(key)] = this[key]?.code;
      }

      if (!Object.values(result).every((val) => val)) {
        // If there isn't a value selected for ALL filters
        // don't load any data
        return null;
      }

      return result;
    },
    apiValuesGrouped() {
      if (!this.groupBy || this.groupBy.length === 0) return {};

      const result = {};

      for (const item of this.apiData) {
        const lastKey = this.groupBy.slice(-1)[0];

        let group = result;

        for (const key of this.groupBy.slice(0, -1)) {
          const itemValue = item[key];

          if (!group[itemValue]) {
            group[itemValue] = {};
          }

          group = group[itemValue];
        }

        group[item[lastKey]] = item.value;
      }

      return result;
    },
    countries() {
      if (Array.isArray(this.country)) return this.country;
      if (this.country) return [this.country];
      return [];
    },
  },
  watch: {
    endpointParams(newValue, oldValue) {
      if (JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
        this.loadData();
      }
    },
  },
  mounted() {
    this.loadData();
  },
  methods: {
    highchartsCallback(chart) {
      this.chart = chart;
    },
    async loadData() {
      this.loaded = false;
      try {
        await Promise.all([this.getFacts(), this.loadExtra()]);
      } finally {
        this.loaded = true;
      }
    },
    async getFacts() {
      if (!this.endpointParams) return;

      this.apiData = await apiCall("GET", this.endpoint, this.endpointParams);
    },
    async loadExtra() {},
  },
};
</script>
