import describeResponsive from "../support/describeResponsive";

describeResponsive("Check App Navigation", (viewportWidth) => {
  it("Navigate in between charts and groups", () => {
    cy.visit("/");
    cy.get(".ecl-list-illustration a").contains("2. Key Indicators").click();
    cy.get("h1").contains("Key Indicators");
    cy.get(".ecl-list-illustration a")
      .contains("1. Analyse one indicator and compare countries")
      .click();
    cy.get("h1").contains("Analyse one indicator and compare countries");
    cy.get(".ecl-card")
      .contains("Analyse one indicator and compare breakdowns")
      .click();
    cy.get("h1").contains("Analyse one indicator and compare breakdowns");
    cy.get(".ecl-card").contains("Digital Economy and Society Index").click();
    cy.get("h1").contains("Digital Economy and Society Index");
  });
  it("Navigate breadcrumbs", () => {
    cy.visit("/");
    cy.get(".ecl-list-illustration a").contains("2. Key Indicators").click();
    cy.get(".ecl-list-illustration a")
      .contains("1. Analyse one indicator and compare countries")
      .click();
    cy.get(".ecl-breadcrumb a").contains("Key Indicators").click();
    cy.get("h1").contains("Key Indicators");
    cy.get(".ecl-breadcrumb a").contains("Home").click();
    cy.get(".ecl-list-illustration a").contains("2. Key Indicators");
  });
  it("Navigate in between indicator groups", () => {
    cy.visit("/");
    cy.get(".ecl-list-illustration a").contains("2. Key Indicators").click();

    if (viewportWidth >= 996) {
      cy.get(".ecl-category-filter a").contains("Indicators").click();
    } else {
      cy.get(".ecl-tabs a").contains("Indicators").click();
    }

    cy.get("a").contains("Digital Skills").click();
    cy.get(".ecl-table td span")
      .contains("ict_grad")
      .should("be.visible")
      .parents("td")
      .should("contain", "2015 - 2020");

    cy.get("a").contains("ICT graduates").click();
    cy.get("h1").contains("Analyse one indicator and compare countries");
  });
});
