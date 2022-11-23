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
import { apiCall } from "@/lib/api";
import { arrayEquals } from "@/lib/utils";
import { useChartGroupStore } from "@/stores/chartGroupStore";

export default {
  name: "ChartDefinitions",
  components: { EclLink },
  props: {
    indicator: {
      type: [Object, Array],
      required: false,
      default: null,
    },
    breakdown: {
      type: [Object, Array],
      required: false,
      default: null,
    },
    unit: {
      type: [Object, Array],
      required: false,
      default: null,
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
    indicatorList() {
      if (!this.indicator) return [];
      if (Array.isArray(this.indicator)) return this.indicator;
      return [this.indicator];
    },
    breakdownList() {
      if (!this.breakdown) return [];
      if (Array.isArray(this.breakdown)) return this.breakdown;
      return [this.breakdown];
    },
    unitList() {
      if (!this.unit) return [];
      if (Array.isArray(this.unit)) return this.unit;
      return [this.unit];
    },
    items() {
      return {
        Indicator: this.indicatorList,
        Breakdown: this.breakdownList,
        Unit: this.unitList,
      };
    },
    dataSourceCodes() {
      return this.indicatorList
        .filter((indicator) => indicator.data_source)
        .map((indicator) => indicator.data_source);
    },
  },
  watch: {
    dataSourceCodes(newValue, oldValue) {
      if (!arrayEquals(newValue, oldValue)) {
        this.loadDataSources();
      }
    },
  },
  mounted() {
    this.loadDataSources();
  },
  methods: {
    async loadDataSources() {
      if (this.dataSourceCodes.length === 0) return;

      const resp = await apiCall("GET", "/data-sources/", {
        code_in: this.dataSourceCodes.join(","),
      });

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
