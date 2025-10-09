/**
 * Init Highcharts:
 *
 *  - init extra Highcharts modules required
 *  - set global option defaults
 *  - export the Chart component from highcharts-vue
 */

import { useAppSettings } from "@/stores/appSettingsStore";
import HighchartsVue from "highcharts-vue";

import Highcharts from "highcharts";

import "highcharts/modules/exporting";
import "highcharts/modules/export-data";
import "highcharts/modules/offline-exporting";

import "highcharts/modules/accessibility";
import "highcharts/modules/no-data-to-display";

// highchart-more required for the Bubble chart
// (adds a 3rd dimension to the scatter plot)
import "highcharts/highcharts-more";
import "highcharts/modules/map";

import { SERIES_COLORS } from "@/lib/constants";

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

export function setHighchartsDefaults() {
  const appSettings = useAppSettings().appSettings;

  // Set global defaults
  Highcharts.setOptions({
    accessibility: {
      screenReaderSection: {
        beforeChartFormat: [
          "<h2>{chartTitle}</h2>",
          "<div>{typeDescription}</div>",
          "<div>{chartSubtitle}</div>",
          "<div>{chartLongdesc}</div>",
          "<div>{playAsSoundButton}</div>",
          "<div>{viewTableButton}</div>",
          "<div>{xAxisDescription}</div>",
          "<div>{yAxisDescription}</div>",
          "<div>{annotationsTitle}{annotationsList}</div>",
          ].join("")
      }
    },
    chart: {
      // Chart height is set by the parent container
      height: null,
      zooming: {
        pinchType: "x",
      },
      animation: !prefersReducedMotion,
    },
    colors: SERIES_COLORS,
    exporting: {
      sourceHeight: 690,
      sourceWidth: 1280,
      buttons: {
        contextButton: {
          enabled: false,
        },
      },
    },
    credits: {
      text: appSettings.chart_credits || "European Commission",
      // Disable credit link on small screens
      href: null,
    },
    yAxis: {
      allowDecimals: false,
      // improve automatic setting of max value for percentages close to 100%
      endOnTick: false,
    },
    xAxis: {
      allowDecimals: false,
      title: {
        enabled: false,
      },
      dateTimeLabelFormats: {
        // The day formatter is likely only used when displaying 1 datapoint in
        // the (sp)line charts.
        // Avoid showing "July 1st" and instead show only the year.
        day: "%Y",
      },
    },
    plotOptions: {
      series: {
        animation: !prefersReducedMotion,
        events: {
          // Disable selecting series from the legend on small screen
          legendItemClick() {
            return false;
          },
        },
      },
      column: {
        // Make sure we show zero or close to zero values
        minPointLength: 3,
      },
    },
    responsive: {
      rules: [
        {
          condition: { minWidth: 768 },
          chartOptions: {
            credits: {
              // Enable credit links on larger screens.
              href: "https://digital-strategy.ec.europa.eu/",
            },
            plotOptions: {
              series: {
                animation: !prefersReducedMotion,
                events: {
                  // Enable selecting series from the legend on large screens
                  legendItemClick() {
                    return true;
                  },
                },
              },
            },
          },
        },
      ],
    },
  });
}
export default HighchartsVue;
