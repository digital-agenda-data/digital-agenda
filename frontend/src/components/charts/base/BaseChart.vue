<template>
  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m ecl-u-screen-only hide-embedded chart-filters"
  >
    <component
      :is="item.component"
      v-for="item in normalizedComponents"
      :key="item.key || item.component.name"
      v-bind="item.attrs"
    />
  </div>
  <div
    class="ecl-u-mt-m ecl-u-mb-m ecl-u-border-width-1 ecl-u-border-style-solid ecl-u-border-color-grey-10 chart-container-digital-agenda"
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
import { mapState, mapStores } from "pinia";
import { Chart } from "highcharts-vue";

import { apiCall } from "@/lib/api";

import { useChartStore } from "@/stores/chartStore";
import { useFilterStore } from "@/stores/filterStore";

import EclSpinner from "@/components/ecl/EclSpinner.vue";

import ChartDefinitions from "@/components/charts/ChartDefinitions.vue";
import ChartActions from "@/components/charts/ChartActions.vue";
import { getDisplay, toAPIKey } from "@/lib/utils";

/**
 * Base component use for charts. Extend this component and override various
 * computed properties to create a chart.
 */
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
    ...mapStores(useFilterStore),
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
    /**
     * List of components to display in the chart filter section of the page.
     *
     * Can also be Objects in the following format:
     *
     *   {
     *     key: <unique id>,
     *     component: <component>
     *     attrs: {
     *       <additional props for the component>
     *     }
     *   }
     */
    filterComponents() {
      return [];
    },
    /**
     * Normalize components to Objects with key, component
     * and attrs attributes.
     */
    normalizedComponents() {
      return this.filterComponents.map((item) => this.normalizeComponent(item));
    },
    endpoint() {
      return "/facts/";
    },
    /**
     * Filters to be sent as query parameters to the API endpoint. E.g.
     *
     *   ["breakdown", "indicator", "period", "unit"]
     *
     *  Or, for multi axis loads:
     *
     *  {
     *    "X": ["breakdownX", "indicatorX", "period"],
     *    "Y": ["breakdownY", "indicatorY", "period"],
     *  }
     *
     * `camelCase` entries will be automatically converted to `snake_case`
     * before sending to the API.
     */
    endpointFilters() {
      return [];
    },
    /**
     * Compute API query params based on the endpointFilters property. Multiple
     * API calls will be made for each property of the object. E.g:
     *
     * {
     *   "": {
     *     breakpoint: <code>,
     *     unit: <code>,
     *     ...
     *   },
     *   "X": {
     *     ...
     *   },
     *   "Y": {
     *     ...
     *   }
     * }
     *
     */
    endpointParams() {
      let filterKeys = null;

      if (Array.isArray(this.endpointFilters)) {
        filterKeys = {
          "": this.endpointFilters,
        };
      } else {
        filterKeys = this.endpointFilters;
      }

      const result = {};

      for (const axis in filterKeys) {
        result[axis] = {};

        for (const key of filterKeys[axis]) {
          result[axis][toAPIKey(key)] = this.filterStore[key]?.code;
        }

        if (!Object.values(result[axis]).every((val) => val)) {
          // If there isn't a value selected for ALL filters
          // don't load any data
          return null;
        }
      }

      return result;
    },
    /**
     * Series used for the HighCharts
     */
    series() {
      return [];
    },
    /**
     * Default chart options, (shallow) merged with the chartOptions
     * and used for HighCharts.
     */
    chartOptionsDefaults() {
      return {
        series: this.series,
        title: {
          text: this.makeTitle([this.indicator, this.breakdown]),
        },
        subtitle: {
          text: this.period?.code && `Year: ${this.period.code}`,
        },
        legend: {
          enabled: false,
        },
        tooltip: this.defaultTooltip,
        yAxis: {
          title: {
            text: this.unit?.alt_label,
          },
        },
      };
    },
    /**
     * Chart options, (shallow) merged with the chartOptionsDefaults
     * and used for HighCharts.
     */
    chartOptions() {
      return {};
    },
    /**
     * Attribute key to use to group the API data values. E.g.
     *
     *  ["country", "period"]
     */
    groupBy() {
      return [];
    },
    /**
     * Group API data values by the specified keys in `groupBy`. E.g. for
     * the ["country", "period"] groupBy the result would be:
     *
     * {
     *   "EU": {
     *     "2017": 42,
     *     "2018": 156,
     *     ...
     *   },
     *   ...
     * }
     */
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
    /**
     * Array of country objects currently selected in the filters.
     */
    countries() {
      if (Array.isArray(this.country)) return this.country;
      if (this.country) return [this.country];
      return [];
    },
    /**
     * Sorted Array of all the unique period codes from the API data
     */
    apiDataPeriods() {
      return Array.from(
        new Set(this.apiData.map((item) => item.period))
      ).sort();
    },
    lastPeriod() {
      return parseInt(this.apiDataPeriods.slice(-1)[0]);
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
    /**
     * Entries that will be defined in the page footer
     */
    defineEntries() {
      return {
        Indicator: this.indicator,
        Breakdown: this.breakdown,
        Unit: this.unit,
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
    makeTitle(items) {
      return items
        .map((s) => s?.label)
        .filter((s) => !!s)
        .map((s) => s?.trim())
        .join(", ");
    },
    normalizeComponent(item, suffix = "", className = "chart-filter") {
      let result = item;
      if (!item.component) {
        result = {
          component: item,
          attrs: {},
        };
      }

      result.key = result.key || result.component.name + suffix;
      result.attrs.suffix = suffix;
      result.attrs.class = className;

      return result;
    },
    highchartsCallback(chart) {
      this.chart = chart;
      this.chart.showLoading();
    },
    async loadData() {
      if (!this.endpointParams) {
        this.apiData = [];
        return;
      }

      this.loaded = false;
      this.chart.showLoading();
      try {
        await Promise.all([this.getFacts(), this.loadExtra()]);
      } finally {
        this.chart.hideLoading();
        this.loaded = true;
      }
    },
    async getFacts() {
      const result = {};

      await Promise.all(
        Object.keys(this.endpointParams).map((axis) =>
          this.getFactForAxis(axis, result)
        )
      );

      this.apiData = Object.values(result).flat();
    },
    async getFactForAxis(axis, result) {
      const resp = await apiCall(
        "GET",
        this.endpoint,
        this.endpointParams[axis]
      );

      result[axis] = [];
      for (const item of resp) {
        result[axis].push({
          ...item,
          axis,
        });
      }
    },
    async loadExtra() {},
  },
};
</script>
