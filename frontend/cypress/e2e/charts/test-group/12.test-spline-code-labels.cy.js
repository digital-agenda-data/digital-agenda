import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Test Chart Group", "Test Spline Code Labels");
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
      title: ["ict_grad, f and ict_grad, m", "EU"],
      point: "2019, 0.8. ict_grad.",
      legend: ["ict_grad", "ict_grad"],
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
