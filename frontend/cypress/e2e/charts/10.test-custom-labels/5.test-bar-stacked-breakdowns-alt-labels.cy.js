import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Custom Labels",
      "Test Bar Stacked Breakdowns Alt Labels",
    );
    cy.checkChart({
      filters: {
        indicator: "Households with a broadband connection",
        breakdownGroup: "Dependent childrens",
        period: 2012,
        unit: "% of households",
      },
      title: ["Households with a broadband connection", "2012"],
      xAxis: ["European Union", "Romania", "Greece"],
      yAxisTitle: ["% of households"],
      point: "European Union, 85.45. with dependent childrens.",
      tooltip: [
        "European Union",
        "with dependent children",
        "85.45% of households",
        "Period: 2012",
      ],
      legend: ["with dependent childrens", "without dependent childrens"],
      definitions: [
        "Indicator: Households having a broadband connection",
        "Breakdown: Household with dependent children",
        "Breakdown: Household without dependent children",
        "Definition: dependent childrens are under 16",
        "Unit of measure: Percentage of households",
        "Definition: Households with at least one member aged 16-74",
      ],
    });
  });
});
