<script>
import BaseCompareTwoChart from "@/components/charts/base/BaseCompareTwoChart.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import EclHeading from "@/components/ecl/EclHeading.vue";
import { apiCall } from "@/lib/api";

export default {
  name: "ScatterCompareTwoIndicators",
  extends: BaseCompareTwoChart,
  data() {
    return {
      countriesList: [],
    };
  },
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
    countryByCode() {
      const result = new Map();
      for (const country of this.countriesList) {
        result.set(country.code, country);
      }
      return result;
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
            },
          ],
        };
      });
    },
    chartOptions() {
      return {
        chart: {
          type: "scatter",
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
  methods: {
    async loadExtra() {
      if (this.countriesList.length === 0) {
        this.countriesList = await apiCall("GET", `/countries/`);
      }
    },
  },
};
</script>
