import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.visit(
      "/chart-group/key-indicators/charts/2-see-the-evolution-of-an-indicator-and-compare-co"
    ).checkChart({
      filters: {
        indicatorGroup: "Digital Skills",
        indicator: "ICT graduates",
        breakdown: "Females",
        unit: "% of graduates",
      },
      title: ["ICT graduates, Females"],
      point: "2019, 0.8. European Union.",
      // tooltip: ["European Union", "Females", "0.8% of graduates"],
    });
  });
});
