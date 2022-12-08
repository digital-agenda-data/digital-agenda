import "./styles/main.scss";

import { createApp, reactive } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import router from "@/router";
import ECLInit from "@/directives/ECLInit";
import HighchartsVue from "./initHighchart";

const app = createApp(App);

app.use(router);
app.use(createPinia());
app.use(HighchartsVue);

app.mixin({
  beforeCreate() {
    // Makes this.$refs reactive
    this.$.refs = reactive({});
  },
});

app.directive("ecl-init", ECLInit);

app.mount("#digital-agenda-app");
