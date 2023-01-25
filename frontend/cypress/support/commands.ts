Cypress.Commands.add("selectFilter", (inputName, label) => {
  return cy
    .get(`[data-name='${inputName}']`)
    .click()
    .get("[role='option']")
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
