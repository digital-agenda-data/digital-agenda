import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.checkChart(
      "Key Indicators",
      "Compare two indicators, using country bubbles sized on a third one",
      {
        filters: {
          indicatorGroupX: "Digital Skills",
          indicatorX: "ICT graduates",
          breakdownX: "Females",
          periodX: "2019",
          unitX: "% of graduates",
          indicatorGroupY: "Digital Skills",
          indicatorY: "ICT graduates",
          breakdownY: "Males",
          unitY: "% of graduates",
          indicatorGroupZ: "Digital Skills",
          indicatorZ: "ICT graduates",
          breakdownZ: "Total",
          unitZ: "% of graduates",
        },
        title: ["Year: 2019"],
        point: "EU, y: 3.1, z: 3.9. European Union.",
        tooltip: [
          "European Union",
          "0.8% of graduates",
          "3.1% of graduates",
          "3.9% of graduates",
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
      }
    );
  });
});
