<template>
  <div v-html="currentChart.description" />
</template>

<script>
import { mapState } from "pinia";
import { useChartStore } from "@/stores/chartStore";

export default {
  name: "ChartView",
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
  },
};
</script>

<style scoped></style>
