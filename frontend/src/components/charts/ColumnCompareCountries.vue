<template>
  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m chart-filters"
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
    <chart v-else-if="apiData.length > 0" :options="chartOptions" />
    <div v-else class="ecl-u-type-align-center ecl-u-pa-2xl">
      No data available
    </div>
  </div>

  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m"
  >
    <h2>Definition and scopes:</h2>

    <div class="ecl-row">
      <div class="ecl-col-12 ecl-col-l-8">
        <div v-html="currentChart.description" />
      </div>
      <div
        class="ecl-col-12 ecl-col-l-4 ecl-u-d-flex ecl-u-flex-column chart-actions"
      >
        <ecl-link label="Print chart" to="" no-visited />
        <ecl-link label="Print page" to="" no-visited />
        <ecl-link label="Download image" to="" no-visited />
        <ecl-link label="Export data" to="" no-visited />
        <ecl-link label="Embedded URL" to="" no-visited />
        <ecl-link label="View comments" to="" no-visited />
        <ecl-link label="Submit comment" to="" no-visited />
        <ecl-social-media-share />
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
import { useChartStore } from "@/stores/chartStore";
import { mapState } from "pinia";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclSocialMediaShare from "@/components/ecl/EclSocialMediaShare.vue";

export default {
  name: "ColumnCompareCountries",
  components: {
    EclSocialMediaShare,
    EclLink,
    Chart,
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
        credits: {
          text: "European Commission, Digital Scoreboard",
          href: "https://digital-strategy.ec.europa.eu/",
        },
        series: [
          {
            data: this.chartData,
          },
        ],
        legend: {
          enabled: false,
        },
        title: {
          text: this.indicator?.label,
        },
        subtitle: {
          text: this.period && `Year: ${this.period.code}`,
        },
        xAxis: {
          categories: this.categories,
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
    endpointParams() {
      this.loadData();
      console.log(this.$route);
    },
  },
  mounted() {
    this.loadData();
  },
  methods: {
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

.chart-actions > * {
  margin-bottom: 1rem;
}
</style>
