import describeResponsive from "../support/describeResponsive";

describeResponsive("Check Indicators Page", () => {
  it("Check export links", () => {
    cy.visit("/");
    cy.get(".ecl-list-illustration a")
      .contains("Digital Economy and Society Index")
      .click();
    cy.get("a")
      .contains("Consult the list of indicators, their definition and sources")
      .click();

    // Check exporting data for an indicator group
    cy.get("thead a")
      .contains("data")
      .parent("a")
      .downloadLink()
      .should("contain", "period,country,indicator,breakdown,unit,value,flags");

    // Check exporting values for an indicator group
    for (const label of [
      "indicators",
      "data sources",
      "countries",
      "breakdowns",
      "units",
    ]) {
      cy.get("thead a")
        .contains(label)
        .parent("a")
        .downloadLink()
        .should("contain", "code,label,alt_label,definition");
    }

    // Check exporting values for an indicator
    for (const label of ["countries", "breakdowns", "units"]) {
      cy.get("tbody a")
        .contains(label)
        .parent("a")
        .downloadLink()
        .should("contain", "code,label,alt_label,definition");
    }
  });
  it("Check fields", () => {
    cy.visit("/");
    cy.get(".ecl-list-illustration a").contains("Key Indicators").click();
    cy.get("a")
      .contains("Consult the list of indicators, their definition and sources")
      .click();

    cy.get("thead th").contains("Broadband take-up and coverage");
    cy.get("tbody td").contains("Notation: h_broad");
    cy.get("tbody td").contains(
      "Notes: Scope includes Households with at least one member aged 16-74."
    );
    cy.get("tbody td").contains("Time coverage: 2012-2013");
  });
});
