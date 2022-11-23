<template>
  <div class="ecl-u-d-flex ecl-u-flex-column chart-actions">
    <ecl-link
      v-if="chart"
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
      v-if="chart"
      no-visited
      label="Download image"
      to="#download-chart"
      @click.capture.prevent="downloadChart"
    />
    <ecl-link
      v-if="chart"
      no-visited
      label="Export data"
      to="#export-chart"
      @click.capture.prevent="exportChart"
    />
    <ecl-link no-visited label="Embedded URL" :to="embedURL" />
    <ecl-link
      no-visited
      label="View comments"
      :to="{
        name: 'comments',
        params: { chartGroupCode: currentChartGroupCode },
      }"
    />
    <ecl-link
      no-visited
      label="Submit comments"
      :to="{
        name: 'comments',
        params: { chartGroupCode: currentChartGroupCode },
      }"
    />
    <ecl-social-media-share :text="currentChart.name" />
  </div>
</template>
<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclSocialMediaShare from "@/components/ecl/EclSocialMediaShare.vue";
import { mapState } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";

export default {
  name: "ChartAction",
  components: { EclLink, EclSocialMediaShare },
  props: {
    chart: {
      type: Object,
      required: false,
      default: null,
    },
  },
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    ...mapState(useChartGroupStore, ["currentChartGroupCode"]),
    embedURL() {
      const url = new URL(this.$route.href, window.location);
      url.searchParams.set("embed", "true");
      return url.toString();
    },
  },
  methods: {
    printPage() {
      window.print();
    },
    printChart() {
      this.chart.print();
    },
    downloadChart() {
      this.chart.exportChartLocal();
    },
    exportChart() {
      this.chart.downloadXLS();
    },
  },
};
</script>
<style scoped>
.chart-actions > * {
  margin-bottom: 1rem;
}
</style>
