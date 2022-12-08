<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/filters/BreakdownWithGroupsFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import topology from "@/assets/nuts/NUTS_RG_10M_2021_3857_LEVL_0.json";

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
      ];
    },
    endpointFilters() {
      return ["breakdown", "period", "indicator", "unit"];
    },
    series() {
      return [
        {
          name: this.getDisplay(this.unit),
          data: this.apiData.map((item) => {
            return {
              code: item.country,
              value: item.value,
            };
          }),
          joinBy: ["NUTS_ID", "code"],
          states: {
            hover: {
              color: "#a4edba",
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
          map: topology,
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
          // center: [10, 58],
          // zoom: 1.5,
        },
        tooltip: {
          valueSuffix: this.getDisplay(this.unit),
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
