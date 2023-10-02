<template>
  <chart-group-nav>
    <h4>Dataset Metadata</h4>
    <div
      class="ecl-u-bg-grey-10 ecl-u-border-color-yellow ecl-u-border-left ecl-u-border-width-8 ecl-u-pa-m ecl-u-break-word"
    >
      <dl class="ecl-description-list">
        <dt class="ecl-description-list__term">Dataset</dt>
        <dd class="ecl-description-list__definition">
          <ecl-link :to="datasetRoute" :label="datasetLink" no-visited />
        </dd>

        <dt class="ecl-description-list__term">Description</dt>

        <dd class="ecl-description-list__definition">
          <!-- eslint-disable-next-line vue/no-v-html -->
          <span v-html="currentChartGroup.description" />
        </dd>

        <dt class="ecl-description-list__term">Identifier</dt>
        <dd class="ecl-description-list__definition">
          {{ currentChartGroup.code }}
        </dd>

        <dt class="ecl-description-list__term">License</dt>
        <dd class="ecl-description-list__definition">
          <!-- eslint-disable-next-line vue/no-v-html -->
          <span v-html="currentChartGroup.license" />
        </dd>
      </dl>
    </div>

    <h4>Dimensions</h4>

    <table class="ecl-table ecl-table--zebra ecl-u-break-word">
      <thead class="ecl-table__head">
        <tr class="ecl-table__row">
          <th class="ecl-table__header">Notation</th>
          <th class="ecl-table__header">Label</th>
          <th class="ecl-table__header">Comment</th>
        </tr>
      </thead>
      <tbody class="ecl-table__body">
        <tr
          v-for="{ notation, label, endpoint } in dimensions"
          :key="notation"
          class="ecl-table__row"
        >
          <td class="ecl-table__cell" data-ecl-table-header="Notation">
            {{ notation }}
          </td>
          <td class="ecl-table__cell" data-ecl-table-header="Label">
            {{ label ?? currentChartGroup[notation + "_label"] }}
          </td>
          <td class="ecl-table__cell" data-ecl-table-header="Comment">
            <span>Values from</span>
            <span>&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/${endpoint}/?chart_group=${currentChartGroup.code}&format=csv`"
              download-class
              label="codelist"
            />
          </td>
        </tr>
        <tr class="ecl-table__row">
          <td class="ecl-table__cell" data-ecl-table-header="Notation">
            flags
          </td>
          <td class="ecl-table__cell" data-ecl-table-header="Label">Flags</td>
          <td class="ecl-table__cell" data-ecl-table-header="Comment">
            <span>Values from</span>
            <span>&nbsp;</span>
            <ecl-link
              to="https://ec.europa.eu/eurostat/data/database/information"
              label="Eurostat"
              no-visited
            />
          </td>
        </tr>
      </tbody>
    </table>

    <h4>Download Data</h4>

    <ul>
      <li>
        <ecl-link
          :to="exportLink"
          no-visited
          label="Export CSV"
          download-class
        />
      </li>
      <li>
        <ecl-link :to="redocLink" no-visited label="API documentation" />
      </li>
    </ul>
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
  data() {
    return {
      apiURL,
    };
  },
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroup"]),
    dimensions() {
      return [
        {
          notation: "indicator",
          endpoint: "indicators",
        },
        {
          notation: "breakdown",
          endpoint: "breakdowns",
        },
        {
          notation: "unit",
          endpoint: "units",
        },
        {
          notation: "country",
          endpoint: "countries",
          label: "Country",
        },
        {
          notation: "period",
          endpoint: "periods",
        },
        // {
        //   notation: "indicator_group",
        //   endpoint: "indicator-groups",
        // },
        // {
        //   notation: "breakdown_group",
        //   endpoint: "breakdown-groups",
        // },
        {
          notation: "data_sources",
          endpoint: "data-sources",
          label: "Data Sources",
        },
      ];
    },
    datasetRoute() {
      return {
        name: "chart-group",
        chartGroupCode: this.currentChartGroup.code,
      };
    },
    datasetLink() {
      return new URL(
        this.$router.resolve(this.datasetRoute).fullPath,
        window.location
      ).href;
    },
    exportLink() {
      return `${apiURL}/chart-groups/${this.currentChartGroup.code}/facts/`;
    },
    redocLink() {
      return `${apiURL}/schema/redoc/`;
    },
  },
};
</script>

<style scoped>
table {
  table-layout: fixed;
}

th:nth-of-type(3) {
  width: 40%;
}
</style>
