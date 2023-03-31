<script>
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import BaseMultiAxisChart from "@/components/charts/base/BaseMultiAxisChart.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";

export default {
  name: "SplineCompareTwoIndicators",
  extends: BaseMultiAxisChart,
  computed: {
    chartType() {
      return "spline";
    },
    showAxisLabel() {
      return false;
    },
    filterXComponents() {
      return [
        IndicatorWithGroupsFilter,
        BreakdownWithGroupsFilter,
        UnitFilter,
        CountryFilter,
      ];
    },
    filterYComponents() {
      return [IndicatorWithGroupsFilter, BreakdownWithGroupsFilter, UnitFilter];
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
          name: indicator.display,
          data: this.apiDataPeriods.map((periodCode) => {
            const apiValue = this.apiValuesGrouped[axis]?.[periodCode];

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
          text: this.filterStore.countryX?.display,
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
              text: this.filterStore.unitX?.display,
            },
            min: 0,
          },
          {
            opposite: true,
            title: {
              text: this.filterStore.unitY?.display,
            },
            min: 0,
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
            `<b>Breakdown:</b> ${this.point.options.breakdown?.display}`,
            `<b>Time Period:</b> Year: ${this.point.x}`,
          ].join("<br/>");
        },
      };
    },
  },
};
</script>
