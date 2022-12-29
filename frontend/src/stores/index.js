import { createPinia } from "pinia";

import router from "@/router";

const pinia = createPinia();

/**
 * Plugin to make currentRoute available in pinia getters via this.$route
 */
pinia.use(({ store }) => {
  store.$route = router.currentRoute;
});

export default pinia;
