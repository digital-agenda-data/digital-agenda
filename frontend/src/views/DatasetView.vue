<template>
  <router-view />

  <div class="ecl-u-screen-only">
    <h4>Browse other datasets</h4>
    <card-nav :items="chartGroupNavItems" />
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
    ...mapState(useChartGroupStore, ["chartGroupNavItems"]),
  },
};
</script>

<style scoped></style>
