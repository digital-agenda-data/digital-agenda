import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Key Indicators",
      "See the evolution of an indicator and compare breakdowns"
    );
    cy.checkChart({
      filters: {
        indicator: "ICT graduates",
        breakdownGroup: "Gender",
        unit: "% of graduates",
        country: "European Union",
      },
      title: ["ICT graduates", "European Union"],
      point: "Year: 2019, 0.8. Females.",
      definitions: [
        "Indicator: ICT graduates",
        "Definition: Individuals with a degree in ICT",
        "Breakdown: Females",
        "Breakdown: Males",
        "Unit of measure: Percentage of graduates",
      ],
    });
  });
});
