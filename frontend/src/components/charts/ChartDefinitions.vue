<template>
  <div
    v-for="item in items"
    :key="item.itemType + item.code"
    class="ecl-u-type-paragraph"
  >
    <div class="ecl-u-mt-m">
      <b>{{ item.dimensionLabel }}:&nbsp;</b>
      <span>{{ item.label || item.alt_label }}</span>
    </div>
    <div class="ecl-u-ml-m ecl-u-mt-m">
      <dimension-prop :value="item?.definition" label="Definition:" />
      <dimension-prop :value="item?.note" label="Notes:" />

      <div
        v-for="data_source in item.data_sources ?? []"
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
        <dimension-prop
          :value="dataSourceByCode.get(data_source)?.definition"
        />
        <dimension-prop
          :value="dataSourceByCode.get(data_source)?.note"
          label="Notes:"
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
    />
  </p>
</template>

<script>
import DimensionProp from "@/components/charts/DimensionProp.vue";
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
  components: { DimensionProp, EclLink },
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
          let dimensionLabel = this.currentLabels[itemType] || itemType;
          // coerce all values to array if not already, to support
          // multiple definitions of the same type
          const items = forceArray(this.filterStore[axis][itemType]);

          if (axis && this.showAxisLabel) {
            dimensionLabel = `(${axis}) ${dimensionLabel}`;
          }

          // If the dimension group doesn't have any extra information that
          // needs to be displayed, put them on the same line.
          const sameLine =
            items.length > 0 &&
            items.every(
              (item) =>
                !item.definition &&
                !item.note &&
                (!item.data_sources || item.data_sources.length === 0),
            );

          if (sameLine) {
            result.push({
              dimensionLabel,
              itemType,
              label: items
                .map((item) => (item.label || item.alt_label || "").trim())
                .join(", "),
            });
          } else {
            for (const item of items) {
              result.push({
                dimensionLabel,
                itemType,
                ...item,
              });
            }
          }
        }
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
