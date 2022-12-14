<template>
  <chart-group-nav v-if="!chartStore.currentChartCode">
    <ecl-spinner v-if="chartGroupStore.isLoading" size="large" centered />
    <div v-else v-html="chartGroupStore.currentChartGroup.description" />

    <h4>Please select one of the available charts:</h4>

    <hr class="ecl-u-border-color-primary" />

    <ecl-list-illustration
      :items="items"
      :loading="chartStore.isLoading"
      zebra
      small
    >
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
import { mapStores } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";

import chartRegistry from "@/lib/chartRegistry";
import placeholderImageURL from "@/assets/placeholder.png?url";

import EclSpinner from "@/components/ecl/EclSpinner.vue";
import ChartGroupNav from "@/components/ChartGroupNav.vue";
import EclListIllustration from "@/components/ecl/EclListIllustration.vue";

export default {
  name: "ChartListView",
  components: { EclListIllustration, ChartGroupNav, EclSpinner },
  computed: {
    ...mapStores(useChartStore, useChartGroupStore),
    chartListForCurrentGroup() {
      return this.chartStore.chartList.filter(
        (item) =>
          item.chart_group === this.chartGroupStore.currentChartGroupCode
      );
    },
    items() {
      return this.chartListForCurrentGroup.map((chart, index) => {
        return {
          id: chart.code,
          title: `${index + 1}. ${chart.name}`,
          image:
            chart.image ||
            chartRegistry[chart.chart_type]?.image ||
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
