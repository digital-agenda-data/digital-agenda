<script>
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import BaseMultiAxisChart from "@/components/charts/base/BaseMultiAxisChart.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import {
  forceArray,
  getBreakdownLabel,
  getCountryLabel,
  getCustomOptions,
  getIndicatorLabel,
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
        X: ["indicatorX", "breakdownX", "unitX"],
        Y: ["indicatorY", "breakdownY", "unitY"],
      };
    },
    groupBy() {
      return ["axis", "country", "period"];
    },
    countries() {
      return forceArray(this.filterStore.X.country);
    },
    isSameUnit() {
      return this.filterStore.X.unit?.code === this.filterStore.Y.unit?.code;
    },
    series() {
      return ["X", "Y"]
        .map((axis, index) => {
          return (this.countries || []).map((country) => {
            const unit = this.filterStore[axis].unit;
            const breakdown = this.filterStore[axis].breakdown;
            const indicator = this.filterStore[axis].indicator;

            return {
              ...getCustomOptions([breakdown, indicator]),
              yAxis: this.isSameUnit ? 0 : index,
              name: this.joinStrings([
                getCountryLabel(country),
                getIndicatorLabel(indicator),
              ]),
              pointRange: 365 * 24 * 3600 * 1000,
              data: this.apiDataPeriods.map((periodCode) => {
                const apiValue =
                  this.apiValuesGrouped[axis]?.[country.code]?.[periodCode];
                const period = this.periodByCode.get(periodCode);

                return {
                  y: apiValue,
                  x: period?.date,
                  name: this.getPeriodWithExtraNotes(period, indicator),
                  unit,
                  period,
                  indicator,
                  breakdown,
                };
              }),
            };
          });
        })
        .flat();
    },
    chartOptions() {
      const yAxis = [
        {
          title: {
            text: getUnitLabel(this.filterStore.unitX),
          },
          min: 0,
        },
      ];
      if (!this.isSameUnit) {
        yAxis.push({
          opposite: true,
          title: {
            text: getUnitLabel(this.filterStore.unitY),
          },
          min: 0,
        });
      }

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
          text: this.joinStrings(this.countries.map(getCountryLabel)),
        },
        legend: {
          enabled: true,
        },
        plotOptions: {
          series: {
            connectNulls: true,
          },
        },
        xAxis: {
          type: "datetime",
        },
        yAxis,
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
