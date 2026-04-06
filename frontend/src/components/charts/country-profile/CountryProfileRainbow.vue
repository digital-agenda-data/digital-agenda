<script>
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import BaseChart from "@/components/charts/base/BaseChart.vue";
import { getCountryLabel, getIndicatorLabel } from "@/lib/utils.js";
import { useCountryProfileIndicatorStore } from "@/stores/countryProfileIndicatorStore.js";
import Highcharts from "highcharts";
import { mapState } from "pinia";

import missingPatternUrl from "@/assets/missing-pattern.png?url";

const EU_CODE = "EU";
const TARGET_PERIOD = "2030";
const TARGET_BREAKDOWN = "dd_target_2030";

export default {
  name: "CountryProfileRainbow",
  extends: BaseChart,
  computed: {
    ...mapState(useCountryProfileIndicatorStore, [
      "countryProfileIndicatorList",
    ]),
    chartType() {
      return "column";
    },
    filterComponents() {
      return [
        {
          component: CountryFilter,
          attrs: { ignoreCountryGroups: true },
        },
        PeriodFilter,
      ];
    },
    endpointFilters() {
      return ["country", "period"];
    },
    extraFilterValues() {
      return {
        country: [EU_CODE],
        period: [TARGET_PERIOD],
      };
    },
    groupBy() {
      return ["period", "indicator", "breakdown", "unit", "country"];
    },
    chartDimensionList() {
      return this.countryProfileIndicatorList.filter(
        (item) => item.is_percentage && item.period.code === this.period.code,
      );
    },
    backgroundSeries() {
      return {
        name: "Background",
        data: this.getItems().map((item) => {
          return {
            fact: {},
            isMissing: item.isMissing,
            y: 100,
            name: getIndicatorLabel(item.indicator),
            color: "#F8F9FD",
          };
        }),
        enableMouseTracking: false,
        showInLegend: false,
      };
    },
    countrySeries() {
      return {
        name: getCountryLabel(this.country),
        data: this.getItems().map((item) => {
          const value = item.isMissing ? 100 : Math.abs(item.fact?.value || 0);
          return {
            fact: item.fact,
            isMissing: item.isMissing,
            y: value,
            name: getIndicatorLabel(item.indicator),
            color: !item.isMissing
              ? item.color
              : {
                  pattern: {
                    image: missingPatternUrl,
                    aspectRatio: 1,
                    width: 100,
                    height: 100,
                    opacity: 1,
                  },
                },
          };
        }),
      };
    },
    euAverageSeries() {
      return {
        type: "scatter",
        name: "EU Average",
        enableMouseTracking: false,
        data: this.getItems({ country: EU_CODE }).map((item) => {
          return {
            fact: item.fact,
            isMissing: item.isMissing,
            y: item.fact?.value || 0,
            name: getIndicatorLabel(item.indicator),
            visible: false,
          };
        }),
      };
    },
    euTargetSeries() {
      return {
        name: `EU ${TARGET_PERIOD} Target`,
        data: this.getItems({
          country: EU_CODE,
          period: TARGET_PERIOD,
          breakdown: TARGET_BREAKDOWN,
        })
          .filter((item) => !item.isMissing)
          .map((item) => {
            return {
              fact: item.fact,
              isMissing: item.isMissing,
              color: item.lightColor,
              y: item.fact?.value || 0,
              name: getIndicatorLabel(item.indicator),
            };
          }),
      };
    },
    series() {
      return [
        this.backgroundSeries,
        this.euTargetSeries,
        this.countrySeries,
        this.euAverageSeries,
      ];
    },
    chartOptions() {
      return {
        chart: {
          polar: true,
          type: "column",
        },
        plotOptions: {
          column: {
            grouping: false,
            pointPadding: 0,
            groupPadding: 0,
            borderWidth: 1,
            states: {
              inactive: { opacity: 1 },
            },
            point: {
              events: {
                mouseOver: function () {
                  const scatter = this.series.chart.series.find(
                    (s) => s.name === "EU Average",
                  );
                  const pt = scatter.points[this.index];
                  if (pt && !pt.isMissing) {
                    pt.update({ visible: true }, false);
                    this.series.chart.redraw();
                  }
                },
                mouseOut: function () {
                  const scatter = this.series.chart.series.find(
                    (s) => s.name === "EU Average",
                  );
                  const pt = scatter.points[this.index];
                  if (pt) {
                    pt.update({ visible: false }, false);
                    this.series.chart.redraw();
                  }
                },
              },
            },
          },
          scatter: {
            grouping: false,
            states: {
              inactive: { opacity: 1 },
              hover: {
                enabled: true,
                halo: { size: 0 },
                marker: {
                  enabled: true,
                  fillColor: "#fff",
                  lineColor: "#185FA5",
                  lineWidth: 2.5,
                },
              },
            },
            marker: {
              symbol: "circle",
              radius: 7,
              fillColor: "#fff",
              lineColor: "#185FA5",
              lineWidth: 2.5,
            },
          },
        },
        xAxis: {
          type: "category",
          lineWidth: 0,
          gridLineWidth: 0,
          labels: {
            enabled: false,
          },
        },
        yAxis: {
          lineWidth: 0,
          gridLineWidth: 0,
          labels: {
            enabled: false,
          },
        },
        pane: {
          startAngle: -90,
          endAngle: 90,
          size: "160%",
          innerSize: "50%",
          center: ["50%", "85%"],
        },
      };
    },
  },
  methods: {
    getItems({
      period = null,
      indicator = null,
      breakdown = null,
      unit = null,
      country = null,
    } = {}) {
      return this.chartDimensionList.map((item) => {
        const color = new Highcharts.Color(
          item.indicator_group.color ||
            item.indicator_group.parent?.color ||
            "#6083f6",
        );
        let fact = this.apiDataGrouped;
        fact = fact[period ?? item.period.code] ?? {};
        fact = fact[indicator ?? item.indicator.code] ?? {};
        fact = fact[breakdown ?? item.breakdown.code] ?? {};
        fact = fact[unit ?? item.unit.code] ?? {};
        fact = fact[country ?? this.country.code] ?? {};
        return {
          ...item,
          fact,
          color: color.get(),
          lightColor: color.brighten(0.4).get(),
          darkColor: color.brighten(-0.4).get(),
          isMissing: typeof fact?.value === "undefined",
        };
      });
    },
  },
};
</script>
