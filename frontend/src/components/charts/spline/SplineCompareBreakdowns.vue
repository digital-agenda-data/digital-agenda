<script>
import IndicatorWithGroupsFilter from "@/components/chart-filters/IndicatorWithGroupsFilter.vue";
import BaseChart from "@/components/charts/base/BaseChart.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import BreakdownGroupFilter from "@/components/chart-filters/BreakdownGroupFilter.vue";
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import BreakdownMultiFilter from "@/components/chart-filters/BreakdownMultiFilter.vue";
import {
  getBreakdownLabel,
  getCountryLabel,
  getMarkerSymbol,
  getPeriodLabel,
  getUnitLabel,
} from "@/lib/utils";
import { usePeriodStore } from "@/stores/periodStore";
import { mapState } from "pinia";

export default {
  name: "SplineCompareBreakdowns",
  extends: BaseChart,
  computed: {
    ...mapState(usePeriodStore, ["periodByCode"]),
    chartType() {
      return "spline";
    },
    filterComponents() {
      return [
        IndicatorWithGroupsFilter,
        BreakdownGroupFilter,
        {
          component: BreakdownMultiFilter,
          attrs: { allInitial: true, hidden: true, syncRoute: false },
        },
        UnitFilter,
        CountryFilter,
      ];
    },
    endpointFilters() {
      return ["breakdownGroup", "indicator", "unit", "country"];
    },
    groupBy() {
      return ["breakdown", "period"];
    },
    series() {
      return (this.breakdown || []).map((breakdown) => {
        return {
          name: getBreakdownLabel(breakdown),
          color: breakdown.chart_options?.color,
          dashStyle: breakdown.chart_options?.dash_style,
          marker: {
            symbol: getMarkerSymbol(breakdown.chart_options),
          },
          pointRange: 365 * 24 * 3600 * 1000,
          data: this.apiDataPeriods.map((periodCode) => {
            const fact = this.apiDataGrouped[breakdown.code]?.[periodCode];
            const period = this.periodByCode.get(periodCode);

            return {
              fact,
              y: fact?.value ?? null,
              x: new Date(period?.date),
              name: getPeriodLabel(period, "label"),
            };
          }),
        };
      });
    },
    chartOptions() {
      return {
        subtitle: {
          text: getCountryLabel(this.country),
        },
        legend: {
          enabled: (this.breakdown || []).length > 1,
        },
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
              enabled: false,
            },
          },
        },
      };
    },
  },
};
</script>
