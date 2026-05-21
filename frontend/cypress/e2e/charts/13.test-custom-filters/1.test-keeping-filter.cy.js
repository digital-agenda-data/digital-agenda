import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Custom Filters",
      "Test Default And Ignore Breakdown Group Total",
    );
    cy.checkChartInstance({
      filters: {
        breakdownGroup: "Total",
        country: "European Union",
        indicator: "ICT graduates",
      },
      title: ["ICT graduates", "European Union"],
      point: "Year: 2015, 3.6. Total.",
    });

    // Click the card to check how filter preservation works for this impossible
    // situation. As the "total" breakdown group is hidden in the other chart.

    cy.get("a")
      .contains("Test Default And Ignore Breakdown Group Gender")
      .click();

    cy.checkChartInstance({
      filters: {
        breakdownGroup: "Gender",
        country: "European Union",
        indicator: "ICT graduates",
      },
      title: ["ICT graduates", "European Union"],
      point: "Year: 2015, 0.7. Females.",
    });
  });
});
