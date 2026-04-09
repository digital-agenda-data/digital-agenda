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
  <ecl-table
    v-else-if="indicatorGroupsFiltered.length > 0"
    class="ecl-u-break-word"
    zebra
  >
    <ecl-thead>
      <ecl-tr>
        <ecl-th>Indicator</ecl-th>
        <ecl-th>Information</ecl-th>
      </ecl-tr>
    </ecl-thead>
    <template v-for="group in indicatorGroupsFiltered" :key="group.code">
      <ecl-thead>
        <ecl-tr :id="group.code">
          <ecl-th>
            {{ group.label }}
          </ecl-th>
          <ecl-th>
            <span>Export:&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/indicator-groups/${group.code}/facts/`"
              no-visited
              download-class
              variant="none"
              label="data"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/indicators/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              variant="none"
              label="indicators"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/data-sources/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              variant="none"
              label="data sources"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/countries/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              variant="none"
              label="countries"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/breakdowns/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              variant="none"
              label="breakdowns"
            />
            <span>,&nbsp;</span>
            <ecl-link
              :to="`${apiURL}/units/?indicator_group=${group.code}&format=csv`"
              no-visited
              download-class
              variant="none"
              label="units"
            />
          </ecl-th>
        </ecl-tr>
      </ecl-thead>
      <ecl-tbody>
        <ecl-tr v-for="indicator in group.indicators" :key="indicator.code">
          <ecl-td class="label-cell" header="Indicator">
            <ecl-link
              :to="getChartLink(group, indicator)"
              :label="indicator.label"
              no-visited
            />
          </ecl-td>
          <ecl-td header="Information">
            <div>
              <div class="ecl-u-type-paragraph-m">
                <strong>Notation:&nbsp;</strong>
                <span>{{ indicator.code }}</span>
              </div>

              <dimension-prop
                :value="indicator.definition"
                label="Definition:"
                class="ecl-u-type-paragraph-m"
              />
              <dimension-prop
                :value="indicator.note"
                label="Notes:"
                class="ecl-u-type-paragraph-m"
              />

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
          </ecl-td>
        </ecl-tr>
      </ecl-tbody>
    </template>
  </ecl-table>
  <p v-else>No indicators found</p>
</template>

<script>
import ChartGroupNav from "@/components/ChartGroupNav.vue";
import DimensionProp from "@/components/charts/DimensionProp.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclTable from "@/components/ecl/table/EclTable.vue";
import EclTbody from "@/components/ecl/table/EclTbody.vue";
import EclTd from "@/components/ecl/table/EclTd.vue";
import EclTh from "@/components/ecl/table/EclTh.vue";
import EclThead from "@/components/ecl/table/EclThead.vue";
import EclTr from "@/components/ecl/table/EclTr.vue";
import { api, apiURL } from "@/lib/api";
import { groupByUnique, scrollToHash } from "@/lib/utils";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useChartStore } from "@/stores/chartStore";
import { useDataSourceStore } from "@/stores/dataSourceStore";
import { mapState } from "pinia";

export default {
  name: "IndicatorView",
  components: {
    EclTd,
    EclTbody,
    EclTr,
    EclTh,
    EclThead,
    EclTable,
    DimensionProp,
    ChartGroupNav,
    EclLink,
    EclSpinner,
  },
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
          // Specify the time period from the sample fact to ensure the link
          // works even when the indicator filter comes after the period
          period: indicator.sample_fact.period,
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
