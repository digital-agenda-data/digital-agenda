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
    endpointParams() {
      const result = {};

      for (const key of this.endpointFilters) {
        result[key] = this[key]?.code;
      }

      if (!Object.values(result).every((val) => val)) {
        // If there isn't a value selected for ALL filters
        // don't load any data
        return null;
      }

      return result;
    },
    chartOptions() {
      return {};
    },
    countries() {
      if (Array.isArray(this.country)) return this.country;
      if (this.country) return [this.country];
      return [];
    },
    selectedCountriesMap() {
      return new Map(
        this.countries.map((item) => [item.code, item.alt_label || item.label])
      );
    },
    chartData() {
      return this.apiData.map((item) => {
        return {
          y: item.value,
          color: item.country === "EU" ? "#427baa" : "#63b8ff",
          data: item,
        };
      });
    },
    chartDataFilteredByCountry() {
      return this.chartData.filter((item) =>
        this.selectedCountriesMap.has(item.data.country)
      );
    },
    categories() {
      return this.apiData.map(
        (item) => this.selectedCountriesMap.get(item.country) || item.country
      );
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
        await this.getFacts();
      } finally {
        this.loaded = true;
      }
    },
    async getFacts() {
      if (!this.endpointParams) return;

      this.apiData = await apiCall("GET", this.endpoint, this.endpointParams);
    },
  },
};
</script>
