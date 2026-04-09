<template>
  <div class="chart-actions">
    <div class="ecl-u-pb-none ecl-u-bg-neutral-50 ecl-u-ph-xl ecl-u-pv-m">
      <ecl-list v-slot="{ item }" :items="actionLinks" divider>
        <ecl-link
          :label="item.label"
          :to="item.to"
          :download-class="item.downloadClass"
          no-visited
          @click.capture="handleAction($event, item.action)"
        />
      </ecl-list>
    </div>

    <transition mode="out-in">
      <div v-if="!shareURL">
        <ecl-button
          v-if="!loading"
          label="Share"
          size="m"
          icon-size="m"
          icon="share"
          variant="secondary"
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
import EclList from "@/components/ecl/EclList.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclSocialMediaShare from "@/components/ecl/EclSocialMediaShare.vue";
import { api } from "@/lib/api";
import { mapState } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";

export default {
  name: "ChartActions",
  components: { EclList, EclSpinner, EclButton, EclLink, EclSocialMediaShare },
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
    shortUrlData() {
      return {
        chart: this.currentChart.id,
        query_arguments:
          "?" + new URLSearchParams(this.$route.query).toString(),
      };
    },
    actionLinks() {
      const exportLinks = Object.entries(this.chartRef?.exportLinks ?? {}).map(
        ([axis, exportLink]) => ({
          id: `export-${axis}`,
          label: `Export data ${axis}`,
          to: exportLink,
          downloadClass: true,
        }),
      );

      const result = [];
      if (this.highchartInstance) {
        result.push({
          id: "print-chart",
          label: "Print chart",
          to: "#print-chart",
          action: () => this.printChart(),
        });
      }
      result.push({
        id: "print-page",
        label: "Print page",
        to: "#print-page",
        action: () => this.printPage(),
      });

      if (this.highchartInstance) {
        result.push(
          {
            id: "download-image",
            label: "Download image",
            to: "#download-chart",
            action: () => this.downloadChart(),
            downloadClass: true,
          },
          {
            id: "download-svg",
            label: "Download SVG",
            to: "#download-chart-svg",
            action: () => this.downloadChart({ type: "image/svg+xml" }),
            downloadClass: true,
          },
        );
      }

      result.push(
        ...exportLinks,
        {
          id: "embed-url",
          label: "Embedded URL",
          to: this.embedURL,
        },
        {
          id: "feedback",
          label: "Submit feedback",
          to: { name: "feedback" },
        },
      );
      return result;
    },
  },
  watch: {
    shortUrlData() {
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
          await api.post("/short-urls/", this.shortUrlData)
        ).data.short_url;
      } finally {
        this.loading = false;
      }
    },
    handleAction(event, action) {
      if (!action) return;
      event.preventDefault();
      action();
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
