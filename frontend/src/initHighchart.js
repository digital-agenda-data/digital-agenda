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

import exportingInit from "highcharts/modules/exporting";
import exportingDataInit from "highcharts/modules/export-data";
import offlineExportingInit from "highcharts/modules/offline-exporting";

import accessibilityInit from "highcharts/modules/accessibility";
import noDataToDisplayInit from "highcharts/modules/no-data-to-display";

// highchart-more required for the Bubble chart
// (adds a 3rd dimension to the scatter plot)
import highchartsMoreInit from "highcharts/highcharts-more";
import mapInit from "highcharts/modules/map";

import { SERIES_COLORS } from "@/lib/constants";

exportingInit(Highcharts);
exportingDataInit(Highcharts);
offlineExportingInit(Highcharts);

accessibilityInit(Highcharts);
noDataToDisplayInit(Highcharts);

mapInit(Highcharts);
highchartsMoreInit(Highcharts);

export function setHighchartsDefaults() {
  const appSettings = useAppSettings().appSettings;

  // Set global defaults
  Highcharts.setOptions({
    chart: {
      // Chart height is set by the parent container
      height: null,
      zooming: {
        pinchType: "x",
      },
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
        events: {
          // Disable selecting series from the legend on small screen
          legendItemClick() {
            return false;
          },
        },
        dataLabels: {
          enabled: true,
          formatter() {
            // Show "N/A" only if there is no value defined from the API.
            // The X or Y coordinates still need to be actual values (usually 0)
            // to avoid errors and to have an empty space for the missing
            // values.
            const fact = this.point.options.fact;
            if (fact && (fact.value === undefined || fact.value === null)) {
              return "N/A";
            }
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
