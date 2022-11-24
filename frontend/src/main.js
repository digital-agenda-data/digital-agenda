import { createApp } from "vue";
import { createPinia } from "pinia";
import HighchartsVue from "highcharts-vue";

import App from "./App.vue";
import router from "./router";

import "./styles/main.scss";
import ECLInit from "@/directives/ECLInit";

import Highcharts from "highcharts";
import exportingInit from "highcharts/modules/exporting";
import offlineExportingInit from "highcharts/modules/offline-exporting";
import exportingDataInit from "highcharts/modules/export-data";
import accessibilityInit from "highcharts/modules/accessibility";

exportingInit(Highcharts);
offlineExportingInit(Highcharts);
exportingDataInit(Highcharts);
accessibilityInit(Highcharts);

// Set defaults
Highcharts.setOptions({
  chart: {
    height: "600px",
  },
  exporting: {
    sourceWidth: 1024,
    sourceHeight: 600,
  },
  credits: {
    text: "European Commission, Digital Scoreboard",
    href: "https://digital-strategy.ec.europa.eu/",
  },
});

const app = createApp(App);

app.use(router);
app.use(createPinia());

app.use(HighchartsVue);

app.directive("ecl-init", ECLInit);

app.mount("#digital-agenda-app");
