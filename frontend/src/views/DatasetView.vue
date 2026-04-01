<template>
  <router-view />

  <div v-if="filteredChartGroupNavItems.length > 0" class="ecl-u-screen-only">
    <h3>Browse other datasets</h3>
    <card-nav :items="filteredChartGroupNavItems" />
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useChartGroupStore } from "@/stores/chartGroupStore";

import CardNav from "@/components/CardNav.vue";

export default {
  name: "DatasetView",
  components: { CardNav },
  computed: {
    ...mapState(useChartGroupStore, [
      "currentChartGroup",
      "chartGroupNavItems",
    ]),
    filteredChartGroupNavItems() {
      return this.chartGroupNavItems.filter(
        (item) => item.id !== this.currentChartGroup.code,
      );
    },
  },
};
</script>

<style scoped></style>
