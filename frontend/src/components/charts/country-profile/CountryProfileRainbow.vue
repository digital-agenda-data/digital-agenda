<script>
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import PeriodFilter from "@/components/chart-filters/PeriodFilter.vue";
import BaseChart from "@/components/charts/base/BaseChart.vue";
import {
  getCountryLabel,
  getIndicatorGroupLabel,
  getIndicatorLabel,
} from "@/lib/utils.js";
import chroma from "chroma-js";

import { useCountryProfileIndicatorStore } from "@/stores/countryProfileIndicatorStore.js";
import { mapState } from "pinia";

import missingPatternUrl from "@/assets/missing-pattern.png?url";

const BG_COLOR = "#F8F9FD";
const EU_CODE = "EU";
const TARGET_PERIOD = "2030";
const TARGET_BREAKDOWN = "dd_target_2030";
const SERIES = {
  invisible: "Invisible",
  background: "Background",
  euTarget: `EU ${TARGET_PERIOD} Target`,
  euAverage: "EU Average",
  indicatorGroup: "Indicator Group",
  mainGroup: "Main Group",
};

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
        showInLegend: false,
        enableMouseTracking: false,
        name: SERIES.background,
        data: this.getItems().map((item) => {
          return {
            item,
            y: 100,
            name: getIndicatorLabel(item.indicator),
            color: BG_COLOR,
          };
        }),
      };
    },
    countrySeries() {
      return {
        showInLegend: false,
        enableMouseTracking: false,
        name: getCountryLabel(this.country),
        data: this.getItems().map((item) => {
          const value = item.isMissing ? 100 : Math.abs(item.fact?.value || 0);
          return {
            item,
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
        showInLegend: false,
        type: "scatter",
        name: SERIES.euAverage,
        enableMouseTracking: false,
        data: this.getItems({ country: EU_CODE }).map((item) => {
          const iconUrl = this.getStarIcon(BG_COLOR, item.color);
          return {
            item,
            y: item.fact?.value || 0,
            name: getIndicatorLabel(item.indicator),
            visible: false,
            marker: {
              symbol: `url(${iconUrl})`,
            },
          };
        }),
        states: {
          inactive: { opacity: 1 },
        },
      };
    },
    euTargetSeries() {
      return {
        showInLegend: false,
        enableMouseTracking: false,
        name: SERIES.euTarget,
        data: this.getItems({
          country: EU_CODE,
          period: TARGET_PERIOD,
          breakdown: TARGET_BREAKDOWN,
        })
          .filter((item) => !item.isMissing)
          .map((item) => {
            return {
              item,
              color: item.colorLighter,
              y: item.fact?.value || 0,
              name: getIndicatorLabel(item.indicator),
            };
          }),
      };
    },
    groupCounts() {
      return this.getGroupCounts((item) => item.indicator_group);
    },
    mainGroupCounts() {
      return this.getGroupCounts((item) => item.indicator_group.parent);
    },
    groupSeries() {
      return {
        showInLegend: false,
        type: "pie",
        name: SERIES.indicatorGroup,
        data: this.groupCounts.map(({ group, colorLight, count }) => {
          return {
            name: getIndicatorGroupLabel(group),
            color: colorLight,
            y: count,
          };
        }),
        size: "46.5%",
        innerSize: "90%",
        startAngle: -90,
        endAngle: 90,
      };
    },
    mainGroupSeries() {
      return {
        // This series is only use to generate the legend.
        showInLegend: true,
        visible: false,
        type: "pie",
        name: SERIES.mainGroup,
        data: this.mainGroupCounts.map(({ group, color, count }) => {
          return {
            name: getIndicatorGroupLabel(group),
            color,
            y: count,
          };
        }),
        size: "41.5%",
        innerSize: "90%",
        startAngle: -90,
        endAngle: 90,
      };
    },
    invisibleSeries() {
      return {
        showInLegend: false,
        name: SERIES.invisible,
        data: [
          // Invisible series to overlap with the other column series.
          // This is the only one that listens to mouse events and triggers the
          // tooltip. This way the position of the tooltip is consistent and
          // smooth.
          ...this.getItems().map((item) => {
            return {
              item,
              y: 100,
              name: getIndicatorLabel(item.indicator),
              color: "#00000000",
              states: {
                hover: {
                  color: "#00000011",
                },
              },
            };
          }),
          // Highchart puts the last column with the left side AT the endAngle.
          // Because of that there the last column will drop below the 180deg
          // that want for our semicircle.
          // By adding this invisible column, we can make sure that the last
          // real column is properly positioned.
          {
            item: {},
            y: 0,
            name: "// EXTRA FOR PADDING",
            visible: false,
          },
        ],
      };
    },
    series() {
      return [
        this.groupSeries,
        this.mainGroupSeries,
        this.backgroundSeries,
        this.euTargetSeries,
        this.countrySeries,
        this.euAverageSeries,
        this.invisibleSeries,
      ];
    },
    chartOptions() {
      const parent = this;
      return {
        chart: {
          polar: true,
          type: "column",
          margin: [0, 0, -500, 0],
        },
        title: {
          text: this.joinStrings([getCountryLabel(this.country)]),
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
                  parent.showAverage(this.series.chart, this.index, true);
                  parent.fillCenter(this.series.chart, this.item);
                },
                mouseOut: function () {
                  parent.showAverage(this.series.chart, this.index, false);
                  parent.fillCenter(this.series.chart);
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
          innerSize: "55%",
        },
      };
    },
    legend() {
      const defaults = {
        enabled: true,
        events: {
          itemClick() {
            return false;
          },
        },
      };
      if (this.currentChart?.legend_layout === "vertical") {
        return {
          ...defaults,
          itemWidth: 150,
          layout: "vertical",
          align: "right",
          verticalAlign: "top",
        };
      } else {
        return {
          ...defaults,
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom",
        };
      }
    },
    tooltip() {
      const parent = this;
      return {
        useHTML: true,
        formatter() {
          if (
            this.series.name === SERIES.indicatorGroup ||
            this.series.name === SERIES.mainGroup
          ) {
            return `<b>${this.series.name}</b><br/>${this.name}`;
          }

          const countryItem = parent.getChartItem(this.item);
          const euAverageItem = parent.getChartItem(this.item, {
            country: EU_CODE,
          });
          const euTargetItem = parent.getChartItem(this.item, {
            country: EU_CODE,
            period: TARGET_PERIOD,
            breakdown: TARGET_BREAKDOWN,
          });
          const countryName = getCountryLabel(parent.country);

          const result = [
            `<b>${this.name}</b>`,
            [
              `<span class="dot" style="background-color: ${countryItem.color}"></span>`,
              `${countryName}:&nbsp;`,
              `<b>${countryItem.valueDisplay}</b>`,
            ].join(" "),
            [
              `<span class="dot" style="background-color: ${countryItem.colorLight}"></span>`,
              `${SERIES.euTarget}:&nbsp;`,
              `<b>${euTargetItem.valueDisplay}</b>`,
            ].join(" "),
            [
              `<span style="color: ${countryItem.color}">&starf;</span>`,
              `${SERIES.euAverage}:&nbsp;`,
              `<b>${euAverageItem.valueDisplay}</b>`,
            ].join(" "),
          ];

          const referencePeriod =
            countryItem.fact?.reference_period ??
            euAverageItem.fact?.reference_period ??
            euTargetItem.fact?.reference_period;

          const extraNotes = parent
            .getExtraNotes(parent.period, countryItem.indicator)
            .join(" ");

          if (referencePeriod) {
            result.push(`Reference period: ${referencePeriod} ${extraNotes}`);
          } else {
            result.push(extraNotes);
          }

          const lines = result.map((line) => `<span>${line}</span>`).join("");

          return `<div class="countryProfileTooltip">${lines}</div>`;
        },
      };
    },
  },
  methods: {
    getItems(override = {}) {
      return this.chartDimensionList.map((item) =>
        this.getChartItem(item, override),
      );
    },
    getChartItem(item, override = {}) {
      let fact = this.apiDataGrouped;
      fact = fact[override.period ?? item.period.code] ?? {};
      fact = fact[override.indicator ?? item.indicator.code] ?? {};
      fact = fact[override.breakdown ?? item.breakdown.code] ?? {};
      fact = fact[override.unit ?? item.unit.code] ?? {};
      fact = fact[override.country ?? this.country.code] ?? {};

      const base = chroma(
        item.indicator_group.color ||
          item.indicator_group.parent?.color ||
          "#6083f6",
      );

      return {
        ...item,
        fact,
        valueDisplay: this.getUnitDisplay(fact?.value, item.unit),
        color: base.hex(),
        colorLight: base.brighten(0.8).desaturate(0.3).hex(),
        colorLighter: base.brighten(1.6).desaturate(0.6).hex(),
        colorDark: base.darken(1.4).hex(),
        isMissing: typeof fact?.value === "undefined",
      };
    },
    getGroupCounts(getGroup) {
      const groupCounts = {};
      this.getItems().forEach((item, index) => {
        const group = getGroup(item);
        if (!group) return;

        groupCounts[group.code] ??= {
          group,
          color: item.color,
          colorLight: item.colorLight,
          count: 0,
          start: index,
        };
        groupCounts[group.code].count += 1;
      });
      return Object.values(groupCounts);
    },
    fillCenter(chart, item = null) {
      const series = chart.series.find((s) => s.name === SERIES.indicatorGroup);

      let content = "";
      if (item) {
        content = [
          `<div class="parent">
            <span>${getIndicatorGroupLabel(item.indicator_group.parent)}</span>
            <img src="${item.indicator_group.parent?.icon}" alt=""/>
          </div>`,
          `<div class="group">${getIndicatorGroupLabel(item.indicator_group)}</div>`,
          `<div class="indicator" style="color: ${item.colorDark}">${getIndicatorLabel(item.indicator)}</div>`,
        ].join("\n");
      }

      const labelText = `<div class="countryProfileCenter">${content}</div>`;
      if (!series.customLabel) {
        series.customLabel = chart.renderer
          .label(labelText, 0, 0, void 0, void 0, void 0, true)
          .css({
            pointerEvents: "none",
          })
          .add();
      } else {
        series.customLabel.attr({
          text: labelText,
        });
      }

      series.customLabel.attr({
        text: labelText,
        x:
          chart.pane[0].center[0] +
          chart.plotLeft -
          series.customLabel.attr("width") / 2,
        y:
          chart.pane[0].center[1] +
          chart.plotTop -
          series.customLabel.attr("height") -
          10,
      });
    },
    showAverage(chart, index, visible) {
      const scatter = chart.series.find((s) => s.name === SERIES.euAverage);
      const pt = scatter.points[index];
      if (pt && !pt.item.isMissing) {
        pt.update({ visible }, false);
        chart.redraw();
      }
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
      return `data:image/svg+xml;base64,${btoa(svgString)}`;
    },
  },
};
</script>

<style lang="scss">
.countryProfileTooltip {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;

  .dot {
    display: inline-block;
    vertical-align: middle;
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }
}

.countryProfileCenter {
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  align-items: center;
  gap: 1rem;
  width: 20rem;
  white-space: normal;

  .parent {
    display: flex;
    align-items: center;
    gap: 0.25rem;

    font-size: 0.75rem;
    text-transform: uppercase;
    border: 1px solid #26324b;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;

    img {
      height: 0.75rem;
    }
  }

  .group {
    font-size: 1rem;
    font-weight: bold;
  }

  .indicator {
    font-size: 1.5rem;
  }
}
</style>
