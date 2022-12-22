<template>
  <highcharts
    v-if="ready"
    class="ecl-u-flex-grow-1"
    :constructor-type="constructorType"
    :options="{ ...chartOptionsDefaults, ...chartOptions }"
    :callback="highchartsCallback"
  />
  <ecl-spinner v-else size="large" centered />
</template>

<script>
import { mapState, mapStores } from "pinia";
import { Chart } from "highcharts-vue";

import EclSpinner from "@/components/ecl/EclSpinner.vue";

import { api } from "@/lib/api";
import {
  getDisplay,
  getUnitDisplay,
  groupByMulti,
  toAPIKey,
} from "@/lib/utils";

import { useChartStore } from "@/stores/chartStore";
import { useFilterStore } from "@/stores/filterStore";
import { useCountryStore } from "@/stores/countryStore";
import { EUROSTAT_FLAGS } from "@/lib/constants";

/**
 * Base component use for charts. Extend this component and override various
 * computed properties to create a chart.
 */
export default {
  name: "BaseChart",
  components: {
    EclSpinner,
    highcharts: Chart,
  },
  data() {
    return {
      loading: true,
      ready: false,
      apiData: [],
      chart: null,
    };
  },
  computed: {
    ...mapStores(useFilterStore),
    ...mapState(useChartStore, ["currentChart"]),
    ...mapState(useCountryStore, ["countryByCode"]),
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
     * Default chart type for the series. See docs upstream:
     *
     *  https://api.highcharts.com/highcharts/chart.type
     */
    chartType() {
      return "";
    },
    /**
     * The Highchart constructor used to initialize the chart. Possible
     * values include: chart, mapChart, stockChart, ganttChart
     */
    constructorType() {
      return "chart";
    },
    /**
     * Show axis labels in filters and definitions.
     */
    showAxisLabel() {
      return true;
    },
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
    filterXComponents() {
      return [];
    },
    filterYComponents() {
      return [];
    },
    filterZComponents() {
      return [];
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
      return this.errorMustImplement("endpointFilters");
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
        chart: {
          type: this.chartType,
        },
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
        tooltip: this.tooltip,
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
      return groupByMulti(this.apiData, this.groupBy, "value");
    },
    /**
     * Same as `apiValuesGrouped` but has the original "fact" Object from
     * the api for the final group, instead of only the value.
     */
    apiDataGrouped() {
      return groupByMulti(this.apiData, this.groupBy);
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
    /**
     * Default tooltip used. See documentation upstream here
     *
     *  https://api.highcharts.com/highcharts/tooltip
     */
    tooltip() {
      const parent = this;
      return {
        formatter() {
          const fact = this.point.options.fact;
          const result = [`<b>${this.point.options.key ?? this.key}</b>`];

          if (this.series.userOptions.name) {
            result.push(this.series.userOptions.name);
          }

          if (parent.unit?.code) {
            result.push(parent.getUnitDisplay(fact?.value, parent.unit));
          }

          for (const flag of fact?.flags || "") {
            result.push("<b>Flag:</b> " + (EUROSTAT_FLAGS[flag] ?? flag));
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
    getUnitDisplay,
    /**
     * Join objects from the backend or strings to make a title
     *
     * @param items {*[]}
     * @return {String}
     */
    makeTitle(items) {
      return items
        .map((s) => s?.label)
        .map((s) => s?.trim())
        .filter((s) => !!s)
        .join(", ");
    },
    highchartsCallback(chart) {
      this.chart = chart;
    },
    async loadData() {
      if (!this.endpointParams) {
        this.apiData = [];
        return;
      }

      this.loading = true;
      this.chart?.showLoading();
      try {
        await Promise.all([this.getFacts(), this.loadExtra()]);
      } finally {
        this.loading = false;
        this.chart?.hideLoading();
        // Don't show the chart until data is ready to avoid unnecessary
        // layout shifts
        this.ready = true;
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
      const resp = (
        await api.get(this.endpoint, {
          params: this.endpointParams[axis],
        })
      ).data;

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
