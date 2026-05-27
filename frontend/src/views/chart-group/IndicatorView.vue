<template>
  <chart-group-nav>
    <!-- eslint-disable-next-line vue/no-v-html -->
    <div v-html="currentChartGroup.description" />
  </chart-group-nav>
  <div class="ecl-form-group ecl-u-align-items-center ecl-u-mb-8xl">
    <input
      v-model="searchQuery"
      autofocus
      type="search"
      class="ecl-text-input ecl-text-input--m ecl-u-width-100"
      placeholder="Search for indicators"
      aria-label="Search"
    />
  </div>
  <ecl-spinner v-if="!loaded" size="large" class="ecl-u-ma-2xl" centered />
  <div v-else-if="indicatorGroupsFiltered.length > 0">
    <div
      v-for="(parent, parentCode) in indicatorParents"
      :key="parentCode"
      class="rainbow-table"
    >
      <indicator-table :parent="parent" />
    </div>
    <div v-for="(parent, parentCode) in indicatorParents" :key="parentCode">
      <indicator-details :parent="parent" />
    </div>
  </div>
  <p v-else>No indicators found</p>
</template>

<script>
import ChartGroupNav from "@/components/ChartGroupNav.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import IndicatorDetails from "@/components/IndicatorDetails.vue";
import IndicatorTable from "@/components/IndicatorTable.vue";
import { api } from "@/lib/api";
import { groupByUnique, scrollToHash } from "@/lib/utils.js";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useRouteQuery } from "@vueuse/router";
import { mapState } from "pinia";

export default {
  name: "IndicatorView",
  components: {
    IndicatorDetails,
    IndicatorTable,
    ChartGroupNav,
    EclSpinner,
  },
  data() {
    return {
      loaded: false,
      indicatorGroups: [],
      indicators: [],
      searchQuery: useRouteQuery("q"),
    };
  },
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroup"]),
    indicatorsByCode() {
      return groupByUnique(this.indicators);
    },
    indicatorGroupsFiltered() {
      const searchValue = this.searchQuery?.toLocaleLowerCase() ?? "";
      return this.indicatorGroups
        .map((group) => {
          return {
            ...group,
            indicators: group.members
              .map((indicatorCode) => this.indicatorsByCode.get(indicatorCode))
              .filter((i) => !!i)
              .filter(
                (i) =>
                  searchValue === "" ||
                  group.code.toLocaleLowerCase().includes(searchValue) ||
                  group.label.toLocaleLowerCase().includes(searchValue) ||
                  group.alt_label.toLocaleLowerCase().includes(searchValue) ||
                  i.code.toLocaleLowerCase().includes(searchValue) ||
                  i.label.toLocaleLowerCase().includes(searchValue) ||
                  i.alt_label.toLocaleLowerCase().includes(searchValue),
              ),
          };
        })
        .filter((group) => group.indicators.length > 0);
    },
    indicatorParents() {
      const result = {};
      for (const group of this.indicatorGroupsFiltered) {
        const parent = group.parent ?? {
          code: "",
          label: "",
          icon: "",
          colors: [],
        };
        result[parent.code] ??= { ...parent, members: [] };
        result[parent.code].members.push(group);
      }
      return result;
    },
  },
  mounted() {
    this.loadData();
  },
  methods: {
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
