<template>
  <div>
    <div v-html="dataset.description" />
    <p>TODO List of charts</p>
  </div>
</template>

<script>
import chartGroupStore from "@/stores/chartGroupStore";

export default {
  name: "ChartListView",
  computed: {
    chartGroupStore: () => chartGroupStore(),
    dataset() {
      return this.chartGroupStore.chartGroups.find(
        (item) => item.code === this.$route.params.chartGroupCode
      );
    },
  },
};
</script>

<style scoped></style>
