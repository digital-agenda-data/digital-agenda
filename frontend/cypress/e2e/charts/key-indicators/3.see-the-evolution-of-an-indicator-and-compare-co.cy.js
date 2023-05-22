import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Key Indicators",
      "See the evolution of an indicator and compare countries"
    );
    cy.checkChart({
      filters: {
        indicator: "ICT graduates",
        breakdown: "Females",
        unit: "% of graduates",
      },
      title: ["ICT graduates, Females"],
      point: "Year: 2019, 0.8. European Union.",
      definitions: [
        "Indicator: ICT graduates",
        "Definition: Individuals with a degree in ICT",
        "Breakdown: Females",
        "Unit of measure: Percentage of graduates",
      ],
    });
  });
});
