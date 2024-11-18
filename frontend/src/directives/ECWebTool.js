/**
 * Wrapper over the WebTools SmartLoader render function
 *
 *  https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/SmartLoader+-+API#SmartLoaderAPI-$wt.render
 *
 * Example usage:
 *
 *   <div
 *     v-ec-wt-render="{
 *       service: 'cdown',
 *       date: '01/01/2050',
 *     }"
 *   />
 */
export default {
  mounted(el, binding) {
    if (window.$wt) {
      render(el, binding);
    } else {
      window.addEventListener("wtReady", () => render(el, binding), {
        once: true,
        capture: false,
      });
    }
  },
  unmounted(el) {
    const snippet = el.querySelector("script");
    for (const key in window.$wt.components) {
      if (window.$wt.components[key] === snippet) {
        delete window.$wt.components[key];
      }
    }
  },
};

function render(el, binding) {
  if (!window.$wt.exists(binding.value.service || binding.value.utility)) {
    window.$wt.render(el, binding.value);
  }
}
