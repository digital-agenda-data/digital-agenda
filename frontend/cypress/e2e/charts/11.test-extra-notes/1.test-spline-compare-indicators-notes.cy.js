import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Extra Notes",
      "Test Spline Compare Indicators Notes",
    );
    cy.checkChart({
      filters: {
        indicatorY: "e-Government users",
      },
      point:
        "DESI period: 2023 (data from 2022), 71.705804. Access to e-health records.",
      tooltip: [
        "Access to e-health records",
        "71.71 Score (0 to 100)",
        "DESI period: 2023 (data from 2022)",
      ],
      xAxis: ["DESI period: 2023"],
    });
  });
});
