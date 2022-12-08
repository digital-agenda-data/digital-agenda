<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import topologyAllCountries from "@/assets/topology.json";
import CountryMultiFilter from "@/components/filters/CountryMultiFilter.vue";

const valueNotAvailableColor = "#E3E3E3";
const hoverCountryColor = "#467A39";

export default {
  name: "MapCompareCountries",
  extends: BaseChart,
  computed: {
    constructorType() {
      return "mapChart";
    },
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownWithGroupsFilter,
        PeriodFilter,
        UnitFilter,
        { component: CountryMultiFilter, attrs: { allInitial: true } },
      ];
    },
    endpointFilters() {
      return ["breakdown", "period", "indicator", "unit"];
    },
    groupBy() {
      return ["country"];
    },
    series() {
      return [
        {
          data: this.countries.map((country) => {
            const apiValue = this.apiValuesGrouped[country.code];

            return {
              key: this.getDisplay(this.countryByCode.get(country.code)),
              code: country.code,
              value: apiValue,
              color:
                apiValue === undefined ? valueNotAvailableColor : undefined,
            };
          }),
          joinBy: ["CNTR_ID", "code"],
          states: {
            hover: {
              color: hoverCountryColor,
            },
          },
        },
      ];
    },
    maxValue() {
      return Math.max(...this.apiData.map((item) => item.value));
    },
    chartOptions() {
      return {
        chart: {
          map: topologyAllCountries,
        },
        legend: {
          enabled: true,
        },
        mapNavigation: {
          enabled: true,
          buttonOptions: {
            verticalAlign: "bottom",
          },
        },
        mapView: {
          // projection: {
          //   name: "WebMercator",
          // },
          center: [-52668.06327497485, 7321748.004313275],
          zoom: -13.009736538516464,
        },
        colorAxis: {
          min: 0,
          max: this.maxValue,
          type: "linear",
        },
        plotOptions: {
          series: {
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
