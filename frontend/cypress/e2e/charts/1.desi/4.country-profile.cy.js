import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Table", () => {
    cy.navigateToChart(
      "Digital Economy and Society Indicators",
      "Country profile",
    );
    cy.selectFilter("period", "DESI 2026");
    cy.selectFilter("country", "Romania");

    // Only some indicators should appear in the chart
    cy.get('.highcharts-series[aria-label^="Romania"] path').should(
      "have.length",
      24,
    );
    // Only some indicators have targets
    cy.get('.highcharts-series[aria-label^="EU 2030 Target"] path').should(
      "have.length",
      12,
    );
    // Check indicator group slices
    cy.get('.highcharts-series[aria-label^="Indicator Group"] path').should(
      "have.length",
      6,
    );
    // Check legend only contains the 4 main groups
    cy.get(".highcharts-a11y-proxy-group-legend li").should("have.length", 4);
    // ALL indicators should appear in the table
    cy.get("table tbody tr").should("have.length", 28);
    // Check that non-DD KPI indicators appear in the table
    cy.get("table tbody tr").contains("Use of generative AI");
  });
  it("Check DD KPI Table", () => {
    cy.navigateToChart(
      "Digital Economy and Society Indicators",
      "Country profile",
    );
    cy.selectFilter("period", "DESI 2026");
    cy.selectFilter("country", "Romania");
    // Filter by DD KPI
    cy.get("label").contains("Digital Decade KPIs").click();

    // Only some indicators should appear in the chart
    cy.get('.highcharts-series[aria-label^="Romania"] path').should(
      "have.length",
      12,
    );
    // ALL DD KPI indicators should have targets
    cy.get('.highcharts-series[aria-label^="EU 2030 Target"] path').should(
      "have.length",
      12,
    );
    // Check indicator group slices
    cy.get('.highcharts-series[aria-label^="Indicator Group"] path').should(
      "have.length",
      4,
    );
    // Check legend only contains the 4 main groups
    cy.get(".highcharts-a11y-proxy-group-legend li").should("have.length", 4);
    // ALL indicators should appear in the table
    cy.get("table tbody tr").should("have.length", 14);
    // Check that non-DD KPI indicators should not appear in the table
    cy.get("table tbody tr")
      .contains("Use of generative AI")
      .should("not.exist");
  });
  it("Check Chart", () => {
    cy.navigateToChart(
      "Digital Economy and Society Indicators",
      "Country profile",
    );
    cy.checkChart({
      filters: {
        country: "Romania",
        period: "DESI 2026",
      },
      title: ["Romania", "DESI period: 2026"],
      point: "At least basic digital skills, 100. Invisible.",
      tooltip: [
        "At least basic digital skills",
        "Romania",
        "31.84% of individuals",
        "EU 2030 Target",
        "80.00% of individuals",
        "EU Average",
        "60.39% of individuals",
        "Reference period: 2025",
      ],
    });
  });
});
