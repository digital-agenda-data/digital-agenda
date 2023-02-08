Cypress.Commands.add("selectFilter", (inputName, label) => {
  return cy
    .get(`[data-name='${inputName}']`)
    .click()
    .get(`[data-name='${inputName}'] [role='option']`)
    .contains(label)
    .click();
});

Cypress.Commands.add("searchIndicators", (searchQuery) => {
  cy.visit("/")
    .window()
    .then((remoteWindow) => {
      if (remoteWindow.innerWidth < 996) {
        // Search input is hidden on mobile, and needs to be toggled
        cy.get(".ecl-site-header__search-toggle").click();
      }
    });

  cy.get("form.ecl-search-form input[type=search]")
    .type(searchQuery)
    .get("form.ecl-search-form [type=submit]")
    .click()
    .get("h1")
    .contains("Search results for");
});

Cypress.Commands.add(
  "checkChart",
  (
    chartGroup,
    chart,
    { filters = {}, title = [], point = null, tooltip = [] }
  ) => {
    cy.visit("/")
      .get(".ecl-list-illustration a")
      .contains(chartGroup)
      .click()
      .get(".ecl-list-illustration a")
      .contains(chart)
      .click();

    for (const filtersKey in filters) {
      cy.selectFilter(filtersKey, filters[filtersKey]);
    }

    cy.get(".highcharts-title, .highcharts-subtitle")
      .invoke("text")
      .then((text) => {
        for (const txt of title) {
          // Highcharts adds ZeroWidthSpaces in the text, so we can't
          // check normally
          expect(text.replace(/[\u200B-\u200D\uFEFF]/g, " ")).to.contain(txt);
        }
      });

    if (point) {
      cy.get(`.highcharts-point[aria-label='${point}']`)
        .should("be.visible")
        .trigger("mouseover", { force: true });

      for (const txt of tooltip) {
        cy.get(".highcharts-tooltip").should("contain", txt);
      }
    }

    return cy;
  }
);
