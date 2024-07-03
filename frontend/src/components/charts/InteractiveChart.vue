<template>
  <div
    class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m ecl-u-screen-only chart-filters"
  >
    <component
      :is="item.component"
      v-for="item in normalizedFilterComponents"
      :key="item.key"
      v-bind="item.attrs"
      :ref="item.key"
      v-on="item.on"
    />
  </div>
  <div
    class="ecl-u-mt-m ecl-u-mb-m ecl-u-border-width-1 ecl-u-border-style-solid ecl-u-border-color-grey-10 chart-container-digital-agenda"
    :class="chartComponent?.name"
  >
    <component :is="chartComponent" ref="chart" />
  </div>
</template>

<script>
import CardNav from "@/components/CardNav.vue";
import ChartActions from "@/components/charts/ChartActions.vue";
import ChartDefinitions from "@/components/charts/ChartDefinitions.vue";
import EclIcon from "@/components/ecl/EclIcon.vue";
import { setHighchartsDefaults } from "@/initHighchart";
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
        // Normalize each filter component of the axis
        const axisResult = items
          .filter((item) => !!item)
          .map((item) => this.normalizeFilterComponent(item, axis));

        // Sort them according to the chart rules (if any)
        const filterOrder = [
          // Fixed order
          "EclHeading",
          // Custom order
          ...(this.currentChart.filter_order ?? []),
          // Default order
          ...axisResult.map((item) => item.filterType),
        ];
        axisResult.sort((a, b) => {
          const filterPositionA = filterOrder.indexOf(a.filterType);
          const filterPositionB = filterOrder.indexOf(b.filterType);
          return filterPositionA - filterPositionB;
        });

        // Add extra filter params based on the previous filters; that way
        // we should never have impossible combinations.
        const previousParams = [];
        for (const filterComponent of axisResult) {
          filterComponent.attrs.extraParams = [
            ...(filterComponent.attrs.extraParams ?? []),
            ...previousParams,
          ];

          if (filterComponent.queryName && !filterComponent.isMultiple) {
            previousParams.push(filterComponent.queryName);
          }
        }

        // When one filter changes load the next one in order.
        // This should avoid race conditions that can cause filter values
        // to be reset from the query params.
        for (let i = 0; i < axisResult.length; i++) {
          const filterComponent = axisResult[i];
          const nextFilter = axisResult[i + 1];
          if (nextFilter) {
            filterComponent.on.change = () => {
              console.log(filterComponent.key, nextFilter.key);
              if (this.$refs[nextFilter.key]) {
                this.$refs[nextFilter.key][0].load();
              }
            };
          }
        }

        result.push(...axisResult);
      }

      return result;
    },
  },
  beforeMount() {
    setHighchartsDefaults();
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
      result.isMultiple = result.component.computed?.multiple?.();
      result.queryName = result.component.computed?.queryName?.();
      result.filterType = result.queryName ?? result.component.name;
      result.attrs.axis ??= suffix;
      result.attrs.showAxisLabel ??= this.$refs.chart.showAxisLabel;

      result.attrs.class = [
        ...(result.attrs.class || []),
        "chart-filter",
        `chart-filter${suffix}`,
      ];
      result.on ??= {};

      return result;
    },
  },
};
</script>

<style scoped></style>
