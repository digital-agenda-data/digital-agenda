import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Key Indicators",
      "Compare two indicators, using country bubbles sized on a third one"
    );
    cy.checkChart({
      filters: {
        indicatorX: "ICT graduates",
        breakdownX: "Females",
        periodX: "2019",
        unitX: "% of graduates",
        indicatorY: "ICT graduates",
        breakdownY: "Males",
        unitY: "% of graduates",
        indicatorZ: "ICT graduates",
        breakdownZ: "Total",
        unitZ: "% of graduates",
      },
      title: ["Year: 2019"],
      point: "Romania, y: 4.1, z: 6.3. Romania.",
      tooltip: [
        "Romania",
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
