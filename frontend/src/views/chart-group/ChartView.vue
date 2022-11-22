<template>
  <component :is="chartComponent" />
  <div v-html="currentChart.description" />
</template>

<script>
import { mapState } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { CHARTS } from "@/lib/constants";

export default {
  name: "ChartView",
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    chartComponent() {
      return CHARTS[this.currentChart.chart_type].component;
    },
  },
};
</script>

<style scoped></style>
