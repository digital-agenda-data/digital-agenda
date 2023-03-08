describe("Check data file import", () => {
  it("Create and run data file import", () => {
    cy.login()
      // Navigate to the data file import page
      .get("a")
      .contains("Data file imports")
      .click()
      .get("a")
      .contains("Add data file import")
      .click()
      // Add a new data file import
      .get("input[type=file]")
      .selectFile("cypress/fixtures/import_file_valid.xlsx")
      .get("textarea[name=description]")
      .type("Test file import")
      .get("input[type=submit][value=Save]")
      .click()
      // Wait for the task to finish
      .get("a")
      .contains("Data file import tasks")
      .click()
      .get("tbody tr:first-child td.field-status_display")
      .contains("SUCCESS", { timeout: 10000 })
      // Navigate to the import config change form
      .get("tbody tr:first-child td.field-import_file_link a")
      .click()
      // Check that only one fact has been imported
      .get(".field-num_facts a")
      .contains("1")
      // Delete the import file
      .get("a")
      .contains("Delete")
      .click()
      .get("input[type=submit]")
      .click();
  });
  it("Create and run invalid data file import", () => {
    cy.login()
      // Navigate to the data file import page
      .get("a")
      .contains("Data file imports")
      .click()
      .get("a")
      .contains("Add data file import")
      .click()
      // Add a new data file import
      .get("input[type=file]")
      .selectFile("cypress/fixtures/import_file_invalid.xlsx")
      .get("textarea[name=description]")
      .type("Test file invalid import")
      .get("input[type=submit][value=Save]")
      .click()
      // Wait for the task to finish
      .get("a")
      .contains("Data file import tasks")
      .click()
      .get("tbody tr:first-child td.field-status_display")
      .contains("FAILURE", { timeout: 10000 })
      // Navigate to the import config change form
      .get("tbody tr:first-child td.field-import_file_link a")
      .click()
      // Check that only one fact has been imported
      .get(".field-num_facts a")
      .contains("0")
      // Delete the import file
      .get("a")
      .contains("Delete")
      .click()
      .get("input[type=submit]")
      .click();
  });
});
