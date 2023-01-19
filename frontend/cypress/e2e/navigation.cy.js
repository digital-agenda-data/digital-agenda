describe("Check App Navigation", () => {
  it("Navigate in between charts and groups", () => {
    cy.visit("/")
      .get(".ecl-list-illustration__item")
      .contains("2. Key Indicators")
      .click()
      .get(".ecl-page-header__title")
      .contains("Key Indicators")
      .get(".ecl-list-illustration__item")
      .contains("1. Analyse one indicator and compare countries")
      .click()
      .get(".ecl-page-header__title")
      .contains("Analyse one indicator and compare countries")
      .get(".ecl-card")
      .contains("Analyse one indicator and compare breakdowns")
      .click()
      .get(".ecl-page-header__title")
      .contains("Analyse one indicator and compare breakdowns")
      .get(".ecl-card")
      .contains("Digital Economy and Society Index")
      .click()
      .get(".ecl-page-header__title")
      .contains("Digital Economy and Society Index");
  });
  it("Navigate breadcrumbs", () => {
    cy.visit("/")
      .get(".ecl-list-illustration__item")
      .contains("2. Key Indicators")
      .click()
      .get(".ecl-list-illustration__item")
      .contains("1. Analyse one indicator and compare countries")
      .click()
      .get(".ecl-breadcrumb .ecl-link")
      .contains("Charts")
      .click()
      .get(".ecl-page-header__title")
      .contains("Key Indicators")
      .get(".ecl-breadcrumb .ecl-link")
      .contains("Home")
      .click()
      .get(".ecl-list-illustration__item")
      .contains("2. Key Indicators");
  });
  it("Navigate in between indicator groups", () => {
    cy.visit("/")
      .get(".ecl-list-illustration__item")
      .contains("2. Key Indicators")
      .click()
      .get(".ecl-category-filter__list-item")
      .contains("Indicators")
      .click()
      .get(".ecl-link")
      .contains("Digital Skills")
      .click()
      .get(".ecl-table__cell")
      .contains("ict_grad")
      .should("be.visible");
  });
});
