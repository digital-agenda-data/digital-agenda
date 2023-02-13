import describeResponsive from "../support/describeResponsive";

describeResponsive("Check Metadata Page", () => {
  it("Check export links", () => {
    cy.visit("/")
      .get(".ecl-list-illustration a")
      .contains("Digital Economy and Society Index")
      .click()
      .get("a")
      .contains("Entire dataset metadata and download services")
      .click()
      .get("[data-ecl-table-header=Comment] a")
      .each(($el) => {
        if (!$el.text().match(/codelist/)) {
          return;
        }

        cy.request($el.attr("href"))
          .its("body")
          .should("match", /^code,label,alt_label,definition/);
      });

    cy.get("a")
      .contains("Export CSV")
      .parent("a")
      .invoke("attr", "href")
      .then((url) => {
        cy.request(url)
          .its("body")
          .should(
            "match",
            /^period,indicator,breakdown,unit,country,value,flags/
          );
      });
  });
});
