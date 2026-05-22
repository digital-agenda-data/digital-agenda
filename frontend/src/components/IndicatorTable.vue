<template>
  <div class="parent-header">
    <div class="table-section-header" :style="{ color: parent.colors[0] }">
      <img v-if="parent.icon" :src="parent.icon" alt="" />
      <span>{{ parent.label || currentChartGroup.short_name }}</span>
    </div>
    <ecl-button
      v-if="collapsed"
      variant="text"
      icon="corner-arrow-down"
      label="Show indicators"
      icon-position="right"
      @click="collapsed = false"
    />
    <ecl-button
      v-else
      variant="text"
      icon="corner-arrow-up"
      label="Hide indicators"
      icon-position="right"
      @click="collapsed = true"
    />
  </div>
  <ecl-table class="ecl-u-break-word">
    <template v-for="group in parent.members" :key="group.code">
      <ecl-thead>
        <ecl-tr :id="group.code" :style="{ backgroundColor: parent.colors[0] }">
          <ecl-th>
            {{ group.label }}
          </ecl-th>
          <ecl-th>Time coverage</ecl-th>
          <ecl-th>Export links</ecl-th>
        </ecl-tr>
      </ecl-thead>
      <ecl-tbody v-if="!collapsed">
        <ecl-tr v-for="indicator in group.indicators" :key="indicator.code">
          <ecl-td class="label-cell" header="Indicator">
            <ecl-link
              :to="`#indicator-${indicator.code}`"
              :label="indicator.label"
              no-visited
              variant="brand"
            />
          </ecl-td>
          <ecl-td header="Time coverage">
            {{ indicator.time_coverage }}
          </ecl-td>
          <ecl-td header="Export links">
            <ecl-link
              :to="`${apiURL}/indicators/${indicator.code}/facts/`"
              no-visited
              download-class
              label="data"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/countries/?indicator=${indicator.code}&format=csv`"
              no-visited
              download-class
              label="countries"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/breakdowns/?indicator=${indicator.code}&format=csv`"
              no-visited
              download-class
              label="breakdowns"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/units/?indicator=${indicator.code}&format=csv`"
              no-visited
              download-class
              label="units"
            />
          </ecl-td>
        </ecl-tr>
      </ecl-tbody>
    </template>
  </ecl-table>
</template>

<script>
import EclButton from "@/components/ecl/EclButton.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclTable from "@/components/ecl/table/EclTable.vue";
import EclTbody from "@/components/ecl/table/EclTbody.vue";
import EclTd from "@/components/ecl/table/EclTd.vue";
import EclTh from "@/components/ecl/table/EclTh.vue";
import EclThead from "@/components/ecl/table/EclThead.vue";
import EclTr from "@/components/ecl/table/EclTr.vue";
import { apiURL } from "@/lib/api.js";
import { useChartGroupStore } from "@/stores/chartGroupStore.js";
import { useChartStore } from "@/stores/chartStore.js";
import { mapState } from "pinia";

export default {
  name: "IndicatorTable",
  components: {
    EclButton,
    EclTd,
    EclTbody,
    EclTr,
    EclTh,
    EclThead,
    EclTable,
    EclLink,
  },
  props: {
    parent: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      apiURL,
      collapsed: true,
    };
  },
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroup"]),
    ...mapState(useChartStore, ["defaultChartForCurrentGroup"]),
  },
};
</script>

<style scoped lang="scss">
th:first-of-type {
  width: 60%;
}

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
