import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Key Indicators",
      "Analyse one indicator and compare countries",
    );
    cy.checkChart({
      filters: {
        indicator: "Enterprises with a fixed broadband connection",
        breakdown: "Total",
        period: "2022",
        unit: "% of enterprises",
      },
      title: [
        "Enterprises having a fixed broadband connection, Total",
        "Year: 2022",
      ],
      point: "European Union, 0.5.",
      tooltip: [
        "European Union",
        "Total",
        "0.50% of enterprises",
        "This data point is for the EU",
      ],
      definitions: [
        "Indicator: Enterprises having a fixed broadband connection",
        "Definition: Fixed broadband connections include DSL, xDSL, cable leased lines, Frame Relay, Metro-Ethernet, PLC-Powerline communications, fixed wireless connections, etc.",
        "Breakdown: Total",
        "Unit of measure: Percentage of enterprises",
      ],
    });
  });
});
