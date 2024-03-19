import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Extra Notes",
      "Test Spline Compare Breakdowns Notes",
    );
    cy.checkChart({
      // No filters since the chart should have the defaults already set to what we need.
      filters: {},
      title: ["e-Government users", "European Union"],
      point: "DESI period: 2018 (data from 2017), 58.3384. All individuals.",
      tooltip: [
        "All individuals",
        "58.34% of internet users (last 12 months)",
        "DESI period: 2018 (data from 2017)",
      ],
      xAxis: ["DESI period: 2018 (data from 2017)"],
      yAxisTitle: ["% of internet users (last 12 months)"],
    });
  });
  it("Check Chart Hidden Points from extra notes", () => {
    cy.navigateToChart(
      "Test Extra Notes",
      "Test Spline Compare Breakdowns Notes",
    );
    cy.checkChart({
      filters: {
        indicator: "e-Invoices",
      },
      point: "DESI period: 2019 (data from 2018), 24.7944. All enterprises.",
      // 3 points from e-Invoices instead of 5 (because 2 are hidden via extra notes)
      pointNr: 3,
      tooltip: [
        "All enterprises",
        "24.79% of enterprises",
        "DESI period: 2019 (data from 2018)",
      ],
    });
  });
});
