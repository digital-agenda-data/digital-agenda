<template>
  <div v-if="isVisible" class="breakdown-weights ecl-u-mb-m">
    <b class="ecl-u-type-color-grey-75"> Click to drill down </b>
    <b class="breakdown-weights-extra-header"></b>
    <b class="ecl-u-type-color-grey-75 ecl-u-type-align-center"> Normalized </b>

    <template v-for="item in apiData" :key="item.code">
      <ecl-link
        class="breakdown-weights-drill-down"
        :to="getDefaultChartRoute(item)"
        no-visited
      >
        {{ item.display }}
      </ecl-link>
      <range-filter :query-name="item.code" />
      <span class="ecl-u-type-align-center">
        {{ getNormalized(item.code) }}%
      </span>
    </template>
  </div>
</template>

<script>
import BreakdownMultiFilter from "@/components/chart-filters/BreakdownMultiFilter.vue";
import RangeFilter from "@/components/chart-filters/RangeFilter.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { mapState } from "pinia";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useChartStore } from "@/stores/chartStore";

export default {
  name: "BreakdownWeightsFilter",
  components: { EclLink, RangeFilter },
  extends: BreakdownMultiFilter,
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroup"]),
    ...mapState(useChartStore, ["defaultChartForGroup"]),
    rawValues() {
      const result = {};

      for (const item of this.apiData) {
        result[item.code] = parseInt(this.$route.query[item.code] ?? 5);
      }

      return result;
    },
    total() {
      return Object.values(this.rawValues).reduce((a, b) => a + b, 0);
    },
    isVisible() {
      return this.apiData.length > 1;
    },
  },
  methods: {
    getNormalized(code) {
      return ((this.rawValues[code] / this.total) * 100).toFixed(2);
    },
    getDefaultChartRoute(item) {
      const chart = this.defaultChartForGroup[this.currentChartGroup.code];
      return {
        name: "chart-view",
        params: {
          chartCode: chart.code,
          chartGroupCode: this.currentChartGroup.code,
        },
        query: {
          period: this.$route.query.period,
          indicator: item.code,
          indicatorGroup: item.group,
        },
      };
    },
  },
};
</script>

<style scoped>
.breakdown-weights-extra-header {
  display: none;
}

.breakdown-weights {
  display: grid;
  align-items: center;
  grid-gap: 1rem;
  grid-template-columns: 1fr auto;
}

.breakdown-weights-drill-down {
  grid-column: span 2;
}

@media (min-width: 768px) {
  .breakdown-weights-extra-header {
    display: inline;
  }

  .breakdown-weights {
    grid-auto-rows: 2.15em;
    grid-template-columns: 12rem auto 12rem;
  }

  .breakdown-weights-drill-down {
    grid-column: auto;
  }
}
</style>
