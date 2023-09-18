import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Key Indicators", "Compare two indicators");
    cy.checkChart({
      filters: {
        indicatorX: "ICT graduates",
        breakdownX: "Females",
        periodX: "2019",
        unitX: "% of graduates",
        indicatorY: "ICT graduates",
        breakdownY: "Males",
        unitY: "% of graduates",
      },
      title: ["Year: 2019"],
      point: "Romania, 4.1. Romania.",
      tooltip: ["Romania", "2.20% of graduates", "4.10% of graduates"],
      definitions: [
        "(X) Indicator: ICT graduates",
        "(X) Breakdown: Females",
        "(X) Unit of measure: Percentage of graduates",
        "(Y) Indicator: ICT graduates",
        "(Y) Breakdown: Males",
        "(Y) Unit of measure: Percentage of graduates",
        "Definition: Individuals with a degree in ICT",
      ],
    });
  });
});
