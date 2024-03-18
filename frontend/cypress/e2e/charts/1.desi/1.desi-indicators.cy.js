import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("DESI 2023 dashboard", "DESI 2023 indicators");
    cy.checkChart({
      filters: {
        indicator: "e-Government users",
        breakdown: "All individuals",
        period: "DESI period: 2023",
        unit: "% of internet users (last 12 months)",
      },
      title: [
        "e-Government users",
        "All Individuals",
        "(aged 16-74)",
        // Check for the extra note
        "DESI period: 2023 (data from 2022)",
      ],
      point: "European Union, 74.2.",
      tooltip: [
        "European Union",
        "All individuals",
        "74.20% of internet users (last 12 months)",
        "DESI period: 2023 (data from 2022)",
      ],
      definitions: [
        "Indicator: e-Government users",
        "Definition: Individuals who used the Internet, in the last 12 months, for interaction with public authorities on websites or on mobile applications",
        "Breakdown: All Individuals (aged 16-74)",
        "Unit of measure: Percentage of individuals who used Internet within the last 12 months",
      ],
    });
  });
});
