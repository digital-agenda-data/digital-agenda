import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.checkChart("Key Indicators", "Maps by country", {
      filters: {
        indicatorGroup: "Digital Skills",
        indicator: "ICT graduates",
        breakdown: "Females",
        period: "2019",
        unit: "% of graduates",
      },
      title: ["ICT graduates, Females", "Year: 2019"],
      point: "x, RO, value: 2.2.",
      tooltip: ["Romania", "Females", "2.2% of graduates"],
      definitions: [
        "Indicator: ICT graduates",
        "Definition: Individuals with a degree in ICT",
        "Breakdown: Females",
        "Unit of measure: Percentage of graduates",
      ],
    });
  });
});
