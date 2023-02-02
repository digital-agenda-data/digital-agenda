import describeResponsive from "../describeResponsive";

describeResponsive("Check App Navigation", (viewportWidth) => {
  it("Navigate in between charts and groups", () => {
    cy.visit("/")
      .get(".ecl-list-illustration a")
      .contains("2. Key Indicators")
      .click()
      .get("h1")
      .contains("Key Indicators")
      .get(".ecl-list-illustration a")
      .contains("1. Analyse one indicator and compare countries")
      .click()
      .get("h1")
      .contains("Analyse one indicator and compare countries")
      .get(".ecl-card")
      .contains("Analyse one indicator and compare breakdowns")
      .click()
      .get("h1")
      .contains("Analyse one indicator and compare breakdowns")
      .get(".ecl-card")
      .contains("Digital Economy and Society Index")
      .click()
      .get("h1")
      .contains("Digital Economy and Society Index");
  });
  it("Navigate breadcrumbs", () => {
    cy.visit("/")
      .get(".ecl-list-illustration a")
      .contains("2. Key Indicators")
      .click()
      .get(".ecl-list-illustration a")
      .contains("1. Analyse one indicator and compare countries")
      .click()
      .get(".ecl-breadcrumb a")
      .contains("Charts")
      .click()
      .get("h1")
      .contains("Key Indicators")
      .get(".ecl-breadcrumb a")
      .contains("Home")
      .click()
      .get(".ecl-list-illustration a")
      .contains("2. Key Indicators");
  });
  it("Navigate in between indicator groups", () => {
    cy.visit("/")
      .get(".ecl-list-illustration a")
      .contains("2. Key Indicators")
      .click();

    if (viewportWidth >= 996) {
      cy.get(".ecl-category-filter a").contains("Indicators").click();
    } else {
      cy.get(".ecl-tabs a").contains("Indicators").click();
    }

    cy.get("a")
      .contains("Digital Skills")
      .click()
      .get(".ecl-table td span")
      .contains("ict_grad")
      .should("be.visible")
      .parents("td")
      .should("contain", "2015 - 2020");
  });
});
