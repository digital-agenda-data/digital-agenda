import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.checkChart(
      "Key Indicators",
      "Analyse one indicator and compare breakdowns",
      {
        filters: {
          indicator: "ICT graduates",
          breakdownGroup: "Gender",
          period: "2019",
          unit: "% of graduates",
        },
        title: ["ICT graduates", "Year: 2019"],
        point: "European Union, 0.8. Females.",
        tooltip: ["European Union", "Females", "0.8% of graduates"],
        definitions: [
          "Indicator: ICT graduates",
          "Definition: Individuals with a degree in ICT",
          "Breakdown: Females",
          "Breakdown: Males",
          "Unit of measure: Percentage of graduates",
        ],
      }
    );
  });
});
