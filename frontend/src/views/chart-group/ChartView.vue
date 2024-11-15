<template>
  <interactive-chart ref="interactiveChart" :key="currentChart.code" />
  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m"
  >
    <h2>Definition and scopes:</h2>

    <div class="ecl-row">
      <div class="ecl-col-12 ecl-col-l-8 chart-definitions">
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div v-html="currentChart.description" />
        <chart-definitions :show-axis-label="chartRef?.showAxisLabel" />
      </div>

      <hr
        class="actions-separator ecl-u-border-color-grey-50 ecl-u-d-block ecl-u-d-l-none"
      />

      <div class="ecl-col-12 ecl-col-l-4 ecl-u-screen-only">
        <chart-actions :chart-ref="chartRef" />
      </div>
    </div>
  </div>

  <div class="ecl-u-screen-only">
    <h2>See more charts for the same data</h2>
    <card-nav :items="chartNavKeepFilters" />
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import ChartActions from "@/components/charts/ChartActions.vue";
import ChartDefinitions from "@/components/charts/ChartDefinitions.vue";
import CardNav from "@/components/CardNav.vue";
import SimpleSpinner from "@/components/SimpleSpinner.vue";
import { defineAsyncComponent } from "vue";

export default {
  name: "ChartView",
  components: {
    CardNav,
    ChartDefinitions,
    ChartActions,
    InteractiveChart: defineAsyncComponent({
      loader: () => import("@/components/charts/InteractiveChart.vue"),
      loadingComponent: SimpleSpinner,
    }),
  },
  computed: {
    ...mapState(useChartStore, ["currentChart", "chartNavForCurrentGroup"]),
    chartRef() {
      return this.$refs.interactiveChart?.$refs.chart;
    },
    chartNavKeepFilters() {
      return this.chartNavForCurrentGroup.map((item) => {
        const newRoute = {
          ...item.to,
          query: {
            ...item.to.query,
            // This is slightly problematic as it will include:
            //  - extra filters that are not used in the other chart
            //    will be incorrectly kept in the URL
            //  - multi-axis charts are completely incompatible with single
            //  - if a filter changes from multi to single, only one
            //    value will be used from the list in the other chart
            ...this.$route.query,
          },
        };
        return {
          ...item,
          to: newRoute,
        };
      });
    },
  },
};
</script>

<style scoped>
.actions-separator {
  width: 100%;
  margin: 0.5rem 1rem 1.5rem 1rem;
}
</style>
