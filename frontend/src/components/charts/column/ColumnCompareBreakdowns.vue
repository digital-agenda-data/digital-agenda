<script>
import BaseChart from "@/components/charts/BaseChart.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import { apiCall } from "@/lib/api";
import { colorForCountry } from "@/lib/utils";

export default {
  name: "ColumnCompareBreakdowns",
  extends: BaseChart,
  data() {
    return {
      breakdownList: [],
    };
  },
  computed: {
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownGroupFilter,
        PeriodFilter,
        UnitFilter,
        CountryFilter,
      ];
    },
    endpointFilters() {
      return ["breakdownGroup", "period", "indicator", "unit"];
    },
    groupBy() {
      return ["breakdown", "country"];
    },
    apiDataBreakdowns() {
      const codes = new Set(this.apiData.map((item) => item.breakdown));
      // Preserve the order from the API
      return this.breakdownList.filter((item) => codes.has(item.code));
    },
    series() {
      return this.apiDataBreakdowns.map((breakdown, seriesIndex) => {
        return {
          name: breakdown.alt_label || breakdown.label,
          data: this.countries.map((country) => {
            return {
              name: country.alt_label || country.label || country.code,
              y: this.apiValuesGrouped[breakdown.code][country.code] || 0,
              color: colorForCountry(country.code, seriesIndex),
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        chart: {
          type: "column",
        },
        series: this.series,
        legend: {
          enabled: this.apiDataBreakdowns.length > 1,
        },
        xAxis: {
          type: "category",
          title: {
            text: "Country",
            enabled: false,
          },
        },
      };
    },
    defineEntries() {
      // Set the breakdowns to define them in the "Definitions and scopes"
      return {
        Indicator: this.indicator,
        Breakdown: this.apiDataBreakdowns,
        Unit: this.unit,
      };
    },
  },
  methods: {
    async loadExtra() {
      if (!this.breakdownGroup) return;

      this.breakdownList = await apiCall(
        "GET",
        `/breakdown-groups/${this.breakdownGroup.code}/breakdowns/`
      );
    },
  },
};
</script>
