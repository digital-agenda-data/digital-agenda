<template>
  <chart-group-nav>
    <p>Metadata Stuff</p>
    <ecl-link :to="exportLink" no-visited label="Export CSV"/>
  </chart-group-nav>
</template>

<script>
import ChartGroupNav from "@/components/ChartGroupNav.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { apiURL } from "@/lib/api";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { mapState } from "pinia";
export default {
  name: "MetadataView",
  components: { EclLink, ChartGroupNav },
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroupCode"]),
    exportLink() {
      return `${apiURL}/chart-groups/${this.currentChartGroupCode}/facts/`
    }
  },
};
</script>

<style scoped></style>
