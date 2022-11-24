<script>
import BaseChart from "@/components/charts/BaseChart.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import { apiCall } from "@/lib/api";
import { useFilterStore } from "@/stores/filterStore";

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
    endpoint() {
      return "/facts/facts-per-country/";
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
      return this.apiDataBreakdowns.map((breakdown) => {
        return {
          name: breakdown.alt_label || breakdown.label,
          data: this.countries.map(
            (country) =>
              this.apiValuesGrouped[breakdown.code][country.code] || 0
          ),
        };
      });
    },
    chartOptions() {
      const parent = this;
      return {
        chart: {
          type: "column",
        },
        series: this.series,
        title: {
          text: this.indicator?.label,
        },
        subtitle: {
          text: this.period && `Year: ${this.period.code}`,
        },
        xAxis: {
          categories: this.countries.map(
            (country) => country.alt_label || country.label || country.code
          ),
          title: {
            text: "Country",
            enabled: false,
          },
        },
        yAxis: {
          title: {
            text: this.unit?.alt_label,
          },
        },
        tooltip: {
          formatter() {
            return [
              `<b>${this.x}</b>`,
              `${this.y}${parent.unit.alt_label}`,
              `<b>Breakdown:</b> ${this.series.name}`,
              `<b>Time Period:</b> Year: ${parent.period.code}`,
            ].join("<br/>");
          },
        },
      };
    },
  },
  watch: {
    apiDataBreakdowns() {
      // Set the breakdowns to define them in the "Definitions and scopes"
      useFilterStore().breakdown = this.apiDataBreakdowns;
    },
  },
  methods: {
    async loadExtra() {
      if (!this.breakdownGroup) return;

      this.breakdownList = await apiCall(
        "GET",
        `/breakdown-groups/${this.breakdownGroup.code}/breakdowns`
      );
    },
  },
};
</script>
