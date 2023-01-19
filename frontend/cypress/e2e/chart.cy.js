describe("Check App Navigation", () => {
  it("Check ColumnCompareCountries", () => {
    cy.visit(
      "/chart-group/key-indicators/charts/2-analyse-one-indicator-and-compare-countries?indicatorGroup=telecom"
    )
      .get("[data-name='indicatorGroup']")
      .click()
      .get("[role='option']")
      .contains("Digital Skills")
      .click()
      .get("[data-name='indicator']")
      .contains("ICT graduates")
      .get("[data-name='breakdown']")
      .contains("Total")
      .get("[data-name='period']")
      .contains("2020")
      .get("[data-name='unit']")
      .contains("% of graduates")
      .get(".highcharts-root")
      .contains("ICT graduates, Total")
      .get(".highcharts-root")
      .contains("Year: 2020");
  });
});
