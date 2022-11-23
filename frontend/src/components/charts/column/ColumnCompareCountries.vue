<template>
  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m ecl-u-screen-only hide-embedded chart-filters"
  >
    <indicator-group-filter @change="indicatorGroup = $event" />
    <indicator-filter @change="indicator = $event" />
    <breakdown-group-filter @change="breakdownGroup = $event" />
    <breakdown-filter @change="breakdown = $event" />
    <period-filter @change="period = $event" />
    <unit-filter @change="unit = $event" />
    <country-filter @change="countries = $event" />
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
        <chart-definitions
          :indicator="indicator"
          :breakdown="breakdown"
          :unit="unit"
        />
      </div>

      <div class="ecl-col-12 ecl-col-l-4 ecl-u-screen-only">
        <chart-actions :chart="chart" />
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from "highcharts-vue";

import { apiCall } from "@/lib/api";

import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import BreakdownFilter from "@/components/filters/BreakdownFilter.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";

import ChartDefinitions from "@/components/charts/ChartDefinitions.vue";
import { useChartStore } from "@/stores/chartStore";
import { mapState } from "pinia";
import ChartActions from "@/components/charts/ChartActions.vue";

export default {
  name: "ColumnCompareCountries",
  components: {
    highcharts: Chart,
    ChartActions,
    ChartDefinitions,
    EclSpinner,
    CountryFilter,
    BreakdownFilter,
    BreakdownGroupFilter,
    UnitFilter,
    PeriodFilter,
    IndicatorFilter,
    IndicatorGroupFilter,
  },
  data() {
    return {
      loaded: false,
      apiData: [],
      chart: null,
      indicatorGroup: null,
      indicator: null,
      period: null,
      unit: null,
      breakdownGroup: null,
      breakdown: null,
      countries: [],
    };
  },
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    endpointParams() {
      if (this.breakdown && this.period && this.indicator && this.unit) {
        return {
          breakdown: this.breakdown.code,
          period: this.period.code,
          indicator: this.indicator.code,
          unit: this.unit.code,
        };
      }
      return null;
    },
    chartOptions() {
      const parent = this;
      return {
        chart: {
          type: "column",
          height: "600px",
        },
        exporting: {
          sourceWidth: 1024,
          sourceHeight: 600,
        },
        credits: {
          text: "European Commission, Digital Scoreboard",
          href: "https://digital-strategy.ec.europa.eu/",
        },
        series: [
          {
            name: this.unit?.alt_label,
            data: this.chartData,
          },
        ],
        legend: {
          enabled: false,
        },
        title: {
          text: [this.indicator?.label, this.breakdown?.label]
            .map((s) => s.trim())
            .join(", "),
        },
        subtitle: {
          text: this.period && `Year: ${this.period.code}`,
        },
        xAxis: {
          categories: this.categories,
          title: {
            text: "Country",
            enabled: false,
          },
        },
        yAxis: {
          title: {
            text: this.unit?.alt_label,
          },
        },
        tooltip: {
          formatter() {
            return [
              `<b>${this.x}</b>`,
              `${this.y}${parent.unit.alt_label}`,
              `<b>Time Period:</b> Year: ${parent.period.code}`,
            ].join("<br/>");
          },
        },
      };
    },
    countriesMap() {
      return new Map(
        this.countries.map((item) => [item.code, item.alt_label || item.label])
      );
    },
    chartData() {
      return this.apiData
        .filter((item) => this.countriesMap.has(item.country))
        .map((item) => {
          return {
            y: item.value,
            color: item.country === "EU" ? "#427baa" : "#63b8ff",
          };
        });
    },
    categories() {
      return this.apiData.map(
        (item) => this.countriesMap.get(item.country) || item.country
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

      this.apiData = await apiCall(
        "GET",
        "/facts/facts-per-country/",
        this.endpointParams
      );
    },
  },
};
</script>

<style scoped>
.chart-filters {
  display: grid;
  grid-gap: 1rem 2rem;
  grid-template-columns: 1fr;
}

@media screen and (min-width: 768px) {
  .chart-filters {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
