import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart(
      "Key Indicators",
      "See the evolution of an indicator and compare breakdowns",
    );

    const txt = "Test metadata";

    cy.selectFilter("indicator", "ICT graduates");
    cy.selectFilter("breakdownGroup", "Total");
    cy.selectFilter("unit", "% of graduates");
    cy.selectFilter("country", "European Union");
    cy.get(".chart-definitions").contains(txt);

    // Fiddle with the filter and check the metadata disappears when the
    // required conditions are not met, and then reappears when they are.
    cy.selectFilter("country", "Romania");
    cy.get(".chart-definitions").should("not.contain", txt);

    cy.selectFilter("country", "European Union");
    cy.get(".chart-definitions").contains(txt);

    cy.selectFilter("breakdownGroup", "Gender");
    cy.get(".chart-definitions").should("not.contain", txt);

    cy.selectFilter("breakdownGroup", "Total");
    cy.get(".chart-definitions").contains(txt);

    cy.selectFilter(
      "indicator",
      "Enterprises with a fixed broadband connection",
    );
    cy.get(".chart-definitions").should("not.contain", txt);
  });
});
