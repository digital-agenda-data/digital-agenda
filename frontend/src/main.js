import { createApp } from "vue";
import { createPinia } from "pinia";
import HighchartsVue from "highcharts-vue";

import App from "./App.vue";
import router from "./router";

import "./styles/main.css";
import ECLInit from "@/directives/ECLInit";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(HighchartsVue);

app.directive("ecl-init", ECLInit);

app.mount("#app");
