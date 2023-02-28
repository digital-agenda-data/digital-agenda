<template>
  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m ecl-u-screen-only chart-filters"
  >
    <component
      :is="item.component"
      v-for="item in normalizedFilterComponents"
      :key="item.key"
      v-bind="item.attrs"
    />
  </div>
  <div
    class="ecl-u-mt-m ecl-u-mb-m ecl-u-border-width-1 ecl-u-border-style-solid ecl-u-border-color-grey-10 chart-container-digital-agenda"
  >
    <component :is="chartComponent" ref="chart" />
  </div>
</template>

<script>
import CardNav from "@/components/CardNav.vue";
import ChartActions from "@/components/charts/ChartActions.vue";
import ChartDefinitions from "@/components/charts/ChartDefinitions.vue";
import EclIcon from "@/components/ecl/EclIcon.vue";
import chartRegistry from "@/lib/chartRegistry";
import { FILTER_SUFFIXES } from "@/lib/constants";
import { useChartStore } from "@/stores/chartStore";
import { mapState } from "pinia";

export default {
  name: "InteractiveChart",
  components: { CardNav, EclIcon, ChartDefinitions, ChartActions },
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    chartComponent() {
      return chartRegistry[this.currentChart.chart_type];
    },
    /**
     * Normalize components to Objects with key, component
     * and attrs attributes.
     */
    normalizedFilterComponents() {
      const result = [];
      for (const axis of FILTER_SUFFIXES) {
        const items = this.$refs.chart?.[`filter${axis}Components`] ?? [];

        for (const item of items) {
          if (!item) {
            continue;
          }

          result.push(this.normalizeFilterComponent(item, axis));
        }
      }
      return result;
    },
  },
  methods: {
    normalizeFilterComponent(item, suffix = "") {
      let result = item;
      if (!item.component) {
        result = {
          component: item,
          attrs: {},
        };
      }

      result.key ??= result.component.name + suffix;
      result.attrs.axis ??= suffix;
      result.attrs.showAxisLabel ??= this.$refs.chart.showAxisLabel;

      result.attrs.class = [
        ...(result.attrs.class || []),
        "chart-filter",
        `chart-filter${suffix}`,
      ];

      return result;
    },
  },
};
</script>

<style scoped></style>
