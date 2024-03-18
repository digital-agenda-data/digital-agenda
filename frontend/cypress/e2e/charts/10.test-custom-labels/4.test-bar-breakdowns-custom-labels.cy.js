import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Custom Labels",
      "Test Bar Breakdowns Custom Labels",
    );
    cy.checkChart({
      filters: {
        indicator: "Households with a broadband connection",
        breakdownGroup: "Dependent childrens",
        period: 2012,
        unit: "% of households",
      },
      title: ["Households having a broadband connection", "Year: 2012"],
      xAxis: ["European Union"],
      yAxisTitle: ["Percentage of households"],
      point: "European Union, 85.45. Household with dependent children.",
      tooltip: [
        "European Union",
        "Household with dependent children",
        "85.45 Percentage of households",
      ],
      legend: [
        "Household with dependent children",
        "Household without dependent children",
      ],
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
