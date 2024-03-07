<script>
import CountryMultiFilter from "@/components/chart-filters/CountryMultiFilter.vue";
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import BaseMultiAxisChart from "@/components/charts/base/BaseMultiAxisChart.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import EclHeading from "@/components/ecl/EclHeading.vue";
import {
  getBreakdownLabel,
  getCountryLabel,
  getIndicatorLabel,
  getPeriodLabel,
  getUnitLabel,
} from "@/lib/utils";

export default {
  name: "ScatterCompareTwoIndicators",
  extends: BaseMultiAxisChart,
  computed: {
    chartType() {
      return "scatter";
    },
    filterXComponents() {
      return [
        {
          key: "x-heading",
          component: EclHeading,
          attrs: { size: 5, text: "Horizontal axis" },
        },
        IndicatorWithGroupsFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
        PeriodFilter,
        {
          component: CountryMultiFilter,
          attrs: { allInitial: true, hidden: true, syncRoute: false },
        },
      ];
    },
    filterYComponents() {
      return [
        {
          key: "y-heading",
          component: EclHeading,
          attrs: { size: 5, text: "Vertical axis" },
        },
        IndicatorWithGroupsFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
        PeriodFilter,
      ];
    },
    endpointFilters() {
      return {
        X: ["indicatorX", "breakdownX", "unitX", "periodX"],
        Y: ["indicatorY", "breakdownY", "unitY", "periodY"],
      };
    },
    groupBy() {
      return ["country", "axis"];
    },
    series() {
      return (this.filterStore.countryX ?? []).map((country) => {
        const name = `${getCountryLabel(country)} (${country.code})`;
        return {
          name,
          color: country?.color,
          marker: {
            symbol: "circle",
          },
          data: [
            {
              name,
              x: this.apiValuesGrouped[country.code]?.X || 0,
              y: this.apiValuesGrouped[country.code]?.Y || 0,
              z: this.apiValuesGrouped[country.code]?.Z || 0,
              code: country.code,
            },
          ],
        };
      });
    },
    chartSubtitle() {
      return "";
    },
    chartOptions() {
      return {
        chart: {
          type: this.chartType,
          zooming: {
            type: "xy",
          },
        },
        legend: {
          enabled: true,
        },
        plotOptions: {
          series: {
            dataLabels: {
              enabled: true,
              formatter() {
                return this.point.code;
              },
            },
          },
        },
        title: {
          text: "",
          enable: false,
        },
        subtitle: {
          enabled: !!this.chartSubtitle,
          text: this.chartSubtitle,
        },
        xAxis: {
          lineWidth: 1,
          gridLineWidth: 1,
          plotLines: this.getMidPlotLine("X"),
          title: {
            text: this.joinStrings([
              getIndicatorLabel(this.filterStore.indicatorX, "label"),
              getBreakdownLabel(this.filterStore.breakdownX, "label"),
              getUnitLabel(this.filterStore.unitX, "label"),
              getPeriodLabel(this.filterStore.periodX, "label"),
            ]),
            enabled: true,
          },
        },
        yAxis: {
          lineWidth: 1,
          gridLineWidth: 1,
          plotLines: this.getMidPlotLine("Y"),
          title: {
            text: this.joinStrings([
              getIndicatorLabel(this.filterStore.indicatorY, "label"),
              getBreakdownLabel(this.filterStore.breakdownY, "label"),
              getUnitLabel(this.filterStore.unitY, "label"),
              getPeriodLabel(this.filterStore.periodY, "label"),
            ]),
            enabled: true,
          },
        },
      };
    },
  },
  methods: {
    /**
     * Get the middle plot line for this axis
     *
     * @return {[{color: string, value: number}]}
     */
    getMidPlotLine(axis) {
      const values = this.apiData
        .filter((item) => item.axis === axis)
        .map((item) => item.value);
      const min = Math.min(...values);
      const max = Math.max(...values);

      return [
        {
          color: "#000000",
          value: (max - min) / 2 + min,
        },
      ];
    },
  },
};
</script>
