<script>
import BaseMultiAxisChart from "@/components/charts/base/BaseMultiAxisChart.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import EclHeading from "@/components/ecl/EclHeading.vue";
import { api } from "@/lib/api";

export default {
  name: "ScatterCompareTwoIndicators",
  extends: BaseMultiAxisChart,
  computed: {
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
    chartType() {
      return "scatter";
    },
    chartSubtitle() {
      return "";
    },
    chartOptions() {
      return {
        chart: {
          type: this.chartType,
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
