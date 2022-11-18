<template>
  <chart-group-nav>
    <p>TODO List of charts</p>
  </chart-group-nav>
</template>

<script>
import { mapState } from "pinia";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import ChartGroupNav from "@/components/ChartGroupNav.vue";

export default {
  name: "ChartListView",
  components: { ChartGroupNav },
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroup"]),
  },
};
</script>

<style scoped></style>
