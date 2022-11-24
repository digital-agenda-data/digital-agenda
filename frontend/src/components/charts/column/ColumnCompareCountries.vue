<script>
import BaseChart from "@/components/charts/BaseChart.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";
import BreakdownFilter from "@/components/filters/BreakdownFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";

export default {
  name: "ColumnCompareCountries",
  extends: BaseChart,
  computed: {
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownGroupFilter,
        BreakdownFilter,
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
    chartOptions() {
      const parent = this;
      return {
        chart: {
          type: "column",
        },
        series: [
          {
            name: this.unit?.alt_label,
            data: this.chartDataFilteredByCountry,
          },
        ],
        legend: {
          enabled: false,
        },
        title: {
          text: [this.indicator?.label, this.breakdown?.label]
            .map((s) => s.trim())
            .join(", "),
        },
        subtitle: {
          text: this.period && `Year: ${this.period.code}`,
        },
        xAxis: {
          categories: this.categories,
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
              `<b>Time Period:</b> Year: ${parent.period.code}`,
            ].join("<br/>");
          },
        },
      };
    },
  },
};
</script>
