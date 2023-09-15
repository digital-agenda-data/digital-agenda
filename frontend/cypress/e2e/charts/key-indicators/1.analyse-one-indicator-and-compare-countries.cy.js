import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Key Indicators",
      "Analyse one indicator and compare countries"
    );
    cy.checkChart({
      filters: {
        indicator: "ICT graduates",
        breakdown: "Females",
        period: "2019",
        unit: "% of graduates",
      },
      title: ["ICT graduates, Females", "Year: 2019"],
      point: "European Union, 0.8.",
      tooltip: ["European Union", "Females", "0.80% of graduates"],
      definitions: [
        "Indicator: ICT graduates",
        "Definition: Individuals with a degree in ICT",
        "Breakdown: Females",
        "Unit of measure: Percentage of graduates",
      ],
    });
  });
});
