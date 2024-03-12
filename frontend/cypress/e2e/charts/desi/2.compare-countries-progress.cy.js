import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("DESI 2023 dashboard", "Compare countries progress");
    cy.checkChart({
      filters: {
        indicator: "e-Government users",
        breakdown: "All individuals",
        unit: "% of internet users (last 12 months)",
      },
      title: ["e-Government users", "All Individuals", "(aged 16-74)"],
      point: "DESI period: 2023 (data from 2022), 74.2. European Union.",
      definitions: [
        "Indicator: e-Government users",
        "Definition: Individuals who used the Internet, in the last 12 months, for interaction with public authorities on websites or on mobile applications",
        "Breakdown: All Individuals (aged 16-74)",
        "Unit of measure: Percentage of individuals who used Internet within the last 12 months",
      ],
    });
  });
});
