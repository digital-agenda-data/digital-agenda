<template>
  <div v-if="isVisible" class="breakdown-weights ecl-u-mb-m">
    <b class="ecl-u-type-color-grey-75">Click to drill down</b>
    <span></span>
    <b class="ecl-u-type-color-grey-75">Normalized</b>

    <template v-for="item in apiData" :key="item.code">
      <ecl-link
        :to="{
          name: $route.name,
          params: $route.params,
          query: {
            indicator: item.code,
            period: $route.query.period,
            noWeights: 'true',
          },
        }"
        no-visited
      >
        {{ getDisplay(item) }}
      </ecl-link>
      <range-filter :query-name="item.code" />
      <span class="ecl-u-type-align-center">
        {{ getNormalized(item.code) }}%
      </span>
    </template>
  </div>
</template>

<script>
import BreakdownMultiFilter from "@/components/filters/BreakdownMultiFilter.vue";
import RangeFilter from "@/components/filters/base/RangeFilter.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "BreakdownWeightsFilter",
  components: { EclLink, RangeFilter },
  extends: BreakdownMultiFilter,
  computed: {
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
      return this.apiData.length > 1 && this.$route.query.noWeights !== "true";
    },
  },
  watch: {
    apiDataRaw(newValue, oldValue) {
      const newQuery = { ...this.$route.query };

      // Delete old values (if any)
      for (const item of oldValue || []) {
        delete newQuery[item.code];
      }

      // Set all values to default of 5
      for (const item of newValue || []) {
        newQuery[item.code] = 5;
      }

      this.$router.replace({ query: newQuery });
    },
  },
  methods: {
    getNormalized(code) {
      return ((this.rawValues[code] / this.total) * 100).toFixed(2);
    },
  },
};
</script>

<style scoped>
.breakdown-weights {
  display: grid;
  align-items: center;
  grid-gap: 1rem;
  grid-template-columns: 180px auto 100px;
}
</style>
