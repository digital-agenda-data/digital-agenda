import { createApp } from "vue";
import { createPinia } from "pinia";
import HighchartsVue from "highcharts-vue";

import App from "./App.vue";
import router from "./router";

import "./styles/main.scss";
import ECLInit from "@/directives/ECLInit";

import Highcharts from "highcharts";
import highchartsMoreInit from "highcharts/highcharts-more";
import exportingInit from "highcharts/modules/exporting";
import offlineExportingInit from "highcharts/modules/offline-exporting";
import exportingDataInit from "highcharts/modules/export-data";
import accessibilityInit from "highcharts/modules/accessibility";
import noDataToDisplayInit from "highcharts/modules/no-data-to-display";
import { SERIES_COLORS } from "@/lib/constants";

exportingInit(Highcharts);
offlineExportingInit(Highcharts);
exportingDataInit(Highcharts);
accessibilityInit(Highcharts);
noDataToDisplayInit(Highcharts);
highchartsMoreInit(Highcharts);

// Set global defaults
Highcharts.setOptions({
  chart: {
    height: "600px",
  },
  colors: SERIES_COLORS,
  exporting: {
    sourceWidth: 1024,
    sourceHeight: 600,
    buttons: {
      contextButton: {
        enabled: false,
      },
    },
  },
  title: {
    widthAdjust: -200,
  },
  subtitle: {
    widthAdjust: -400,
  },
  legend: {
    itemWidth: 150,
    layout: "vertical",
    align: "right",
    verticalAlign: "top",
    y: 60,
  },
  credits: {
    text: "European Commission, Digital Scoreboard",
    href: "https://digital-strategy.ec.europa.eu/",
  },
  yAxis: {
    allowDecimals: false,
    min: 0,
  },
  xAxis: {
    allowDecimals: false,
    title: {
      enabled: false,
    },
  },
  plotOptions: {
    series: {
      dataLabels: {
        enabled: true,
        formatter() {
          // Show "N/A" only if there is no value defined from the API.
          // The X or Y coordinates still need to be actual values (usually 0)
          // to avoid errors and to have an empty space for the missing
          // values.
          return this.point.options.apiValue === undefined ? "N/A" : null;
        },
      },
    },
  },
});

const app = createApp(App);

app.use(router);
app.use(createPinia());

app.use(HighchartsVue);

app.directive("ecl-init", ECLInit);

app.mount("#digital-agenda-app");
