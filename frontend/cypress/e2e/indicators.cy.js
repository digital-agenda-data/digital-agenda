import describeResponsive from "../support/describeResponsive";

describeResponsive("Check Indicators Page", () => {
  it("Check export links", () => {
    cy.visit("/")
      .get(".ecl-list-illustration a")
      .contains("Digital Economy and Society Index")
      .click()
      .get("a")
      .contains("Consult the list of indicators, their definition and sources")
      .click();

    // Check exporting data for an indicator group
    cy.get("thead a")
      .contains("data")
      .parent("a")
      .downloadLink()
      .should("contain", "period,indicator,breakdown,unit,country,value,flags");

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
});
