import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Test Chart Group", "Test Scatter Unit First");
    cy.checkChart({
      filters: {
        unitX: "% of graduates",
        indicatorX: "ICT graduates",
        breakdownX: "Females",
        periodX: "2019",
        unitY: "% of graduates",
        indicatorY: "ICT graduates",
        breakdownY: "Males",
        periodY: "2019",
      },
      point: "Romania (RO), 4.1. Romania (RO).",
      tooltip: ["Romania (RO)", "2.20% of graduates", "4.10% of graduates"],
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
