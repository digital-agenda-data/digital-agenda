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
export default (el, binding) => {
  const render = () => {
    if (!window.$wt.exists(binding.value.service || binding.value.utility)) {
      window.$wt.render(el, binding.value);
    }
  };

  if (window.$wt) {
    render();
  } else {
    window.addEventListener("wtReady", render, {
      once: true,
      capture: false,
    });
  }
};
