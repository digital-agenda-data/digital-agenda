import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("DESI 2023 dashboard", "Compare two indicators");
    cy.checkChart({
      filters: {
        indicatorX: "e-Government users",
        breakdownX: "All individuals",
        unitX: "% of internet users (last 12 months)",
        periodX: "DESI period: 2023",
        indicatorY: "Access to e-health records",
        breakdownY: "All Life Events",
        unitY: "Score (0 to 100)",
        periodY: "DESI period: 2023",
      },
      xAxisTitle: [
        "e-Government users",
        "All Individuals",
        "Percentage of individuals who used Internet within the last 12 months",
        "DESI period: 2023 (data from 2022)",
      ],
      yAxisTitle: [
        "Access to e-health records",
        "All Life Events",
        "Score (0 to 100)",
        "DESI period: 2023 (data from 2022)",
      ],
      point: "European Union (EU), 71.705804. European Union (EU).",
      definitions: [
        "(X) Indicator: e-Government users",
        "(X) Breakdown: All Individuals (aged 16-74)",
        "(X) Unit of measure: Percentage of individuals who used Internet within the last 12 months",
        "(Y) Indicator: Access to e-health records",
        "(Y) Breakdown: All Life Events",
        "(Y) Unit of measure: Score (0 to 100)",
      ],
    });
  });
});
