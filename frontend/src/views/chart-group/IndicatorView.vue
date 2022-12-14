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
          v-for="indicator in group.indicators"
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

              <p v-if="indicator.periods.length > 0">
                <strong>Time coverage:&nbsp;</strong>
                <span>
                  {{ indicator.periods[0] }} -
                  {{ indicator.periods.slice(-1)[0] }}
                </span>
              </p>

              <p v-if="indicator.data_source">
                <strong>Source:&nbsp;</strong>
                <ecl-link
                  v-if="dataSources[indicator.data_source]?.url"
                  :to="dataSources[indicator.data_source]?.url"
                  :label="dataSources[indicator.data_source]?.label"
                  no-visited
                />
                <span v-else>
                  {{ dataSources[indicator.data_source]?.label }}
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
import { mapState } from "pinia";
import { api } from "@/lib/api";
import { scrollToHash } from "@/lib/utils";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import ChartGroupNav from "@/components/ChartGroupNav.vue";

export default {
  name: "IndicatorView",
  components: { ChartGroupNav, EclLink, EclSpinner },
  data() {
    return {
      loaded: false,
      chartGroupDetails: null,
      dataSources: {},
    };
  },
  computed: {
    ...mapState(useChartGroupStore, [
      "currentChartGroup",
      "currentChartGroupCode",
    ]),
    indicatorGroups() {
      return this.chartGroupDetails?.indicator_groups || [];
    },
    indicatorGroupsFiltered() {
      const allowedPeriods = new Set(
        this.chartGroupDetails.periods.map((period) => period.code)
      );

      return this.indicatorGroups
        .map((group) => {
          return {
            ...group,
            indicators: group.indicators.filter(
              (indicator) =>
                allowedPeriods.size === 0 ||
                indicator.periods.some((period) => allowedPeriods.has(period))
            ),
          };
        })
        .filter((group) => group.indicators.length > 0);
    },
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.loaded = false;
        await Promise.all([this.loadChartGroup(), this.loadDataSources()]);
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
    async loadDataSources() {
      const result = {};
      const response = (await api.get("/data-sources/")).data;
      for (const dataSource of response) {
        result[dataSource.code] = dataSource;
      }

      this.dataSources = result;
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
