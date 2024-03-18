<script>
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import BaseChart from "@/components/charts/base/BaseChart.vue";
import CountryMultiFilter from "@/components/chart-filters/CountryMultiFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import { getCountryLabel, getUnitLabel } from "@/lib/utils";
import { usePeriodStore } from "@/stores/periodStore";
import { mapState } from "pinia";

export default {
  name: "SplineCompareCountries",
  extends: BaseChart,
  computed: {
    ...mapState(usePeriodStore, ["periodByCode"]),
    chartType() {
      return "spline";
    },
    filterComponents() {
      return [
        IndicatorWithGroupsFilter,
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
          name: getCountryLabel(country),
          color: country.color,
          pointRange: 365 * 24 * 3600 * 1000,
          data: this.apiDataPeriods.map((periodCode) => {
            const fact = this.apiDataGrouped[country.code][periodCode];
            const period = this.periodByCode.get(periodCode);

            return {
              fact,
              y: fact?.value ?? null,
              x: new Date(period?.date),
              name: this.getPeriodWithExtraNotes(period),
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        xAxis: {
          type: "datetime",
        },
        yAxis: {
          min: 0,
          title: {
            text: getUnitLabel(this.unit),
          },
        },
        plotOptions: {
          series: {
            connectNulls: true,
            dataLabels: {
              // Add data label to the last entry
              enabled: true,
              formatter() {
                const lastIndex = this.series.yData.findLastIndex(
                  (el) => el !== null,
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
