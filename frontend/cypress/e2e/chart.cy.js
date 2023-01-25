import describeResponsive from "../describeResponsive";

describeResponsive("Check App Navigation", () => {
  it("Check ColumnCompareCountries", () => {
    cy.visit(
      "/chart-group/key-indicators/charts/2-analyse-one-indicator-and-compare-countries?indicatorGroup=telecom"
    )
      .selectFilter("indicatorGroup", "Digital Skills")
      .selectFilter("indicator", "ICT graduates")
      .selectFilter("breakdown", "Total")
      .selectFilter("period", "2020")
      .selectFilter("unit", "% of graduates")
      .get(".highcharts-root")
      .contains("ICT graduates, Total")
      .get(".highcharts-root")
      .contains("Year: 2020")
      .get(".highcharts-point[aria-label='European Union, 3.9.']")
      .should("be.visible")
      .trigger("mouseover")
      .get(".highcharts-tooltip")
      .should("contain", "European Union")
      .should("contain", "3.9% of graduates");
  });
});
