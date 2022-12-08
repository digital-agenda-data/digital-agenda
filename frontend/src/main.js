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
  methods: {
    errorMustImplement(propName) {
      throw Error(
        `Component "${this.$options.name}" must implement the "${propName}" property to work correctly.`
      );
    },
  },
});

app.directive("ecl-init", ECLInit);

app.mount("#digital-agenda-app");
