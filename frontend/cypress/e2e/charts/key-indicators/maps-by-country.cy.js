import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.visit("/chart-group/key-indicators/charts/2-maps-by-country").checkChart(
      {
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
      }
    );
  });
});
