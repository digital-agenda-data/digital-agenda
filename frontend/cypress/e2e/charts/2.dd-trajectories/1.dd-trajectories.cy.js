import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart Points", () => {
    cy.navigateToChart(
      "Digital Decade indicators and trajectories",
      "Digital Decade indicators and trajectories",
    );
    cy.selectFilter("indicator", "5G coverage");
    cy.selectFilter("country", "European Union");
    // Check various points
    cy.checkPoint("Year: 2030, 100. European Union, 2030 target.");
    cy.checkPoint(
      "Year: 2030, 99.999994. European Union, Baseline trajectory.",
    );
    cy.checkPoint("Year: 2022, 81.2. European Union, Historical data.");
    cy.checkPoint(
      "Year: 2021, 39.192169. European Union, Baseline trajectory.",
    );
    // Check dash style is changed
    cy.get(".highcharts-series.highcharts-series-1 path.highcharts-graph")
      .invoke("attr", "stroke-dasharray")
      .should("not.contain", "none");
    // Check image is used for target point
    cy.get(
      'image[aria-label="Year: 2030, 100. European Union, 2030 target."]',
    ).should("be.visible");
    // Check image is used for target legend
    cy.get(".highcharts-legend-item.highcharts-series-0").contains(
      "2030 target",
    );
    cy.get(".highcharts-legend-item.highcharts-series-0 image").should(
      "be.visible",
    );
  });
  it("Check Chart", () => {
    cy.navigateToChart(
      "Digital Decade indicators and trajectories",
      "Digital Decade indicators and trajectories",
    );
    cy.checkChart({
      filters: {
        indicator: "5G coverage",
        country: "European Union",
      },
      title: ["5G coverage", "European Union"],
      definitions: [
        "Indicator: 5G coverage",
        "Definition: Percentage of populated areas covered by at least one 5G network regardless of the spectrum band used.",
        "Breakdown: 2030 target, Historical data, Baseline trajectory based on past perfomance",
        "Unit of measure: Percentage of households",
      ],
    });
  });
});
