import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.visit(
      "/chart-group/key-indicators/charts/2-analyse-one-indicator-and-compare-countries"
    ).checkChart({
      filters: {
        indicatorGroup: "Digital Skills",
        indicator: "ICT graduates",
        breakdown: "Females",
        period: "2019",
        unit: "% of graduates",
      },
      title: ["ICT graduates, Females", "Year: 2019"],
      point: "European Union, 0.8.",
      tooltip: ["European Union", "Females", "0.8% of graduates"],
    });
  });
});
