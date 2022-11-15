<template>
  <div>
    <p>
      {{ dataset.description }}
    </p>
    <p>TODO List of charts</p>
  </div>
</template>

<script>
import datasetsStore from "@/stores/datasetsStore";

export default {
  name: "ChartListView",
  computed: {
    datasetsStore: () => datasetsStore(),
    dataset() {
      return this.datasetsStore.datasets.find(
        (item) => item.code === this.$route.params.datasetId
      );
    },
  },
};
</script>

<style scoped></style>
