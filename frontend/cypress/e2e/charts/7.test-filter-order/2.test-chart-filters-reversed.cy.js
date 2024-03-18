import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Test Filter Order", "Test Chart Filters Reversed");
    cy.checkChart({
      filters: {
        unit: "% of graduates",
        period: "2019",
        breakdownGroup: "Gender",
        indicator: "ICT graduates",
      },
      title: ["ICT graduates", "Year: 2019"],
      point: "European Union, 0.8. Females.",
      tooltip: ["European Union", "Females", "0.80% of graduates"],
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
