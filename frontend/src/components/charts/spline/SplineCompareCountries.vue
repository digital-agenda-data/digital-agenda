<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import CountryMultiFilter from "@/components/chart-filters/CountryMultiFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import IndicatorFilter from "@/components/chart-filters/IndicatorFilter.vue";
import IndicatorGroupFilter from "@/components/chart-filters/IndicatorGroupFilter.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";

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
            const fact = this.apiDataGrouped[country.code][periodCode];

            return {
              fact,
              y: fact?.value || null,
              x: parseInt(periodCode),
              name: periodCode,
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        yAxis: {
          min: 0,
        },
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
