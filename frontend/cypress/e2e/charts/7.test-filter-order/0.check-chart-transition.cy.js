import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check chart navigation", () => {
  it("Check charts", () => {
    cy.checkNavigateBetweenCharts("Test Filter Order", [
      "Test Chart Period First",
      "Test Chart Filters Reversed",
      "Test Scatter Unit First",
      "Test Bubble Breakdown First",
      "Test Spline Country First",
    ]);
  });
});
