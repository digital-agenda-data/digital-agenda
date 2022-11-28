<script>
import BaseChart from "@/components/charts/BaseChart.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";
import { colorForCountry } from "@/lib/utils";

export default {
  name: "ColumnCompareCountries",
  extends: BaseChart,
  computed: {
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        PeriodFilter,
        UnitFilter,
        CountryFilter,
      ];
    },
    allInitialCountries() {
      return true;
    },
    endpointFilters() {
      return ["breakdown", "period", "indicator", "unit"];
    },
    groupBy() {
      return ["country"];
    },
    series() {
      return [
        {
          data: this.countries.map((country) => {
            return {
              y: this.apiValuesGrouped[country.code] || 0,
              name: country.alt_label || country.label || country.code,
              color: colorForCountry(country.code),
            };
          }),
          dataSorting: {
            enabled: true,
          },
        },
      ];
    },
    chartOptions() {
      return {
        chart: {
          type: "column",
        },
        series: this.series,
        xAxis: {
          type: "category",
          title: {
            text: "Country",
            enabled: false,
          },
        },
      };
    },
  },
};
</script>
