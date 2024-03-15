import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Test Filter Order", "Test Chart Period First");
    cy.checkChart({
      filters: {
        period: "2019",
        indicator: "ICT graduates",
        breakdown: "Females",
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
