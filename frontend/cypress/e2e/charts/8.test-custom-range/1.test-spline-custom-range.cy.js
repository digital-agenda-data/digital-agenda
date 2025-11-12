import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Test Custom Range", "Test Spline Custom Ranges");
    cy.checkChart({
      filters: {
        indicatorX: "ICT graduates",
        breakdownX: "Females",
        unitX: "% of graduates",
        countryX: "European Union",
        indicatorY: "ICT graduates",
        breakdownY: "Males",
        unitY: "% of graduates",
      },
      title: ["ICT graduates, Females and ICT graduates, Males"],
      point: "Year: 2019, 0.8. European Union, ICT graduates, Females.",
      definitions: [
        "Indicator: ICT graduates",
        "Breakdown: Females",
        "Unit of measure: Percentage of graduates",
        "Indicator: ICT graduates",
        "Breakdown: Males",
        "Unit of measure: Percentage of graduates",
        "Definition: Individuals with a degree in ICT",
      ],
      xAxis: ["2010", "2030"],
      yAxis: ["-1", "4"],
    });
  });
});
