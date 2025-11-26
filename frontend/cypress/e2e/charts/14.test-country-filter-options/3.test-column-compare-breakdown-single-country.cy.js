import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Country Filter Options",
      "Test Column Compare Breakdown Single Country",
    );
    cy.checkChart({
      filters: {
        indicator: "ICT graduates",
        breakdownGroup: "Gender",
        period: "2019",
        unit: "% of graduates",
      },
      title: ["ICT graduates", "Year: 2019"],
      point: "European Union, 0.8. Females.",
      tooltip: ["European Union", "Females", "0.80% of graduates"],
      definitions: [
        "Indicator: ICT graduates",
        "Definition: Individuals with a degree in ICT",
        "Breakdown: Females, Males",
        "Unit of measure: Percentage of graduates",
      ],
    });
  });
});
