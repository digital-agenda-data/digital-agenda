import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Extra Notes",
      "Test Spline Compare Countries Notes",
    );
    cy.checkChart({
      // No filters since the chart should have the defaults already set to what we need.
      filters: {},
      title: ["Access to e-health records", "All Life Events"],
      point: "DESI period: 2023 (data from 2022), 71.705804. European Union.",
      tooltip: [
        "All Life Events",
        "71.71 Score (0 to 100)",
        "DESI period: 2023 (data from 2022)",
      ],
      xAxis: ["DESI period: 2023 (data from 2022)"],
      yAxisTitle: ["Score (0 to 100)"],
    });
  });
});
