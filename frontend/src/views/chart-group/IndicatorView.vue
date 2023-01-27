<template>
  <chart-group-nav>
    <div v-html="currentChartGroup.description" />
    <p>
      The following table provides methodological information about the source,
      the scope and the definition of each indicator. For more details, click on
      the links in the table or explore the whole database.
    </p>
    <ul v-if="chartGroupDetails" class="ecl-u-mb-l">
      <li v-for="group in indicatorGroups" :key="group.code">
        <ecl-link :to="`#${group.code}`" :label="group.label" no-visited />
      </li>
    </ul>
  </chart-group-nav>

  <ecl-spinner v-if="!loaded" size="large" class="ecl-u-ma-2xl" centered />
  <table
    v-else-if="indicatorGroups.length > 0"
    class="ecl-table ecl-table--zebra ecl-u-break-word"
  >
    <thead class="ecl-table__head">
      <tr class="ecl-table__row">
        <th class="ecl-table__header">Indicator</th>
        <th class="ecl-table__header">Information</th>
      </tr>
    </thead>
    <template v-for="group in indicatorGroups" :key="group.code">
      <thead class="ecl-table__head">
        <tr :id="group.code" class="ecl-table__row">
          <th colspan="2" class="ecl-table__header">
            {{ group.label }}
          </th>
        </tr>
      </thead>
      <tbody class="ecl-table__body">
        <tr
          v-for="indicator in indicatorsForGroup(group)"
          :key="indicator.code"
          class="ecl-table__row"
        >
          <td
            class="ecl-table__cell label-cell"
            data-ecl-table-header="Indicator"
          >
            {{ indicator.label }}
          </td>
          <td class="ecl-table__cell" data-ecl-table-header="Information">
            <div>
              <p>
                <strong>Notation:&nbsp;</strong>
                <span>{{ indicator.code }}</span>
              </p>

              <p v-if="indicator.definition">
                <strong>Definition:&nbsp;</strong>
                <span v-html="indicator.definition" />
              </p>

              <p>
                <strong>Time coverage:&nbsp;</strong>
                <span>
                  {{ indicator.min_period }} -
                  {{ indicator.max_period }}
                </span>
              </p>

              <p v-if="indicator.data_source">
                <strong>Source:&nbsp;</strong>
                <ecl-link
                  v-if="dataSourceByCode.get(indicator.data_source)?.url"
                  :to="dataSourceByCode.get(indicator.data_source)?.url"
                  :label="dataSourceByCode.get(indicator.data_source)?.label"
                  no-visited
                />
                <span v-else>
                  {{ dataSourceByCode.get(indicator.data_source)?.label }}
                </span>
              </p>
            </div>
          </td>
        </tr>
      </tbody>
    </template>
  </table>
  <p v-else>No indicators found</p>
</template>

<script>
import ChartGroupNav from "@/components/ChartGroupNav.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { api } from "@/lib/api";
import { groupByUnique, scrollToHash } from "@/lib/utils";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useDataSourceStore } from "@/stores/dataSourceStore";
import { mapState } from "pinia";

export default {
  name: "IndicatorView",
  components: { ChartGroupNav, EclLink, EclSpinner },
  data() {
    return {
      loaded: false,
      chartGroupDetails: null,
      indicatorGroups: [],
      indicators: [],
    };
  },
  computed: {
    ...mapState(useChartGroupStore, [
      "currentChartGroup",
      "currentChartGroupCode",
    ]),
    ...mapState(useDataSourceStore, ["dataSourceByCode"]),
    indicatorsByCode() {
      return groupByUnique(this.indicators);
    },
  },
  mounted() {
    this.loadData();
  },
  methods: {
    indicatorsForGroup(group) {
      return group.indicators
        .map((indicatorCode) => this.indicatorsByCode.get(indicatorCode))
        .filter((i) => !!i);
    },
    async loadData() {
      try {
        this.loaded = false;
        await Promise.all([
          this.loadChartGroup(),
          this.loadIndicatorGroups(),
          this.loadIndicators(),
        ]);
      } finally {
        this.loaded = true;
      }
      this.$nextTick(scrollToHash);
    },
    async loadChartGroup() {
      this.chartGroupDetails = (
        await api.get(`/chart-groups/${this.currentChartGroupCode}/`)
      ).data;
    },
    async loadIndicatorGroups() {
      this.indicatorGroups = (
        await api.get(
          `/chart-groups/${this.currentChartGroupCode}/indicator-groups/`
        )
      ).data;
    },
    async loadIndicators() {
      this.indicators = (
        await api.get(`/chart-groups/${this.currentChartGroupCode}/indicators/`)
      ).data;
    },
  },
};
</script>

<style scoped>
@media screen and (min-width: 996px) {
  .label-cell {
    width: 33%;
  }
}
</style>
