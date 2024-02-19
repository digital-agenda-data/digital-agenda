import describeResponsive from "../support/describeResponsive";

describeResponsive("Check Search Page", () => {
  it("Check search page period first link", () => {
    cy.searchIndicators("h_broad");
    cy.get("table tr:nth-child(2) a").contains("Test Chart Group");
    cy.get("table tr:nth-child(2) a").contains("h_broad").click();
    cy.checkChartInstance({
      filters: {
        period: "2013",
        indicator: "Households with a broadband connection",
        unit: "% of households",
      },
      title: ["Households having a broadband connection", "Year: 2013"],
      definitions: [
        "Indicator: Households having a broadband connection",
        "Unit of measure: Percentage of households",
      ],
    });
  });
  it("Check search results and links", () => {
    cy.searchIndicators("Social Media");
    cy.get(".ecl-table tbody tr").should("have.length", 3);
    cy.get("[data-ecl-table-header=Indicator] a").eq(0).click();
    cy.get("h1").contains("DESI 2022 by components").go("back");
    cy.get("[data-ecl-table-header=Dataset] a").eq(0).click();
    cy.get("h1").contains("Digital Economy and Society Index");
  });
  it("Check search page pagination", () => {
    cy.searchIndicators("enterprise");
    cy.get(".ecl-pagination li [aria-current=true]").contains("1");
    cy.get(".ecl-pagination li").contains("Previous").should("not.be.visible");
    cy.get(".ecl-pagination li").contains("Next").should("be.visible").click();
    cy.get(".ecl-pagination li [aria-current=true]").contains("2");
    cy.get(".ecl-pagination li")
      .contains("Previous")
      .should("be.visible")
      .click();
    cy.get(".ecl-pagination li [aria-current=true]").contains("1");
  });
  it("Check search page highlight", () => {
    cy.searchIndicators("connect");
    // Check for highlight in the label of the indicator (which is a link)
    cy.get(".ecl-table tbody td a b")
      .contains("connection")
      .should("be.visible");
    // Check for highlight in the definition of the indicator
    cy.get(".ecl-table tbody td b")
      .contains("connections")
      .should("be.visible");
  });
});
