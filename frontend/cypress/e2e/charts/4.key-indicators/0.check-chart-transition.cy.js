import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check chart navigation", () => {
  it("Check charts", () => {
    cy.checkNavigateBetweenCharts("Key Indicators", [
      "Analyse one indicator and compare countries",
      "Analyse one indicator and compare breakdowns",
      "See the evolution of an indicator and compare countries",
      "See the evolution of an indicator and compare breakdowns",
      "Maps by country",
      "Compare two indicators",
      "Compare two indicators, using country bubbles sized on a third one",
      "Compare the evolution of two indicators",
    ]);
  });
});
