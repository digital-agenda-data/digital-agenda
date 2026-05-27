<template>
  <ecl-thead>
    <ecl-tr
      :style="{ backgroundColor: parent.colors[0] }"
      @click="collapsed = !collapsed"
    >
      <ecl-th>
        <div>
          <ecl-link
            :to="`#indicator-group-${group.code}`"
            :label="group.label"
            no-visited
            variant="text"
            inverted
          />
          <div
            :key="collapsed"
            role="button"
            :aria-expanded="!collapsed"
            :aria-controls="tableId"
          >
            <ecl-icon v-if="collapsed" icon="corner-arrow-down" />
            <ecl-icon v-else icon="corner-arrow-up" />
            <span class="ecl-u-sr-only">
              {{ collapsed ? "Expand indicators" : "Collapse indicators" }}
            </span>
          </div>
        </div>
      </ecl-th>
      <ecl-th>Time coverage</ecl-th>
      <ecl-th>Export links</ecl-th>
    </ecl-tr>
  </ecl-thead>
  <ecl-tbody v-show="!collapsed" :id="tableId">
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

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclTbody from "@/components/ecl/table/EclTbody.vue";
import EclTd from "@/components/ecl/table/EclTd.vue";
import EclTh from "@/components/ecl/table/EclTh.vue";
import EclThead from "@/components/ecl/table/EclThead.vue";
import EclTr from "@/components/ecl/table/EclTr.vue";
import { apiURL } from "@/lib/api.js";

export default {
  name: "IndicatorGroupTable",
  components: { EclIcon, EclTd, EclTbody, EclLink, EclTh, EclTr, EclThead },
  props: {
    group: {
      type: Object,
      required: true,
    },
    parent: {
      type: Object,
      required: true,
    },
    forceExpand: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      apiURL,
      collapsed: true,
    };
  },
  computed: {
    tableId() {
      return `indicator-group-table-${this.group.code}`;
    },
  },
};
</script>

<style scoped lang="scss">
thead tr {
  cursor: pointer;
}

th:first-of-type {
  width: 60%;

  div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
  }
}
</style>
