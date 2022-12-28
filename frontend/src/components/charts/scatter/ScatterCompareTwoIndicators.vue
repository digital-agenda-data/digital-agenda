<script>
import BaseMultiAxisChart from "@/components/charts/base/BaseMultiAxisChart.vue";
import IndicatorGroupFilter from "@/components/chart-filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/chart-filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import EclHeading from "@/components/ecl/EclHeading.vue";

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
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
        PeriodFilter,
      ];
    },
    filterYComponents() {
      return [
        {
          key: "y-heading",
          component: EclHeading,
          attrs: { size: 5, text: "Vertical axis" },
        },
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
      ];
    },
    endpointFilters() {
      return {
        X: ["indicatorX", "breakdownX", "unitX", "periodX"],
        Y: ["indicatorY", "breakdownY", "unitY", "periodX"],
      };
    },
    groupBy() {
      return ["country", "axis"];
    },
    series() {
      return Object.keys(this.apiValuesGrouped).map((countryCode) => {
        return {
          name: this.getDisplay(this.countryByCode.get(countryCode)),
          color: this.countryByCode.get(countryCode)?.color,
          marker: {
            symbol: "circle",
          },
          data: [
            {
              name: countryCode,
              x: this.apiValuesGrouped[countryCode].X || 0,
              y: this.apiValuesGrouped[countryCode].Y || 0,
              z: this.apiValuesGrouped[countryCode].Z || 0,
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
                return this.point.name;
              },
            },
          },
        },
        title: {
          text:
            this.filterStore.periodX?.code &&
            `Year: ${this.filterStore.periodX.code}`,
        },
        subtitle: {
          enabled: !!this.chartSubtitle,
          text: this.chartSubtitle,
        },
        xAxis: {
          title: {
            text: this.makeTitle([
              this.filterStore.indicatorX,
              this.filterStore.breakdownX,
              this.filterStore.unitX,
            ]),
            enabled: true,
          },
        },
        yAxis: {
          title: {
            text: this.makeTitle([
              this.filterStore.indicatorY,
              this.filterStore.breakdownY,
              this.filterStore.unitY,
            ]),
            enabled: true,
          },
        },
      };
    },
  },
};
</script>
