<template>
  <component :is="chartComponent" />
</template>

<script>
import { mapState } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import chartComponents from "@/lib/chartComponents";

export default {
  name: "ChartView",
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    chartComponent() {
      return chartComponents[this.currentChart.chart_type].component;
    },
  },
};
</script>

<style scoped></style>
