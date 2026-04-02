<template>
  <router-view />

  <div v-if="chartGroupNavItems.length > 0" class="ecl-u-screen-only">
    <h3>Browse other datasets</h3>
    <card-nav
      :items="chartGroupNavItems"
      :current-id="currentChartGroup.code"
    />
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
  },
};
</script>

<style scoped></style>
