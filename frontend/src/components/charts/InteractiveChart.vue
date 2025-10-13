<template>
  <div
    class="ecl-u-bg-neutral-60 ecl-u-border-color-secondary ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m ecl-u-screen-only chart-filters"
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
    class="ecl-u-mt-m ecl-u-mb-m ecl-u-border-width-1 ecl-u-border-style-solid ecl-u-border-color-neutral-60 chart-container-digital-agenda"
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

        result.push(...this.setLoadOrder(axisResult));
      }

      return result;
    },
  },
  watch: {
    currentChart() {
      // Reload in case the filter options have changed.
      this.initialFiltersLoad();
    },
  },
  beforeMount() {
    setHighchartsDefaults();
  },
  mounted() {
    this.initialFiltersLoad();
  },
  methods: {
    initialFiltersLoad() {
      // Next tick, so the filter components are loaded and available as refs.
      this.$nextTick(() => {
        this.normalizedFilterComponents
          .filter((item) => item.initialLoad)
          .forEach((item) => {
            this.$refs[item.key][0].load?.();
          });
      });
    },
    /**
     * Sort the filter components according to any custom settings in the
     * backend and configure them to:
     *
     *  - Send extra query parameters to the backend API when to filter
     *    the results; using the configured order.
     *  - When one value is changed, trigger a chained reload of the other
     *    filters in the correct order.
     *  - Mark which filters are first and trigger a load on mount and chart
     *    changes.
     */
    setLoadOrder(axisFilterComponents) {
      // Sort them according to the chart rules (if any)
      const filterOrder = [
        // Fixed order
        "EclHeading",
        // Custom order
        ...(this.currentChart.filter_order ?? []),
        // Default order
        ...axisFilterComponents.map((item) => item.filterType),
      ];

      axisFilterComponents.sort((a, b) => {
        const filterPositionA = filterOrder.indexOf(a.filterType);
        const filterPositionB = filterOrder.indexOf(b.filterType);
        return filterPositionA - filterPositionB;
      });

      // Add extra filter params based on the previous filters; that way
      // we should never have impossible combinations.
      const previousComponents = [];
      for (const filterComponent of axisFilterComponents) {
        filterComponent.triggerLoadFor = [];
        filterComponent.attrs.extraParams = [
          ...(filterComponent.attrs.extraParams ?? []),
          ...previousComponents.map((i) => i.queryName),
        ];

        if (previousComponents.length === 0) {
          // Set the first one to load on mount and start the chain.
          // Since it has no parent filter in the chain.
          filterComponent.initialLoad = true;
        } else {
          // Add this filter to the chain load of the last component
          previousComponents.slice(-1)[0].triggerLoadFor.push(filterComponent);
        }

        // When one filter changes load the next one in order.
        // This should avoid race conditions that can cause filter values
        // to be reset from the query params in case of weird order loading.
        filterComponent.on.change = () => {
          filterComponent.triggerLoadFor.forEach((nextFilter) => {
            this.$refs[nextFilter.key][0].load?.();
          });
        };

        if (filterComponent.queryName && !filterComponent.isMultiple) {
          previousComponents.push(filterComponent);
        }
      }
      return axisFilterComponents;
    },
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
