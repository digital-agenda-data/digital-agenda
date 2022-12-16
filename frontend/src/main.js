import "./styles/main.scss";

import { createApp, reactive } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import router from "@/router";
import ECLInit from "@/directives/ECLInit";
import visible from "@/directives/visible";
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
    /**
     * Called to help avoid developer errors when extending components.
     */
    errorMustImplement(propName) {
      throw Error(
        `Component "${this.$options.name}" must implement the "${propName}" property to work correctly.`
      );
    },
    /**
     * Get a bound method of a base component. Example usage:
     *
     *  this.super(BaseComponent).foo();
     *
     * @param superComponent {Object}
     * @return {Function}
     */
    super(superComponent) {
      return new Proxy(superComponent, {
        get: (target, name) => {
          const method = target.methods?.[name] || target.computed?.[name];
          if (method) {
            return method.bind(this);
          }
        },
      });
    },
  },
});

app.directive("ecl-init", ECLInit);
app.directive("visible", visible);

app.mount("#digital-agenda-app");
