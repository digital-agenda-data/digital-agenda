import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Key Indicators",
      "Compare the evolution of two indicators"
    );
    cy.checkChart({
      filters: {
        indicatorX: "ICT graduates",
        breakdownX: "Females",
        countryX: "European Union",
        unitX: "% of graduates",
        indicatorY: "ICT graduates",
        breakdownY: "Males",
        unitY: "% of graduates",
      },
      title: ["ICT graduates, Females and ICT graduates, Males"],
      point: "2019, 0.8. ICT graduates.",
      definitions: [
        "Indicator: ICT graduates",
        "Breakdown: Females",
        "Unit of measure: Percentage of graduates",
        "Indicator: ICT graduates",
        "Breakdown: Males",
        "Unit of measure: Percentage of graduates",
        "Definition: Individuals with a degree in ICT",
      ],
    });
  });
});
