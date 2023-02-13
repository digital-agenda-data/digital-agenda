/**
 * Dynamically generate tests for a range of common viewports sizes.
 *
 * The current size is passed to the fn.
 *
 * @param title {String}
 * @param fn {Function}
 */
export default function (title, fn) {
  let viewports = Cypress.config("viewports");

  if (Cypress.env("viewport")) {
    viewports = Cypress.env("viewport")
      .split(";")
      .map((viewport) => viewport.split("x").map((i) => parseInt(i)));
  }

  for (const size of viewports) {
    describe(`${title} (${size.join("x")})`, () => {
      beforeEach(() => {
        cy.viewport(...size);
      });

      fn(...size);
    });
  }
}
