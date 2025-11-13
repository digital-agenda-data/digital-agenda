import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Country Filter Options",
      "Test Spline Compare Indicators Multi Country",
    );
    cy.checkChart({
      filters: {
        indicatorX: "ICT graduates",
        breakdownX: "Male",
        indicatorY: "ICT graduates",
        breakdownY: "Female",
        countryX: ["European Union", "Romania"],
      },
      title: ["ICT graduates", "European Union", "Romania"],
    });
    cy.checkPoint("Year: 2020, 3.1. European Union, ICT graduates, Males.");
    cy.checkPoint("Year: 2020, 0.8. European Union, ICT graduates, Females.");
    cy.checkPoint("Year: 2020, 4.4. Romania, ICT graduates, Males.");
    cy.checkPoint("Year: 2020, 2.3. Romania, ICT graduates, Females.");
  });
});
