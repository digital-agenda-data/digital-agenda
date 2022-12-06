<template>
  <div
    v-for="item in items"
    :key="item.itemType + item.code"
    class="ecl-u-type-paragraph"
  >
    <div class="ecl-u-mt-m">
      <b>{{ item.itemType }}:&nbsp;</b>
      <span>{{ item.label || item.alt_label }}</span>
    </div>
    <div class="ecl-u-ml-m ecl-u-mt-m">
      <div v-if="item.definition">
        <b>Definition:&nbsp;</b>
        <span>{{ item.definition }}</span>
      </div>

      <div v-if="item.note">
        <b>Notes:&nbsp;</b>
        <span>{{ item.note }}</span>
      </div>

      <div v-if="item.data_source">
        <b>Data Source:&nbsp;</b>
        <span>
          {{ dataSources.get(item.data_source)?.label || item.data_source }}
        </span>
        <span>&nbsp;</span>
        <ecl-link
          v-if="dataSources.get(item.data_source)?.url"
          :to="dataSources.get(item.data_source)?.url"
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
import { mapState, mapStores } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { api } from "@/lib/api";
import { setEquals } from "@/lib/utils";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useFilterStore } from "@/stores/filterStore";

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
  data() {
    return {
      dataSources: new Map(),
    };
  },
  computed: {
    ...mapStores(useFilterStore),
    ...mapState(useChartStore, ["currentChart"]),
    ...mapState(useChartGroupStore, ["currentChartGroupCode"]),
    dataSourceCodes() {
      return new Set(
        this.items.map((item) => item.data_source).filter((code) => !!code)
      );
    },
    items() {
      const result = [];
      for (const axis of ["", "X", "Y", "Z"]) {
        for (let itemType of ["Indicator", "Breakdown", "Unit"]) {
          let items = null;
          const val = this.filterStore[axis][itemType.toLowerCase()];

          if (axis && this.showAxisLabels) {
            itemType = `(${axis}) ${itemType}`;
          }

          // coerce all values to array if not already, to support
          // multiple definitions of the same type
          if (!val) {
            items = [];
          } else if (Array.isArray(val)) {
            items = val;
          } else {
            items = [val];
          }

          for (const item of items) {
            result.push({
              itemType,
              ...item,
            });
          }
        }
      }
      return result;
    },
  },
  watch: {
    dataSourceCodes(newValue, oldValue) {
      if (!setEquals(newValue, oldValue)) {
        this.loadDataSources();
      }
    },
  },
  mounted() {
    this.loadDataSources();
  },
  methods: {
    async loadDataSources() {
      if (this.dataSourceCodes.size === 0) return;

      const resp = (
        await api.get("/data-sources/", {
          params: { code_in: Array.from(this.dataSourceCodes).join(",") },
        })
      ).data;

      const result = new Map();
      for (const item of resp) {
        result.set(item.code, item);
      }

      this.dataSources = result;
    },
  },
};
</script>

<style scoped></style>
