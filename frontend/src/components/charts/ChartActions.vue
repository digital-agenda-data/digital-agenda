<template>
  <div class="chart-actions">
    <ecl-link
      v-if="highchartInstance"
      no-visited
      label="Print chart"
      to="#print-chart"
      @click.capture.prevent="printChart"
    />
    <ecl-link
      no-visited
      label="Print page"
      to="#print-page"
      @click.capture.prevent="printPage"
    />
    <ecl-link
      v-if="highchartInstance"
      no-visited
      label="Download image"
      to="#download-chart"
      download-class
      @click.capture.prevent="downloadChart"
    />
    <ecl-link
      v-if="highchartInstance"
      no-visited
      label="Download SVG"
      to="#download-chart-svg"
      download-class
      @click.capture.prevent="downloadChart({ type: 'image/svg+xml' })"
    />
    <ecl-link
      v-for="(exportLink, axis) in chartRef?.exportLinks ?? {}"
      :key="'export' + axis"
      no-visited
      :to="exportLink"
      :label="'Export data ' + axis"
      download-class
    />
    <ecl-link no-visited label="Embedded URL" :to="embedURL" />
    <ecl-link
      no-visited
      label="Submit feedback"
      :to="{
        name: 'feedback',
      }"
    />
    <transition mode="out-in">
      <div v-if="!shareURL">
        <ecl-button
          v-if="!loading"
          label="Share"
          icon="share"
          @click="getShortUrl"
        />
        <ecl-spinner v-else size="small" />
      </div>
      <ecl-social-media-share
        v-else
        :text="currentChart.name"
        :url="shareURL"
      />
    </transition>
  </div>
</template>
<script>
import EclButton from "@/components/ecl/EclButton.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclSocialMediaShare from "@/components/ecl/EclSocialMediaShare.vue";
import { api } from "@/lib/api";
import { mapState } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";

export default {
  name: "ChartActions",
  components: { EclSpinner, EclButton, EclLink, EclSocialMediaShare },
  props: {
    chartRef: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
      shareURL: null,
    };
  },
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    ...mapState(useChartGroupStore, ["currentChartGroupCode"]),
    embedURL() {
      const url = new URL(this.$route.href, window.location);
      url.searchParams.set("embed", "true");
      return url.toString();
    },
    highchartInstance() {
      return this.chartRef?.chart;
    },
  },
  watch: {
    $route() {
      // Reset share URL since we will need to generate a new one if the URL
      // changes
      this.shareURL = null;
    },
  },
  methods: {
    printPage() {
      window.print();
    },
    printChart() {
      this.highchartInstance.print();
    },
    downloadChart(exportingOptions = {}) {
      this.highchartInstance.exportChartLocal(exportingOptions);
    },
    async getShortUrl() {
      try {
        this.loading = true;
        this.shareURL = (
          await api.post("/short-urls/", {
            chart: this.currentChart.id,
            query_arguments: window.location.search,
          })
        ).data.short_url;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style scoped lang="scss">
.chart-actions {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: 1fr;

  @media (min-width: 360px) {
    grid-template-columns: 1fr 1fr;
  }

  @media (min-width: 768px) {
    grid-template-columns: 1fr 1fr 1fr;
  }

  @media (min-width: 996px) {
    grid-template-columns: 1fr;
  }
}
</style>
