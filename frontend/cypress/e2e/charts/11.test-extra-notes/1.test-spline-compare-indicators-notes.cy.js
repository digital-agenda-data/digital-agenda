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
});
