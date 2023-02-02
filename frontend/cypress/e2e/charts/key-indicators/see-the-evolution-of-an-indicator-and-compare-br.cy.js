import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.visit(
      "/chart-group/key-indicators/charts/2-see-the-evolution-of-an-indicator-and-compare-br"
    ).checkChart({
      filters: {
        indicatorGroup: "Digital Skills",
        indicator: "ICT graduates",
        breakdownGroup: "Gender",
        unit: "% of graduates",
        country: "European Union",
      },
      title: ["ICT graduates", "European Union"],
      point: "2019, 0.8. Females.",
      // tooltip: ["European Union", "Females", "0.8% of graduates"],
    });
  });
});
