<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import IndicatorGroupFilter from "@/components/chart-filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/chart-filters/IndicatorFilter.vue";
import BreakdownWithGroupsFilter from "@/components/chart-filters/BreakdownWithGroupsFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import UnitFilter from "@/components/chart-filters/UnitFilter.vue";
import CountryMultiFilter from "@/components/chart-filters/CountryMultiFilter.vue";
import topologyUrl from "@/assets/topology.json?url";

const valueNotAvailableColor = "#E3E3E3";
const hoverCountryColor = "#467A39";

export default {
  name: "MapCompareCountries",
  extends: BaseChart,
  data() {
    return {
      mapData: null,
    };
  },
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
        {
          component: CountryMultiFilter,
          attrs: { allInitial: true, ignoreCountryGroups: true },
        },
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
          borderColor: "#9F9F9F",
          data: this.countries.map((country) => {
            const fact = this.apiDataGrouped[country.code];
            const value = fact?.value;

            return {
              fact,
              value,
              x: country.code,
              y: value,
              key: this.getDisplay(country),
              code: country.code,
              color: value === undefined ? valueNotAvailableColor : undefined,
            };
          }),
          // Join CNTR_ID from the topology to the code from the backend
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
          map: this.mapData,
          // Animations for maps are extremely JANKY,
          // so disable them completely.
          animation: false,
          panning: {
            enabled: false,
          },
        },
        mapNavigation: {
          enabled: false,
        },
        mapView: {
          center: [1164133.0400299034, 7610148.079491587],
          zoom: -13.35,
        },
        colorAxis: {
          min: 0,
          max: this.maxValue,
          type: "linear",
        },
        legend: {
          x: 16,
          enabled: true,
          floating: true,
          align: "center",
          layout: "horizontal",
          verticalAlign: "bottom",
        },
        plotOptions: {
          series: {
            dataLabels: {
              enabled: false,
            },
          },
        },
        responsive: {
          rules: [
            {
              condition: { minWidth: 768 },
              chartOptions: {
                mapView: {
                  center: [348227.6471561784, 7743167.912180269],
                  zoom: -12.65,
                },
                legend: {
                  align: "left",
                },
              },
            },
          ],
        },
      };
    },
  },
  methods: {
    async loadExtra() {
      if (!this.mapData) {
        this.mapData = await (await fetch(topologyUrl)).json();
      }
    },
  },
};
</script>
