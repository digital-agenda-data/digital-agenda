<template>
  <ecl-list-illustration
    :items="chartGroupStore.chartGroupNavItems"
    :loading="chartGroupStore.isLoading"
    show-index
    zebra
  >
    <template #description="{ item }">
      <!-- eslint-disable-next-line vue/no-v-html -->
      <div v-html="item.description" />

      <chart-group-extra-links
        :chart-group-code="item.id"
        class="ecl-u-d-none ecl-u-d-m-block"
      />
    </template>
  </ecl-list-illustration>
</template>

<script>
import { mapStores } from "pinia";

import { useChartGroupStore } from "@/stores/chartGroupStore";

import EclListIllustration from "@/components/ecl/EclListIllustration.vue";
import ChartGroupExtraLinks from "@/components/ChartGroupExtraLinks.vue";

export default {
  name: "HomeView",
  components: { ChartGroupExtraLinks, EclListIllustration },
  computed: {
    ...mapStores(useChartGroupStore),
  },
};
</script>

<style scoped></style>
