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
    <highcharts
      :options="{ ...chartOptionsDefaults, ...chartOptions }"
      :callback="highchartsCallback"
    />
  </div>

  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m hide-embedded"
  >
    <h2>Definition and scopes:</h2>

    <div class="ecl-row">
      <div class="ecl-col-12 ecl-col-l-8">
        <div v-html="currentChart.description" />
        <chart-definitions :define="defineEntries" />
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
import { camelToSnakeCase, getDisplay, randomChoice } from "@/lib/utils";

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
    allInitialCountries() {
      return false;
    },
    defineEntries() {
      return {
        Indicator: this.indicator,
        Breakdown: this.breakdown,
        Unit: this.unit,
      };
    },
    filterComponents() {
      return [];
    },
    endpoint() {
      return "/facts/facts-per-country/";
    },
    endpointFilters() {
      return [];
    },
    chartOptionsDefaults() {
      return {
        legend: {
          enabled: false,
        },
        title: {
          text: [this.indicator?.label, this.breakdown?.label]
            .filter((s) => !!s)
            .map((s) => s?.trim())
            .join(", "),
        },
        subtitle: {
          text: this.period?.code && `Year: ${this.period.code}`,
        },
        tooltip: this.defaultTooltip,
        yAxis: {
          title: {
            text: this.unit?.alt_label,
          },
        },
      };
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
    countriesWithData() {
      return Array.from(new Set(this.apiData.map((item) => item.country)));
    },
    apiDataPeriods() {
      return Array.from(
        new Set(this.apiData.map((item) => item.period))
      ).sort();
    },
    lastPeriod() {
      return parseInt(this.apiDataPeriods.slice(-1)[0]);
    },
    initialCountries() {
      if (this.allInitialCountries) {
        return this.countriesWithData;
      }

      const result = ["EU"];
      const another = randomChoice(
        this.countriesWithData.filter((code) => code !== "EU")
      );
      if (another) {
        result.push(another);
      }

      return result.sort();
    },
    defaultTooltip() {
      const parent = this;
      return {
        formatter() {
          const result = [`<b>${this.key}</b>`];

          if (this.series.userOptions.name) {
            result.push(this.series.userOptions.name);
          }

          if (parent.unit.alt_label.startsWith("%")) {
            result.push(`${this.y}${parent.unit.alt_label}`);
          } else {
            result.push(`${this.y} ${parent.unit.alt_label}`);
          }

          if (parent.breakdown?.code) {
            result.push(
              `<b>Breakdown:</b> ${parent.getDisplay(parent.breakdown)}`
            );
          }

          if (parent.period?.code) {
            result.push(`<b>Time Period:</b> Year: ${parent.period.code}`);
          }

          return result.join("<br/>");
        },
      };
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
    getDisplay,
    highchartsCallback(chart) {
      this.chart = chart;
    },
    async loadData() {
      if (!this.endpointParams) return;

      this.loaded = false;
      this.chart.showLoading();
      try {
        await Promise.all([this.getFacts(), this.loadExtra()]);
        this.setInitialCountries();
      } finally {
        this.chart.hideLoading();
        this.loaded = true;
      }
    },
    async getFacts() {
      this.apiData = await apiCall("GET", this.endpoint, this.endpointParams);
    },
    async loadExtra() {},
    /**
     * Set the country filter if it isn't set already. Otherwise, no data will
     * ever be displayed.
     */
    setInitialCountries() {
      if (this.initialCountries.length > 0 && this.countries.length === 0) {
        this.$router.replace({
          query: {
            ...this.$route.query,
            country: this.initialCountries,
          },
        });
      }
    },
  },
};
</script>
