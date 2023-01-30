<template>
  <div
    v-for="item in items"
    :key="item.itemType + item.code"
    class="ecl-u-type-paragraph"
  >
    <div class="ecl-u-mt-m">
      <b>{{ item.display }}:&nbsp;</b>
      <span>{{ item.label || item.alt_label }}</span>
    </div>
    <div class="ecl-u-ml-m ecl-u-mt-m">
      <div v-if="item.definition">
        <b>Definition:&nbsp;</b>
        <span v-html="item.definition" />
      </div>

      <div v-if="item.note">
        <b>Notes:&nbsp;</b>
        <span>{{ item.note }}</span>
      </div>

      <div
        v-for="data_source in item.data_sources"
        :key="item.code + data_source"
      >
        <b>Data Source:&nbsp;</b>
        <span>
          {{ dataSourceByCode.get(data_source)?.label || data_source }}
        </span>
        <span>&nbsp;</span>
        <ecl-link
          v-if="dataSourceByCode.get(data_source)?.url"
          :to="dataSourceByCode.get(data_source)?.url"
          label="[More information]"
          no-visited
        />
      </div>
    </div>
  </div>

  <p>
    <ecl-link
      :to="{
        name: 'indicators',
        params: {
          chartGroupCode: currentChartGroupCode,
        },
      }"
      variant="primary"
      label="Consult the list of available indicators, their definition and sources"
      no-visited
    />
  </p>
  <p>
    <ecl-link
      :to="{
        name: 'metadata',
        params: {
          chartGroupCode: currentChartGroupCode,
        },
      }"
      label="Entire dataset metadata and download services"
      no-visited
    />
  </p>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { FILTER_SUFFIXES } from "@/lib/constants";
import { mapState, mapStores } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useFilterStore } from "@/stores/filterStore";
import { useDataSourceStore } from "@/stores/dataSourceStore";
import { forceArray } from "@/lib/utils";

export default {
  name: "ChartDefinitions",
  components: { EclLink },
  props: {
    showAxisLabel: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  computed: {
    ...mapStores(useFilterStore),
    ...mapState(useChartStore, ["currentChart"]),
    ...mapState(useChartGroupStore, ["currentLabels", "currentChartGroupCode"]),
    ...mapState(useDataSourceStore, ["dataSourceByCode"]),
    items() {
      const result = [];
      for (const axis of FILTER_SUFFIXES) {
        for (const itemType of ["indicator", "breakdown", "unit"]) {
          let display = this.currentLabels[itemType] || itemType;
          const items = this.filterStore[axis][itemType];

          if (axis && this.showAxisLabel) {
            display = `(${axis}) ${display}`;
          }
          // coerce all values to array if not already, to support
          // multiple definitions of the same type
          for (const item of forceArray(items)) {
            result.push({
              display,
              itemType,
              ...item,
            });
          }
        }
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
