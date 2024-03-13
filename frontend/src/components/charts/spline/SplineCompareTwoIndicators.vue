<script>
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import BaseMultiAxisChart from "@/components/charts/base/BaseMultiAxisChart.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import {
  getBreakdownLabel,
  getCountryLabel,
  getIndicatorLabel,
  getMarkerSymbol,
  getUnitLabel,
} from "@/lib/utils";
import { usePeriodStore } from "@/stores/periodStore";
import { mapState } from "pinia";

export default {
  name: "SplineCompareTwoIndicators",
  extends: BaseMultiAxisChart,
  computed: {
    ...mapState(usePeriodStore, ["periodByCode"]),
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
          name: getIndicatorLabel(indicator),
          color:
            breakdown?.chart_options?.color ?? indicator?.chart_options?.color,
          dashStyle:
            breakdown?.chart_options?.dash_style ??
            indicator?.chart_options?.dash_style,
          marker: {
            symbol: getMarkerSymbol([
              breakdown?.chart_options,
              indicator?.chart_options,
            ]),
          },
          pointRange: 365 * 24 * 3600 * 1000,
          data: this.apiDataPeriods.map((periodCode) => {
            const apiValue = this.apiValuesGrouped[axis]?.[periodCode];
            const period = this.periodByCode.get(periodCode);

            return {
              y: apiValue,
              x: new Date(period?.date),
              name: this.getPeriodWithExtraNotes(period, indicator),
              unit,
              period,
              indicator,
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
            this.joinStrings([
              getIndicatorLabel(this.filterStore.indicatorX, "label"),
              getBreakdownLabel(this.filterStore.breakdownX, "label"),
            ]) +
            " and " +
            this.joinStrings([
              getIndicatorLabel(this.filterStore.indicatorY, "label"),
              getIndicatorLabel(this.filterStore.breakdownY, "label"),
            ]),
        },
        subtitle: {
          text: getCountryLabel(this.filterStore.countryX),
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
        xAxis: {
          type: "datetime",
        },
        yAxis: [
          {
            title: {
              text: getUnitLabel(this.filterStore.unitX),
            },
            min: 0,
          },
          {
            opposite: true,
            title: {
              text: getUnitLabel(this.filterStore.unitY),
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
          const { unit, period, breakdown, indicator } = this.point.options;

          return [
            `<b>${this.series.name}</b>`,
            parent.getUnitDisplay(this.point.y, unit),
            `<b>Breakdown:</b> ${getBreakdownLabel(breakdown)}`,
            `<b>Time Period:</b> ${parent.getPeriodWithExtraNotes(period, indicator)}`,
          ].join("<br/>");
        },
      };
    },
  },
};
</script>
