import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check chart navigation", () => {
  it("Check charts", () => {
    cy.checkNavigateBetweenCharts(
      "Digital Economy and Society Index (until 2022)",
      [
        "DESI 2022 composite index",
        "DESI 2022 by components",
        "DESI 2022 - Compare the evolution of DESI components",
        "DESI 2022 - Compare countries progress",
        "DESI 2022 - Compare two indicators",
      ],
    );
  });
});
