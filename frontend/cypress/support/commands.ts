Cypress.Commands.add("selectFilter", (inputName, label) => {
  return cy
    .get(`[data-name='${inputName}']`)
    .click()
    .get("[role='option']")
    .contains(label)
    .click();
});
