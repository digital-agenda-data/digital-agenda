/**
 * Custom directive to initialize an ECL component when it is added to the DOM.
 * Also destroys the component when the root element is unmounted from the DOM.
 *
 * Example usage:
 *
 * <div
 *   v-ecl-init
 *   role="alert"
 *   class="ecl-message ecl-message--info"
 *   data-ecl-message
 *   data-ecl-auto-init="Message"
 * >
 *   ... Message component ...
 * </div>
 *
 * Makes it much easier to manage components as they are dynamically added/removed
 * from the app.
 *
 * See also documentation for the ECL component library here:
 *
 *   https://ec.europa.eu/component-library/ec/getting-started/
 *
 */
export default {
  // called when the bound element's parent component
  // and all its children are mounted.
  mounted(el, binding) {
    initComponent(el, binding.value);
  },
  // called when the parent component is unmounted
  unmounted(el) {
    destroyComponent(el);
  },
};

function initComponent(el, options) {
  // Requires attribute data-ecl-auto-init="COMPONENT"
  const componentName = el.dataset.eclAutoInit;
  const propName = `ECL${componentName}`;

  if (el[propName]) {
    console.warn("Component already initialized for:", el);
    return;
  }

  if (!window.ECL) {
    console.warn("ECL not initialized");
    return;
  }

  if (!componentName || !window.ECL[componentName]) {
    console.warn(
      `Invalid or missing data-ecl-auto-init value: ${componentName}`,
      el,
    );
    return;
  }

  el[propName] = new window.ECL[componentName](el, options ?? {});
  el[propName].init();
}

function destroyComponent(el) {
  // Requires attribute data-ecl-auto-init="COMPONENT"
  const componentName = el.dataset.eclAutoInit;

  if (!window.ECL) {
    console.warn("ECL not initialized");
    return;
  }

  if (!componentName || !window.ECL[componentName]) {
    console.warn(
      `Invalid or missing data-ecl-auto-init value: ${componentName}`,
      el,
    );
    return;
  }

  // ECL autoInit attaches the created component to the DOM Element.
  // E.g. for the 'Message' component the ECLMessage is created.
  const component = el[`ECL${componentName}`];

  if (!component) {
    console.warn(`Component '${componentName}' not found for:`, el);
    return;
  }

  component.destroy();
}
