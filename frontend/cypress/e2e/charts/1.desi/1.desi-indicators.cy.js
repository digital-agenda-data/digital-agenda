import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Digital Economy and Society Indicators",
      "Digital Economy and Society Indicators",
    );
    cy.checkChart({
      filters: {
        period: "DESI 2023",
        indicator: "e-Government users (until 2021)",
        breakdown: "All individuals",
        unit: "% of internet users (last 12 months)",
      },
      title: [
        "e-Government users (until 2021)",
        "All Individuals",
        "(aged 16-74)",
        "DESI period: 2023",
        // Check for the extra note
        "(data from 2022)",
      ],
      point: "European Union, 74.2.",
      tooltip: [
        "European Union",
        "All individuals",
        "74.20% of internet users (last 12 months)",
        "DESI 2023",
        "(data from 2022)",
      ],
      definitions: [
        "Indicator: e-Government users (until 2021)",
        "Definition: Individuals who used the Internet, in the last 12 months, for interaction with public authorities.",
        "Breakdown: All Individuals (aged 16-74)",
        "Unit of measure: Percentage of individuals who used Internet within the last 12 months",
      ],
    });
  });
});
