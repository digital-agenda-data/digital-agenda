<template>
  <template v-for="(itemList, label) in items" :key="label">
    <div
      v-for="item in itemList"
      :key="label + item.code"
      class="ecl-u-type-paragraph"
    >
      <div class="ecl-u-mt-m">
        <b>{{ label }}:&nbsp;</b>
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
  </template>

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
import { mapState } from "pinia";
import { useChartStore } from "@/stores/chartStore";
import { api } from "@/lib/api";
import { setEquals } from "@/lib/utils";
import { useChartGroupStore } from "@/stores/chartGroupStore";

export default {
  name: "ChartDefinitions",
  components: { EclLink },
  props: {
    define: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      dataSources: new Map(),
    };
  },
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    ...mapState(useChartGroupStore, ["currentChartGroupCode"]),
    items() {
      const result = {};
      for (const [label, val] of Object.entries(this.define)) {
        // coerce all values to array if not already, to support
        // multiple definitions of the same type
        if (!val) {
          result[label] = [];
        } else if (Array.isArray(val)) {
          result[label] = val;
        } else {
          result[label] = [val];
        }
      }
      return result;
    },
    dataSourceCodes() {
      const result = new Set();

      for (const itemList of Object.values(this.items)) {
        for (const item of itemList) {
          if (item.data_source) {
            result.add(item.data_source);
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
