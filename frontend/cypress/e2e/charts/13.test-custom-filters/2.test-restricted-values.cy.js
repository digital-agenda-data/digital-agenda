import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Custom Filters",
      "Test Restrict Only Breakdown Group Total",
    );
    cy.checkChartInstance({
      filters: {
        breakdown: "Total",
        indicator: "ICT graduates",
      },
      title: ["ICT graduates", "Total"],
      point: "Year: 2020, 3.9. European Union.",
    });
    // Gender breakdown should not be present
    cy.checkFilterOptions("breakdown", ["Total"]);
    // All other countries should not be present
    cy.checkFilterOptions("country", ["Denmark", "European Union"]);
  });
});
