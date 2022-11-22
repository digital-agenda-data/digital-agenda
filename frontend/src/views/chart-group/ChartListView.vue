<template>
  <chart-group-nav v-if="!currentChartCode">
    <div v-html="currentChartGroup.description" />

    <h4>Please select one of the available charts:</h4>

    <hr class="ecl-u-border-color-primary" />

    <ecl-list-illustration :items="items" zebra small>
      <template #description="{ item }">
        <div v-html="item.description" />
      </template>
    </ecl-list-illustration>
  </chart-group-nav>
  <div v-else class="ecl-u-pt-m">
    <router-view />
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import ChartGroupNav from "@/components/ChartGroupNav.vue";
import { useChartStore } from "@/stores/chartStore";
import placeholderImageURL from "@/assets/placeholder.png?url";
import EclListIllustration from "@/components/ecl/EclListIllustration.vue";
import { CHARTS } from "@/lib/constants";

export default {
  name: "ChartListView",
  components: { EclListIllustration, ChartGroupNav },
  computed: {
    ...mapState(useChartStore, ["charts", "currentChartCode"]),
    ...mapState(useChartGroupStore, [
      "currentChartGroup",
      "currentChartGroupCode",
    ]),
    chartListForCurrentGroup() {
      return this.charts.filter(
        (item) => item.chart_group === this.currentChartGroupCode
      );
    },
    items() {
      return this.chartListForCurrentGroup.map((chart, index) => {
        return {
          id: chart.code,
          title: `${index + 1}. ${chart.name}`,
          image:
            chart.image ||
            CHARTS[chart.chart_type]?.image ||
            placeholderImageURL,
          description: chart.description,
          to: {
            name: "chart-view",
            params: {
              chartGroupCode: chart.chart_group,
              chartCode: chart.code,
            },
          },
          label: chart.is_draft ? "draft" : null,
          labelVariant: "high",
        };
      });
    },
  },
};
</script>

<style scoped></style>
