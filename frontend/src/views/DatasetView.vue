<template>
  <div class="ecl-row">
    <div class="ecl-col-8">
      <router-view />
    </div>

    <div class="ecl-col-4">
      <div class="ecl-u-pa-xs">
        <h4>About this dataset</h4>
        <ecl-category-filter :items="navRoutes" />
      </div>
    </div>
  </div>
</template>

<script>
import EclCategoryFilter from "@/components/ecl/EclCategoryFilter.vue";

export default {
  name: "DatasetView",
  components: { EclCategoryFilter },
  computed: {
    navRoutes() {
      const params = {
        datasetId: this.$route.params.datasetId,
      };

      return [
        {
          id: "charts",
          text: "Charts",
          to: { name: "charts", params },
        },
        {
          id: "indicators",
          text: "Indicators",
          to: { name: "indicators", params },
        },
        {
          id: "metadata",
          text: "Metadata",
          to: { name: "metadata", params },
        },
        {
          id: "comments",
          text: "Comments",
          to: { name: "comments", params },
        },
      ];
    },
  },
};
</script>

<style scoped></style>
