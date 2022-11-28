<script>
import BaseChart from "@/components/charts/BaseChart.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";

export default {
  name: "SplineCompareCountries",
  extends: BaseChart,
  computed: {
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
        CountryFilter,
      ];
    },
    endpointFilters() {
      return ["breakdown", "indicator", "unit"];
    },
    groupBy() {
      return ["country", "period"];
    },
    periods() {
      return Array.from(
        new Set(this.apiData.map((item) => item.period))
      ).sort();
    },
    lastPeriod() {
      return parseInt(this.periods.slice(-1)[0]);
    },
    series() {
      return this.countries.map((country) => {
        return {
          name: country.alt_label || country.label || country.code,
          color: country.color,
          data: this.periods.map((periodCode) => {
            return {
              y: this.apiValuesGrouped[country.code][periodCode] || 0,
              x: parseInt(periodCode),
              name: periodCode,
            };
          }),
        };
      });
    },
    chartOptions() {
      const parent = this;
      return {
        chart: {
          type: "spline",
        },
        series: this.series,
        xAxis: {
          allowDecimals: false,
          title: {
            text: "Period",
            enabled: false,
          },
        },
        plotOptions: {
          series: {
            dataLabels: {
              // Add data label to the last entry
              enabled: true,
              formatter() {
                return this.x === parent.lastPeriod ? this.series.name : null;
              },
            },
          },
        },
      };
    },
  },
};
</script>
