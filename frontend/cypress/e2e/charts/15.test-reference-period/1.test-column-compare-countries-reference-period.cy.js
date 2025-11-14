import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Reference Period",
      "Test Column Compare Countries Reference Period",
    );
    cy.checkChartInstance({
      filters: {
        indicator: "Enterprises with a fixed broadband connection",
        breakdown: "Total",
        period: "2022",
        unit: "% of enterprises",
        country: ["European Union"],
      },
      title: ["Enterprises having a fixed broadband connection", "Total"],
      point: "European Union, 0.5.",
      tooltip: [
        "European Union",
        "0.50% of enterprises",
        "Period: 2022",
        "Reference period: 2020",
      ],
    });
    cy.get("a")
      .contains(
        "Consult the list of available indicators, their definition and sources",
      )
      .click();
    // Time coverage should use the reference period instead of the regular period
    cy.get("td").contains("Time coverage: 2020");
  });
});
