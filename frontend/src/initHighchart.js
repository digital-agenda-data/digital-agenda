/**
 * Init Highcharts:
 *
 *  - init extra Highcharts modules required
 *  - set global option defaults
 *  - export the Chart component from highcharts-vue
 */

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
    sourceWidth: 1024,
    buttons: {
      contextButton: {
        enabled: false,
      },
    },
  },
  credits: {
    text: "European Commission, Digital Scoreboard",
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
  },
  responsive: {
    rules: [
      {
        condition: { minWidth: 768 },
        chartOptions: {
          legend: {
            itemWidth: 150,
            layout: "vertical",
            align: "right",
            verticalAlign: "middle",
          },
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

export default HighchartsVue;
