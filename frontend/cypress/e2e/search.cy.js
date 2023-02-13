import describeResponsive from "../support/describeResponsive";

describeResponsive("Check Search Page", () => {
  it("Check search results and links", () => {
    cy.searchIndicators("Social Media")
      .get(".ecl-table tbody tr")
      .should("have.length", 3)
      .get("[data-ecl-table-header=Indicator] a")
      .eq(0)
      .click()
      .get("h1")
      .contains("DESI by components")
      .go("back")
      .get("[data-ecl-table-header=Dataset] a")
      .eq(0)
      .click()
      .get("h1")
      .contains("Digital Economy and Society Index");
  });
  it("Check search page pagination", () => {
    cy.searchIndicators("enterprise")
      .get(".ecl-pagination li [aria-current=true]")
      .contains("1")
      .get(".ecl-pagination li")
      .contains("Previous")
      .should("not.be.visible")
      .get(".ecl-pagination li")
      .contains("Next")
      .should("be.visible")
      .click()
      .get(".ecl-pagination li [aria-current=true]")
      .contains("2")
      .get(".ecl-pagination li")
      .contains("Previous")
      .should("be.visible")
      .click()
      .get(".ecl-pagination li [aria-current=true]")
      .contains("1");
  });
  it("Check search page highlight", () => {
    cy.searchIndicators("connect")
      // Check for highlight in the label of the indicator (which is a link)
      .get(".ecl-table tbody td a b")
      .contains("connection")
      .should("be.visible")
      // Check for highlight in the definition of the indicator
      .get(".ecl-table tbody td b")
      .contains("connections")
      .should("be.visible");
  });
});
