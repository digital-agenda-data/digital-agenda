<template>
  <chart-group-nav v-if="!chartStore.currentChartCode">
    <ecl-spinner v-if="chartGroupStore.isLoading" size="large" centered />
    <!-- eslint-disable-next-line vue/no-v-html -->
    <div v-else v-html="chartGroupStore.currentChartGroup.description" />

    <h4>Please select one of the available charts:</h4>

    <hr class="ecl-u-border-color-primary" />

    <ecl-list-illustration
      :items="chartStore.chartNavForCurrentGroup"
      :loading="chartStore.isLoading"
      show-index
      zebra
      small
    >
      <template #description="{ item }">
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div v-html="item.description" />
      </template>
    </ecl-list-illustration>

    <h4>Further information</h4>

    <chart-group-extra-links
      v-if="chartGroupStore.currentChartGroupCode"
      :chart-group-code="chartGroupStore.currentChartGroupCode"
    />
  </chart-group-nav>
  <div v-else class="ecl-u-pt-m">
    <router-view />
  </div>
</template>

<script>
import { mapStores } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";

import EclSpinner from "@/components/ecl/EclSpinner.vue";
import ChartGroupNav from "@/components/ChartGroupNav.vue";
import EclListIllustration from "@/components/ecl/EclListIllustration.vue";
import ChartGroupExtraLinks from "@/components/ChartGroupExtraLinks.vue";

export default {
  name: "ChartListView",
  components: {
    ChartGroupExtraLinks,
    EclListIllustration,
    ChartGroupNav,
    EclSpinner,
  },
  computed: {
    ...mapStores(useChartStore, useChartGroupStore),
  },
};
</script>

<style scoped></style>
