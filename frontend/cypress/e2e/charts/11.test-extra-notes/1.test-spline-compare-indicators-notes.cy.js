import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Extra Notes",
      "Test Spline Compare Indicators Notes",
    );
    cy.checkChart({
      filters: {
        indicatorY: "Access to e-health records",
      },
      point: "DESI period: 2018 (data from 2017), 58.3384. e-Government users.",
      tooltip: [
        "e-Government users",
        "58.34% of internet users (last 12 months)",
        "DESI period: 2018 (data from 2017)",
      ],
      xAxis: ["DESI period: 2018"],
    });
  });
  it("Check Chart Hidden Points from extra notes", () => {
    cy.navigateToChart(
      "Test Extra Notes",
      "Test Spline Compare Indicators Notes",
    );
    cy.checkChart({
      filters: {
        indicatorX: "e-Invoices",
        indicatorY: "Access to e-health records",
      },
      point: "DESI period: 2019 (data from 2018), 24.7944. e-Invoices.",
      // 3 points from e-Invoices instead of 5 (because 2 are hidden via extra notes)
      // 1 point from Access to e-health records
      pointNr: 4,
      tooltip: [
        "e-Invoices",
        "24.79% of enterprises",
        "DESI period: 2019 (data from 2018)",
      ],
    });
  });
});
