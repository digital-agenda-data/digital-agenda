import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.visit(
      "/chart-group/key-indicators/charts/2-compare-two-indicators-using-country-bubbles-siz"
    ).checkChart({
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
    });
  });
});