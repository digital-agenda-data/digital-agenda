import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Test Chart Group", "Test Bubble Code Labels");
    cy.checkChart({
      filters: {
        indicatorX: "ICT graduates",
        breakdownX: "Females",
        unitX: "% of graduates",
        periodX: "2019",
        indicatorY: "ICT graduates",
        breakdownY: "Males",
        unitY: "% of graduates",
        periodY: "2019",
        indicatorZ: "ICT graduates",
        breakdownZ: "Total",
        unitZ: "% of graduates",
        periodZ: "2019",
      },
      title: ["Size of bubble (Z): ict_grad, total, pc_grad, 2019"],
      point: "RO (RO), y: 4.1, z: 6.3. RO (RO).",
      tooltip: ["RO (RO)", "2.20 pc_grad", "4.10 pc_grad", "6.30 pc_grad"],
      legend: ["RO (RO)", "EU (EU)"],
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
