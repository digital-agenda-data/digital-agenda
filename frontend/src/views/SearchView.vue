<template>
  <ecl-search-form
    class="ecl-u-mt-l"
    placeholder="search for indicators"
    :model-value="searchQuery"
  />
  <div v-if="apiData" class="ecl-u-mt-2xl">
    <table
      class="ecl-table ecl-table--zebra ecl-u-break-word ecl-u-position-relative"
    >
      <ecl-spinner v-if="loading" centered absolute />

      <thead class="ecl-table__head">
        <tr class="ecl-table__row">
          <th class="ecl-table__header">Indicator</th>
          <th class="ecl-table__header">Dataset</th>
        </tr>
      </thead>

      <tbody class="ecl-table__body">
        <tr v-for="item in items" :key="item.id" class="ecl-table__row">
          <td class="ecl-table__cell" data-ecl-table-header="Indicator">
            <div>
              <ecl-link :to="item.to" no-visited>
                <!-- eslint-disable-next-line vue/no-v-html -->
                <span v-html="item.label" />
                <!-- eslint-disable-next-line vue/no-v-html -->
                (<span v-html="item.code" />)
              </ecl-link>
              <!-- eslint-disable-next-line vue/no-v-html -->
              <div class="ecl-u-mt-2xs" v-html="item.definition" />
            </div>
          </td>
          <td
            class="ecl-table__cell dataset-cell"
            data-ecl-table-header="Dataset"
          >
            <ecl-link
              :to="item.toGroup"
              :label="item.chartGroup.name"
              no-visited
            />
          </td>
        </tr>
        <tr v-if="items.length === 0">
          <td colspan="2" class="ecl-table__cell">
            No indicators found for "{{ searchQuery }}".
          </td>
        </tr>
      </tbody>
    </table>
    <ecl-pagination :page-size="pageSize" :total="apiData.count" />
  </div>
</template>

<script>
import EclSearchForm from "@/components/ecl/forms/EclSearchForm.vue";
import { ref } from "vue";
import { mapState } from "pinia";
import { useRouteParams, useRouteQuery } from "@vueuse/router";
import { computedAsync } from "@vueuse/core";

import { api } from "@/lib/api";

import { useChartGroupStore } from "@/stores/chartGroupStore";
import { useChartStore } from "@/stores/chartStore";

import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclPagination from "@/components/ecl/navigation/EclPagination.vue";

export default {
  name: "SearchView",
  components: { EclSearchForm, EclPagination, EclLink, EclSpinner },
  data() {
    return {
      loading: ref(false),
      page: useRouteParams("page"),
      pageSize: 10,
      searchQuery: useRouteQuery("q"),
      apiData: computedAsync(this.getItems, null, {
        lazy: true,
        evaluating: this.loading,
      }),
    };
  },
  computed: {
    ...mapState(useChartGroupStore, ["chartGroupByCode"]),
    ...mapState(useChartStore, ["defaultChartForGroup"]),
    items() {
      return (this.apiData?.results ?? []).map((item) => {
        const chart = this.defaultChartForGroup[item.chart_group];
        const chartGroup = this.chartGroupByCode.get(item.chart_group);

        return {
          id: [item.code, item.group, item.chart_group].join("-"),
          chartGroup,
          code: item.highlight?.code || item.code,
          label: item.highlight?.label || item.label,
          definition: item.highlight?.definition || item.definition,
          to: {
            name: "chart-view",
            params: {
              chartCode: chart.code,
              chartGroupCode: chartGroup.code,
            },
            query: {
              indicator: item.code,
              indicatorGroup: item.group,
              // Specify filters from the sample fact to ensure the link
              // works even when the order of the filters are changed around
              breakdown: item.sample_fact.breakdown,
              period: item.sample_fact.period,
              unit: item.sample_fact.unit,
            },
          },
          toGroup: {
            name: "indicators",
            params: {
              chartGroupCode: chartGroup.code,
            },
          },
        };
      });
    },
  },
  methods: {
    async getItems(onCancel) {
      const abortController = new AbortController();
      const pageNr = parseInt(this.page || "1");

      onCancel(() => abortController.abort());

      return (
        await api.get("/chart-groups-indicator-search/", {
          signal: abortController.signal,
          params: {
            search: this.searchQuery,
            limit: this.pageSize,
            offset: (pageNr - 1) * this.pageSize,
          },
        })
      ).data;
    },
  },
};
</script>

<style scoped>
@media screen and (min-width: 996px) {
  .dataset-cell {
    width: 25%;
  }
}
</style>
