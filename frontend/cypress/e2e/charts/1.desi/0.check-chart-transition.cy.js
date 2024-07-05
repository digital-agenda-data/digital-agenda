import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check chart navigation", () => {
  it("Check charts", () => {
    cy.checkNavigateBetweenCharts("DESI 2023 dashboard", [
      "DESI 2023 indicators",
      "Compare countries progress",
      "Compare two indicators",
    ]);
  });
});
