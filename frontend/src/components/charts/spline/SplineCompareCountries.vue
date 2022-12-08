<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import CountryMultiFilter from "@/components/filters/CountryMultiFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";

export default {
  name: "SplineCompareCountries",
  extends: BaseChart,
  computed: {
    chartType() {
      return "spline";
    },
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
        CountryMultiFilter,
      ];
    },
    endpointFilters() {
      return ["breakdown", "indicator", "unit"];
    },
    groupBy() {
      return ["country", "period"];
    },
    series() {
      return this.countries.map((country) => {
        return {
          name: this.getDisplay(country),
          color: country.color,
          data: this.apiDataPeriods.map((periodCode) => {
            return {
              y: this.apiValuesGrouped[country.code][periodCode] || null,
              x: parseInt(periodCode),
              name: periodCode,
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        plotOptions: {
          series: {
            connectNulls: true,
            dataLabels: {
              // Add data label to the last entry
              enabled: true,
              formatter() {
                const lastIndex = this.series.yData.findLastIndex(
                  (el) => el !== null
                );

                return this.point.index === lastIndex ? this.series.name : null;
              },
            },
          },
        },
      };
    },
  },
};
</script>
