import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Test Filter Order", "Test Bubble Breakdown First");
    cy.checkChart({
      filters: {
        breakdownX: "Females",
        indicatorX: "ICT graduates",
        unitX: "% of graduates",
        periodX: "2019",
        breakdownY: "Males",
        indicatorY: "ICT graduates",
        unitY: "% of graduates",
        periodY: "2019",
        breakdownZ: "Total",
        indicatorZ: "ICT graduates",
        unitZ: "% of graduates",
        periodZ: "2019",
      },
      point: "Romania (RO), y: 4.1, z: 6.3. Romania (RO).",
      tooltip: [
        "Romania (RO)",
        "2.20% of graduates",
        "4.10% of graduates",
        "6.30% of graduates",
      ],
      definitions: [
        "(X) Indicator: ICT graduates",
        "(X) Breakdown: Females",
        "(X) Unit of measure: Percentage of graduates",
        "(Y) Indicator: ICT graduates",
        "(Y) Breakdown: Males",
        "(Y) Unit of measure: Percentage of graduates",
        "(Z) Indicator: ICT graduates",
        "(Z) Breakdown: Total",
        "(Z) Unit of measure: Percentage of graduates",
        "Definition: Individuals with a degree in ICT",
      ],
    });
  });
});
