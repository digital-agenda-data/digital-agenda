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
  getCustomOptions,
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
      return ["breakdownGroup", "indicator", "unit"];
    },
    groupBy() {
      return ["country", "breakdown", "period"];
    },
    series() {
      return (this.countries || [])
        .map((country) => {
          return (this.breakdown || []).map((breakdown) => {
            return {
              ...getCustomOptions(breakdown),
              name: this.joinStrings([
                getCountryLabel(country),
                getBreakdownLabel(breakdown),
              ]),
              pointRange: 365 * 24 * 3600 * 1000,
              data: this.apiDataPeriods.map((periodCode) => {
                const fact =
                  this.apiDataGrouped[country.code]?.[breakdown.code]?.[
                    periodCode
                  ];
                const period = this.periodByCode.get(periodCode);

                return {
                  fact,
                  y: fact?.value ?? null,
                  x: period?.date,
                  name: this.getPeriodWithExtraNotes(period),
                };
              }),
            };
          });
        })
        .flat();
    },
    chartOptions() {
      return {
        subtitle: {
          text: this.joinStrings(this.countries.map(getCountryLabel)),
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
          },
        },
      };
    },
  },
};
</script>
