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
    endpoint() {
      return "/facts/facts-per-country/";
    },
    endpointFilters() {
      return ["breakdown", "period", "indicator", "unit"];
    },
    groupBy() {
      return ["country"];
    },
    chartOptions() {
      return {
        chart: {
          type: "column",
        },
        series: [
          {
            colorKey: "colorValue",
            name: this.breakdown.alt_label || this.breakdown.label,
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
        ],
        legend: {
          enabled: false,
        },
        title: {
          text: [this.indicator?.label, this.breakdown?.label]
            .map((s) => s?.trim())
            .join(", "),
        },
        subtitle: {
          text: this.period && `Year: ${this.period.code}`,
        },
        xAxis: {
          type: "category",
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
        tooltip: this.defaultTooltip,
      };
    },
  },
};
</script>
