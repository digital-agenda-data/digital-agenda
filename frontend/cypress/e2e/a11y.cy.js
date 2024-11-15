const pages = [
  "/",
  // Captcha is broken, needs to be completely replaced.
  // "/feedback",
  "/search?q=enterprise",
  "/datasets/desi-2022/charts",
  "/datasets/desi-2022/indicators",
  "/datasets/desi-2022/metadata",
  "/datasets/desi-2022/charts/desi-composite",
  "/datasets/desi-2022/charts/desi-components",
  "/datasets/desi-2022/charts/desi-compare-two-indicators",
  "/datasets/desi-2022/charts/desi-compare-countries-progress",
];

function terminalLog(violations) {
  cy.task(
    "log",
    `${violations.length} accessibility violation${
      violations.length === 1 ? "" : "s"
    } ${violations.length === 1 ? "was" : "were"} detected`,
  );
  // pluck specific keys to keep the table readable
  const violationData = violations.map(
    ({ id, impact, description, nodes }) => ({
      id,
      impact,
      description,
      nodes: nodes.length,
    }),
  );

  cy.task("table", violationData);
}

describe("Test accessibility", () => {
  function checkPage(url) {
    cy.visit(url);
    cy.injectAxe();

    // Wait for loading
    cy.get("#header").should("be.visible");
    cy.get("#nav").should("be.visible");
    cy.get("#main").should("be.visible");
    cy.get("#footer").should("be.visible");
    cy.get(".lds-app-loader").should("not.exist");
    cy.waitForNetworkIdle(1000, { log: false });

    cy.checkA11y(null, null, terminalLog);
  }

  for (const page of pages) {
    it(`Check a11y for page: ${page}`, () => {
      checkPage(page);
    });
  }
});
