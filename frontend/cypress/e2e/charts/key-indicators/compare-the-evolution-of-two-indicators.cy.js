import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.visit(
      "/chart-group/key-indicators/charts/2-compare-the-evolution-of-two-indicators"
    ).checkChart({
      filters: {
        indicatorGroupX: "Digital Skills",
        indicatorX: "ICT graduates",
        breakdownX: "Females",
        countryX: "European Union",
        unitX: "% of graduates",
        indicatorGroupY: "Digital Skills",
        indicatorY: "ICT graduates",
        breakdownY: "Males",
        unitY: "% of graduates",
      },
      title: ["ICT graduates, Females and ICT graduates, Males"],
      point: "2019, 0.8. ICT graduates.",
    });
  });
});