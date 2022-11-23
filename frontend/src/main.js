import { createApp } from "vue";
import { createPinia } from "pinia";
import HighchartsVue from "highcharts-vue";

import App from "./App.vue";
import router from "./router";

import "./styles/main.css";
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

const app = createApp(App);

app.use(router);
app.use(createPinia());

app.use(HighchartsVue);

app.directive("ecl-init", ECLInit);

app.mount("#app");
