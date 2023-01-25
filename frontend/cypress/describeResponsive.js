const sizes = [
  [1920, 1080],
  [1440, 900],
  [1366, 768],
  [1280, 800],
  [1024, 768],
  [768, 1024],
  [800, 1280],
  [600, 960],
  [480, 853],
  [414, 896],
  [375, 667],
  [360, 640],
];

/**
 * Dynamically generate tests for a range of common viewports sizes.
 *
 * The current size is passed to the fn.
 *
 * @param title {String}
 * @param fn {Function}
 */
export default function (title, fn) {
  for (const size of sizes) {
    describe(`${title} (${size.join("x")})`, () => {
      beforeEach(() => {
        cy.viewport(...size);
      });

      fn(...size);
    });
  }
}
