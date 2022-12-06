<script>
import BaseMultiAxisChart from "@/components/charts/base/BaseMultiAxisChart.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import CountryFilter from "@/components/filters/CountryFilter.vue";

export default {
  name: "SplineCompareTwoIndicators",
  extends: BaseMultiAxisChart,
  computed: {
    showAxisLabels() {
      return false;
    },
    filterXComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
        CountryFilter,
      ];
    },
    filterYComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
      ];
    },
    endpointFilters() {
      return {
        X: ["indicatorX", "breakdownX", "unitX", "countryX"],
        Y: ["indicatorY", "breakdownY", "unitY", "countryX"],
      };
    },
    groupBy() {
      return ["axis", "period"];
    },
    series() {
      return ["X", "Y"].map((axis, index) => {
        const unit = this.filterStore[axis].unit;
        const breakdown = this.filterStore[axis].breakdown;
        const indicator = this.filterStore[axis].indicator;

        return {
          yAxis: index,
          name: this.getDisplay(indicator),
          data: this.apiDataPeriods.map((periodCode) => {
            const apiValue =
              this.apiValuesGrouped[axis] &&
              this.apiValuesGrouped[axis][periodCode];

            return {
              y: apiValue,
              x: parseInt(periodCode),
              name: periodCode,
              unit,
              breakdown,
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        chart: {
          type: "spline",
        },
        title: {
          text:
            this.makeTitle([
              this.filterStore.indicatorX,
              this.filterStore.breakdownX,
            ]) +
            " and " +
            this.makeTitle([
              this.filterStore.indicatorY,
              this.filterStore.breakdownY,
            ]),
        },
        subtitle: {
          text: this.getDisplay(this.filterStore.countryX),
        },
        legend: {
          enabled: true,
        },
        plotOptions: {
          series: {
            connectNulls: true,
            dataLabels: {
              enabled: false,
            },
          },
        },
        yAxis: [
          {
            title: {
              text: this.getDisplay(this.filterStore.unitX),
            },
          },
          {
            // lineWidth: 1,
            opposite: true,
            title: {
              text: this.getDisplay(this.filterStore.unitY),
            },
          },
        ],
      };
    },
    tooltip() {
      const parent = this;
      return {
        formatter() {
          return [
            `<b>${this.series.name}</b>`,
            parent.getUnitDisplay(this.point.y, this.point.options.unit),
            `<b>Breakdown:</b> ${parent.getDisplay(
              this.point.options.breakdown
            )}`,
            `<b>Time Period:</b> Year: ${this.point.x}`,
          ].join("<br/>");
        },
      };
    },
  },
};
</script>