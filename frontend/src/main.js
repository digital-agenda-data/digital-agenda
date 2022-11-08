import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";
import ECLInit from "@/directives/ECLInit";

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.directive("ecl-init", ECLInit);

app.mount("#app");
