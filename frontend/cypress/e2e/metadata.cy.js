import describeResponsive from "../support/describeResponsive";

describeResponsive("Check Metadata Page", () => {
  it("Check export links", () => {
    cy.visit("/");
    cy.get(".ecl-list-illustration a")
      .contains("Digital Economy and Society Index")
      .click();
    cy.get("a")
      .contains("Entire dataset metadata and download services")
      .click();

    // Check downloading ALL codelists
    cy.get("[data-ecl-table-header=Comment] a").each(($el) => {
      if (!$el.text().match(/codelist/)) {
        return;
      }
      cy.wrap($el)
        .downloadLink()
        .should("contain", "code,label,alt_label,definition");
    });

    // Check bulk export all data for the chart group
    cy.get("a")
      .contains("Export CSV")
      .parent("a")
      .downloadLink()
      .should("contain", "period,country,indicator,breakdown,unit,value,flags");
  });
});
