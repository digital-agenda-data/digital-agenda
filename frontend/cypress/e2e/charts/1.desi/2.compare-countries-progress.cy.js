import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Digital Economy and Society Indicators",
      "Compare countries progress",
    );
    cy.checkChart({
      filters: {
        indicator: "e-Government users (until 2021)",
        breakdown: "All individuals",
        unit: "% of internet users (last 12 months)",
      },
      title: [
        "e-Government users (until 2021)",
        "All Individuals",
        "(aged 16-74)",
      ],
      point: "DESI 2023 (data from 2022), 74.2. European Union.",
      definitions: [
        "Indicator: e-Government users (until 2021)",
        "Definition: Individuals who used the Internet, in the last 12 months, for interaction with public authorities.",
        "Breakdown: All Individuals (aged 16-74)",
        "Unit of measure: Percentage of individuals who used Internet within the last 12 months",
      ],
    });
  });
});
