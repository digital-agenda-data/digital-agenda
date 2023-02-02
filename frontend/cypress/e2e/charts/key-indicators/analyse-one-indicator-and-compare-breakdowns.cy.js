import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.visit(
      "/chart-group/key-indicators/charts/2-analyse-one-indicator-and-compare-breakdowns"
    ).checkChart({
      filters: {
        indicatorGroup: "Digital Skills",
        indicator: "ICT graduates",
        breakdownGroup: "Gender",
        period: "2019",
        unit: "% of graduates",
      },
      title: ["ICT graduates", "Year: 2019"],
      point: "European Union, 0.8. Females.",
      tooltip: ["European Union", "Females", "0.8% of graduates"],
    });
  });
});
