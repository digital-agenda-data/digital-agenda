/**
 * Dynamically generate tests for a range of common viewports sizes.
 *
 * The current size is passed to the fn.
 *
 * @param title {String}
 * @param fn {Function}
 * @param viewports {Array}
 */
export default function (title, fn, viewports = null) {
  let configuredViewports = [];

  if (viewports) {
    configuredViewports = viewports;
  } else if (Cypress.expose("viewport")) {
    configuredViewports = Cypress.expose("viewport")
      .split(";")
      .map((viewport) => viewport.split("x").map((i) => parseInt(i)));
  } else {
    configuredViewports = Cypress.config("viewports");
  }

  for (const size of configuredViewports) {
    describe(`${title} (${size.join("x")})`, () => {
      beforeEach(() => {
        cy.viewport(...size);
      });

      fn(...size);
    });
  }
}
