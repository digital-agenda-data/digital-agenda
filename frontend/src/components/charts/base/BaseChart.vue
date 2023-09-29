<template>
  <highcharts
    v-if="ready"
    :constructor-type="constructorType"
    :options="mergedChartOptions"
    :callback="highchartsCallback"
  />
  <simple-spinner v-else />
</template>

<script>
import { useAppSettings } from "@/stores/appSettingsStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { mapState, mapStores } from "pinia";
import { Chart } from "highcharts-vue";

import SimpleSpinner from "@/components/SimpleSpinner.vue";

import { api } from "@/lib/api";
import {
  forceArray,
  getUnitDisplay,
  groupByMulti,
  toAPIKey,
} from "@/lib/utils";

import { useChartStore } from "@/stores/chartStore";
import { useFilterStore } from "@/stores/filterStore";
import { useCountryStore } from "@/stores/countryStore";
import { VALUE_AXIS } from "@/lib/constants";

/**
 * Base component use for charts. Extend this component and override various
 * computed properties to create a chart.
 */
export default {
  name: "BaseChart",
  components: {
    SimpleSpinner,
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
    ...mapState(useAppSettings, ["appSettings"]),
    ...mapState(useChartStore, ["currentChart"]),
    ...mapState(useChartGroupStore, ["currentChartGroupCode"]),
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
      if (!this.filterStore.allFiltersLoaded) {
        // Filters are still loading, don't load facts since the filters
        // will change shortly, discarding the loaded data immediately.
        return null;
      }

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
    mergedChartOptions() {
      const result = {
        ...this.chartOptionsDefaults,
        ...this.chartOptions,
      };

      // Set custom ranges to the "value" axis depending on the chart type.
      // No idea why anyone would ever use this. Oh well... ¯\_(ツ)_/¯
      const minValue = this.currentChart.min_value;
      const maxValue = this.currentChart.max_value;

      for (const axis of VALUE_AXIS[this.chartType] ?? []) {
        result[axis] ??= {};

        // Some charts have multiple axis of the same kind, so force array here
        // (e.g. SplineCompareTwoIndicators)
        for (const opt of forceArray(result[axis])) {
          opt.min = minValue ?? opt.min;
          opt.max = maxValue ?? opt.max;
        }
      }

      return result;
    },
    extraNotes() {
      return (this.indicator?.extra_notes || [])
        .filter((item) => item.period === this.period?.code)
        .map((item) => item.note);
    },
    /**
     * Default chart options, (shallow) merged with the chartOptions
     * and used for HighCharts.
     */
    chartOptionsDefaults() {
      let legend;
      if (this.currentChart?.legend_layout === "horizontal") {
        legend = {
          itemWidth: 150,
          layout: "horizontal",
        };
      } else {
        legend = {
          itemWidth: 150,
          layout: "vertical",
          align: "right",
          verticalAlign: "middle",
        };
      }

      return {
        chart: {
          type: this.chartType,
        },
        series: this.series,
        title: {
          text: this.makeTitle([this.indicator, this.breakdown]),
        },
        subtitle: {
          text: this.joinStrings(
            [this.period?.label || this.period?.code, ...this.extraNotes],
            " "
          ),
          style: {
            color: "#333333",
            fontWeight: "bold",
            fontSize: "1rem",
          },
        },
        legend: {
          enabled: false,
        },
        tooltip: this.tooltip,
        yAxis: {
          title: {
            text: this.unit?.display,
          },
        },
        responsive: {
          rules: [
            {
              condition: { minWidth: 768 },
              chartOptions: {
                legend,
              },
            },
          ],
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
      return forceArray(this.filterStore.country);
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
            result.push("<b>Flag:</b> " + parent.getFlagDisplay(flag));
          }

          if (parent.breakdown?.code) {
            result.push(`<b>Breakdown:</b> ${parent.breakdown.display}`);
          }

          if (parent.period?.code) {
            result.push(`<b>Time Period:</b> ${parent.period.label}`);
          }

          return result.join("<br/>");
        },
      };
    },
    exportLinks() {
      const result = {};
      for (const axis in this.endpointParams) {
        result[axis] = api.getUri({
          url: "/facts/",
          params: {
            ...this.endpointParams[axis],
            chart_group: this.currentChartGroupCode,
            format: "xlsx",
          },
        });
      }
      return result;
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
    getUnitDisplay,
    /**
     * Join objects from the backend or strings to make a title
     *
     * @param items {*[]}
     * @param separator {String}
     * @return {String}
     */
    makeTitle(items, separator = ", ") {
      return this.joinStrings(
        items.map((s) => s?.label),
        separator
      );
    },
    /**
     * Join strings excluding any empty/nulls
     *
     * @param items {String[]}
     * @param separator {String}
     * @return {String}
     */
    joinStrings(items, separator = ", ") {
      return items
        .map((s) => s?.trim())
        .filter((s) => !!s)
        .join(separator);
    },
    highchartsCallback(chart) {
      this.chart = chart;
    },
    /**
     * Get a suitable display string for a data point flag
     *
     * @param flag {string} single character data point flag
     * @return {string}
     */
    getFlagDisplay(flag) {
      flag = flag.toLowerCase();
      return useAppSettings().appSettings.eurostat_flags[flag] ?? flag;
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
