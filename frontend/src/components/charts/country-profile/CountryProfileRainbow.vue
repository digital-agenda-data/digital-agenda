<script>
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import BaseChart from "@/components/charts/base/BaseChart.vue";
import {
  brightenColor,
  getCountryLabel,
  getIndicatorGroupLabel,
  getIndicatorLabel,
} from "@/lib/utils.js";
import { useCountryProfileIndicatorStore } from "@/stores/countryProfileIndicatorStore.js";
import { mapState } from "pinia";

import missingPatternUrl from "@/assets/missing-pattern.png?url";

const BG_COLOR = "#F8F9FD";
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
    invisibleSeries() {
      return {
        name: "Invisible",
        enableMouseTracking: false,
        showInLegend: false,
        data: [
          ...this.getItems().map((item) => {
            return {
              fact: {},
              y: 0,
              name: getIndicatorLabel(item.indicator),
              visible: false,
            };
          }),
          // Highchart puts the last column with the left side AT the endAngle.
          // Because of that there the last column will drop below the 180deg
          // that want for our semicircle.
          // By adding this invisible column, we can make sure that the last
          // real column is properly positioned.
          {
            fact: {},
            y: 0,
            name: "// EXTRA FOR PADDING",
            visible: false,
          },
        ],
      };
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
            color: BG_COLOR,
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
            marker: {
              symbol: this.getStarIcon(BG_COLOR, item.color),
            },
          };
        }),
        states: {
          inactive: { opacity: 1 },
          hover: {
            enabled: true,
            marker: {
              enabled: true,
            },
          },
        },
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
    groupCounts() {
      const groupCounts = {};
      this.getItems().forEach((item, index) => {
        const group = item.indicator_group;

        groupCounts[group.code] ??= {
          group,
          color: item.lightColor,
          count: 0,
          start: index,
        };
        groupCounts[group.code].count += 1;
      });
      return Object.values(groupCounts);
    },
    groupSeries() {
      return {
        type: "pie",
        name: "Indicator Groups",
        data: this.groupCounts.map(({ group, color, count }) => {
          return {
            name: getIndicatorGroupLabel(group),
            color,
            y: count,
          };
        }),
        size: "35%",
        innerSize: "90%",
        startAngle: -90,
        endAngle: 90,
      };
    },
    series() {
      return [
        this.groupSeries,
        this.invisibleSeries,
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
          margin: [0, 0, -500, 0],
        },
        plotOptions: {
          pie: {
            states: {
              inactive: { opacity: 1 },
            },
            dataLabels: {
              enabled: false,
            },
          },
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
          innerSize: "42%",
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
        const color =
          item.indicator_group.color ||
          item.indicator_group.parent?.color ||
          "#6083f6";

        let fact = this.apiDataGrouped;
        fact = fact[period ?? item.period.code] ?? {};
        fact = fact[indicator ?? item.indicator.code] ?? {};
        fact = fact[breakdown ?? item.breakdown.code] ?? {};
        fact = fact[unit ?? item.unit.code] ?? {};
        fact = fact[country ?? this.country.code] ?? {};
        return {
          ...item,
          fact,
          color: color,
          lightColor: brightenColor(color, 0.2),
          darkColor: brightenColor(color, -0.4),
          isMissing: typeof fact?.value === "undefined",
        };
      });
    },
    getStarIcon(bgColor, starColor) {
      const svgString = `<svg
      width="24px"
      height="24px"
      fill="${starColor}"
      viewBox="-256 -256 1024.00 1024.00"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g
        id="SVGRepo_bgCarrier"
        stroke-width="0"
        transform="translate(0,0), scale(1)"
      >
        <rect
          x="-256"
          y="-256"
          width="1024.00"
          height="1024.00"
          rx="512"
          fill="${bgColor}"
          strokeWidth="0"
        />
      </g>

      <g
        id="SVGRepo_tracerCarrier"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="1.024"
      />

      <g id="SVGRepo_iconCarrier">
        <path d="M496,203.3H312.36L256,32,199.64,203.3H16L166.21,308.7,107.71,480,256,373.84,404.29,480,345.68,308.7Z" />
      </g>
    </svg>`;
      return `url(data:image/svg+xml;base64,${btoa(svgString)})`;
    },
  },
};
</script>
