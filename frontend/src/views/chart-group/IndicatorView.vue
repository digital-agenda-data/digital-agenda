<template>
  <chart-group-nav>
    <!-- eslint-disable-next-line vue/no-v-html -->
    <div v-html="currentChartGroup.description" />
    <p>
      The following table provides methodological information about the source,
      the scope and the definition of each indicator. For more details, click on
      the links in the table or explore the whole database.
    </p>
    <ul class="ecl-u-mb-l">
      <li v-for="group in indicatorGroupsFiltered" :key="group.code">
        <ecl-link :to="`#${group.code}`" :label="group.label" no-visited />
      </li>
    </ul>
  </chart-group-nav>

  <ecl-spinner v-if="!loaded" size="large" class="ecl-u-ma-2xl" centered />
  <table
    v-else-if="indicatorGroupsFiltered.length > 0"
    class="ecl-table ecl-table--zebra ecl-u-break-word"
  >
    <thead class="ecl-table__head">
      <tr class="ecl-table__row">
        <th class="ecl-table__header">Indicator</th>
        <th class="ecl-table__header">Information</th>
      </tr>
    </thead>
    <template v-for="group in indicatorGroupsFiltered" :key="group.code">
      <thead class="ecl-table__head">
        <tr :id="group.code" class="ecl-table__row">
          <th class="ecl-table__header">
            {{ group.label }}
          </th>
          <th>
            <span>Export:&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/indicator-groups/${group.code}/facts/`"
              no-visited
              download-class
              label="data"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/indicators/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              label="indicators"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/data-sources/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              label="data sources"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/countries/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              label="countries"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/breakdowns/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              label="breakdowns"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/units/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              label="units"
            />
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
            <ecl-link
              :to="getChartLink(group, indicator)"
              :label="indicator.label"
              no-visited
            />
          </td>
          <td class="ecl-table__cell" data-ecl-table-header="Information">
            <div>
              <div class="ecl-u-type-paragraph-m">
                <strong>Notation:&nbsp;</strong>
                <span>{{ indicator.code }}</span>
              </div>

              <div v-if="indicator.definition" class="ecl-u-type-paragraph-m">
                <strong>Definition:&nbsp;</strong>
                <!-- eslint-disable-next-line vue/no-v-html -->
                <span v-html="indicator.definition" />
              </div>

              <div v-if="indicator.note" class="ecl-u-type-paragraph-m">
                <strong>Notes:&nbsp;</strong>
                <!-- eslint-disable-next-line vue/no-v-html -->
                <span v-html="indicator.note" />
              </div>

              <div class="ecl-u-type-paragraph-m">
                <strong>Time coverage:&nbsp;</strong>
                <span v-if="indicator.time_coverage">
                  {{ indicator.time_coverage }}
                </span>
              </div>

              <div
                v-for="data_source in indicator.data_sources"
                :key="indicator.code + data_source"
                class="ecl-u-type-paragraph-m"
              >
                <strong>Source:&nbsp;</strong>
                <ecl-link
                  v-if="dataSourceByCode.get(data_source)?.url"
                  :to="dataSourceByCode.get(data_source)?.url"
                  :label="dataSourceByCode.get(data_source)?.label"
                  no-visited
                />
                <span v-else>
                  {{ dataSourceByCode.get(data_source)?.label }}
                </span>
              </div>

              <div class="ecl-u-type-paragraph-m">
                <strong>Export:&nbsp;</strong>
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
              </div>
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
import { api, apiURL } from "@/lib/api";
import { groupByUnique, scrollToHash } from "@/lib/utils";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useChartStore } from "@/stores/chartStore";
import { useDataSourceStore } from "@/stores/dataSourceStore";
import { mapState } from "pinia";

export default {
  name: "IndicatorView",
  components: { ChartGroupNav, EclLink, EclSpinner },
  data() {
    return {
      apiURL,
      loaded: false,
      indicatorGroups: [],
      indicators: [],
    };
  },
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroup"]),
    ...mapState(useChartStore, ["defaultChartForCurrentGroup"]),
    ...mapState(useDataSourceStore, ["dataSourceByCode"]),
    indicatorsByCode() {
      return groupByUnique(this.indicators);
    },
    indicatorGroupsFiltered() {
      return this.indicatorGroups
        .map((group) => {
          return {
            ...group,
            indicators: group.members
              .map((indicatorCode) => this.indicatorsByCode.get(indicatorCode))
              .filter((i) => !!i),
          };
        })
        .filter((group) => group.indicators.length > 0);
    },
  },
  mounted() {
    this.loadData();
  },
  methods: {
    getChartLink(group, indicator) {
      return {
        name: "chart-view",
        params: {
          chartCode: this.defaultChartForCurrentGroup.code,
          chartGroupCode: this.currentChartGroup.code,
        },
        query: {
          indicator: indicator.code,
          indicatorGroup: group.code,
        },
      };
    },
    async loadData() {
      try {
        this.loaded = false;
        await Promise.all([this.loadIndicatorGroups(), this.loadIndicators()]);
      } finally {
        this.loaded = true;
      }
      this.$nextTick(scrollToHash);
    },
    async loadIndicatorGroups() {
      this.indicatorGroups = (
        await api.get(`/indicator-groups/`, {
          params: {
            chart_group: this.currentChartGroup.code,
          },
        })
      ).data;
    },
    async loadIndicators() {
      this.indicators = (
        await api.get(
          `/chart-groups/${this.currentChartGroup.code}/indicators/`,
        )
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

[data-ecl-table-header="Information"] div + div {
  margin-top: 0.25rem;
}
</style>
