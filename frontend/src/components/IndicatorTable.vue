<template>
  <div class="parent-header">
    <div class="table-section-header" :style="{ color: parent.colors[0] }">
      <img v-if="parent.icon" :src="parent.icon" alt="" />
      <span>{{ parent.label || currentChartGroup.short_name }}</span>
    </div>
  </div>
  <ecl-table class="ecl-u-break-word">
    <indicator-group-table
      v-for="group in parent.members"
      :key="group.code"
      :group="group"
      :parent="parent"
    />
  </ecl-table>
</template>

<script>
import EclTable from "@/components/ecl/table/EclTable.vue";
import IndicatorGroupTable from "@/components/IndicatorGroupTable.vue";
import { useChartGroupStore } from "@/stores/chartGroupStore.js";
import { useChartStore } from "@/stores/chartStore.js";
import { mapState } from "pinia";

export default {
  name: "IndicatorTable",
  components: {
    IndicatorGroupTable,
    EclTable,
  },
  props: {
    parent: {
      type: Object,
      required: false,
      default: null,
    },
  },
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroup"]),
    ...mapState(useChartStore, ["defaultChartForCurrentGroup"]),
  },
};
</script>

<style scoped lang="scss">
.parent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  * {
    text-transform: uppercase;
    font-weight: bold;
  }
}
</style>
