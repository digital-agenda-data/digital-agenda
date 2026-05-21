import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Custom Breakdown Options",
      "Test Spline Compare Breakdowns",
    );
    // Check data labels
    cy.get(".highcharts-data-label").contains("23.53");
    cy.checkChart({
      filters: {},
      title: [
        "playing or downloading games, images, films or music",
        "European Union",
      ],
      point: "Year: 2010, 23.53. Non-nationals.",
      tooltip: ["Non-nationals", "23.53% of individuals"],
    });
  });
});
