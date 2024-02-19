import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Test Chart Group", "Test Spline Custom Year Range");
    cy.checkChart({
      filters: {
        indicator: "Enterprises with a fixed broadband connection",
        breakdown: "Total",
        unit: "% of enterprises",
      },
      point: "Year: 2022, 0.5. European Union.",
      xAxis: ["2020", "2022", "2024"],
    });
  });
});
