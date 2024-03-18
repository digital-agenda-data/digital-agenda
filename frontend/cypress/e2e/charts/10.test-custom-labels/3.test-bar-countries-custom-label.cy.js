import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Custom Labels",
      "Test Bar Countries Custom Labels",
    );
    cy.checkChart({
      filters: {
        indicator: "Households with a broadband connection",
        breakdown: "with dependent childrens",
        period: 2012,
        unit: "% of households",
      },
      title: [
        "Households having a broadband connection",
        "Household with dependent children",
        "Year: 2012",
      ],
      xAxis: ["European Union", "Romania"],
      yAxisTitle: ["Percentage of households"],
      point: "European Union, 85.45.",
      tooltip: [
        "European Union",
        "Household with dependent children",
        "85.45 Percentage of households",
      ],
      definitions: [
        "Indicator: Households having a broadband connection",
        "Breakdown: Household with dependent children",
        "Definition: dependent childrens are under 16",
        "Unit of measure: Percentage of households",
        "Definition: Households with at least one member aged 16-74",
      ],
    });
  });
});
