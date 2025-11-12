import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Test Custom Breakdown Options",
      "Test Spline Compare Indicators",
    );
    cy.checkChart({
      filters: {
        breakdownX: "Non-nationals",
        breakdownY: "Nationals",
      },
      title: [
        "playing or downloading games, images, films or music",
        "European Union",
      ],
      point:
        "Year: 2010, 23.53. European Union, Games, images, films or music.",
      tooltip: ["Non-nationals", "23.53% of individuals"],
    });
    // Check data labels
    cy.get(".highcharts-data-label").contains("23.53");
  });
});
