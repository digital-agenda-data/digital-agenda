import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Country Filter Options",
      "Test Spline Compare Breakdowns Multi Country",
    );
    cy.checkChart({
      filters: {
        breakdownGroup: "Gender",
        indicator: "ICT graduates",
        country: ["European Union", "Romania"],
      },
      title: ["ICT graduates", "European Union", "Romania"],
    });
    cy.checkPoint("Year: 2020, 3.1. European Union, Males.");
    cy.checkPoint("Year: 2020, 0.8. European Union, Females.");
    cy.checkPoint("Year: 2020, 4.4. Romania, Males.");
    cy.checkPoint("Year: 2020, 2.3. Romania, Females.");
  });
});
