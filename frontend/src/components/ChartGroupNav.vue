<template>
  <div
    class="ecl-row ecl-u-pt-m ecl-u-d-flex"
    :class="`ecl-u-d-${mobileBreakpoint}-none`"
  >
    <div class="ecl-col-12">
      <ecl-tabs :items="navRoutes" hide-controls />
    </div>
  </div>

  <div class="ecl-row">
    <div class="ecl-col-12" :class="`ecl-col-${mobileBreakpoint}-8`">
      <slot></slot>
    </div>

    <div
      class="ecl-u-d-none ecl-col-4"
      :class="`ecl-u-d-${mobileBreakpoint}-flex`"
    >
      <div class="ecl-u-pa-xs">
        <h4>About this dataset</h4>
        <ecl-category-filter :items="navRoutes" />
      </div>
    </div>
  </div>
</template>

<script>
import EclTabs from "@/components/ecl/navigation/EclTabs.vue";
import EclCategoryFilter from "@/components/ecl/EclCategoryFilter.vue";

export default {
  name: "ChartGroupNav",
  components: { EclTabs, EclCategoryFilter },
  data() {
    return {
      mobileBreakpoint: "l",
    };
  },
  computed: {
    navRoutes() {
      const params = {
        chartGroupCode: this.$route.params.chartGroupCode,
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
          id: "feedback",
          text: "Submit feedback",
          to: { name: "feedback" },
        },
      ];
    },
  },
};
</script>

<style scoped></style>
