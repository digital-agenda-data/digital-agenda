describe("Check data file import", () => {
  it("Create and run data file import", () => {
    cy.login();
    // Navigate to the data file import page
    cy.get("a").contains("Upload data from file").click();
    cy.get("a").contains("Add Upload data from file").click();
    // Add a new data file import
    cy.get("input[type=file]").selectFile(
      "cypress/fixtures/import_file_valid.xlsx"
    );
    cy.get("textarea[name=description]").type("Test file import");
    cy.get("input[type=submit][value=Save]").click();
    // Wait for the task to finish
    cy.get("a").contains("Upload file results").click();
    cy.get("tbody tr:first-child td.field-status_display").contains("SUCCESS", {
      timeout: 10000,
    });
    // Navigate to the import config change form
    cy.get("tbody tr:first-child td.field-import_file_link a").click();
    // Check that only one fact has been imported
    cy.get(".field-num_facts a").contains("1");
    // Delete the import file
    cy.get("a").contains("Delete").click();
    cy.get("input[type=submit]").click();
  });
  it("Create and run invalid data file import", () => {
    cy.login();
    // Navigate to the data file import page
    cy.get("a").contains("Upload data from file").click();
    cy.get("a").contains("Add Upload data from file").click();
    // Add a new data file import
    cy.get("input[type=file]").selectFile(
      "cypress/fixtures/import_file_invalid.xlsx"
    );
    cy.get("textarea[name=description]").type("Test file invalid import");
    cy.get("input[type=submit][value=Save]").click();
    // Wait for the task to finish
    cy.get("a").contains("Upload file results").click();
    cy.get("tbody tr:first-child td.field-status_display").contains("FAILURE", {
      timeout: 10000,
    });
    // Navigate to the import config change form
    cy.get("tbody tr:first-child td.field-import_file_link a").click();
    // Check that no fact has been imported
    cy.get(".field-num_facts a").contains("0");
    // Delete the import file
    cy.get("a").contains("Delete").click();
    cy.get("input[type=submit]").click();
  });
  it("Create and run invalid data file import duplicate", () => {
    cy.login();
    // Navigate to the data file import page
    cy.get("a").contains("Upload data from file").click();
    cy.get("a").contains("Add Upload data from file").click();
    // Add a new data file import
    cy.get("input[type=file]").selectFile(
      "cypress/fixtures/import_file_invalid_duplicate.xlsx"
    );
    cy.get("textarea[name=description]").type("Test file invalid import");
    cy.get("input[type=submit][value=Save]").click();
    // Wait for the task to finish
    cy.get("a").contains("Upload file results").click();
    cy.get("tbody tr:first-child td.field-status_display").contains("FAILURE", {
      timeout: 10000,
    });
    // Navigate to the import config change form
    cy.get("tbody tr:first-child td.field-import_file_link a").click();
    // Check that no fact has been imported
    cy.get(".field-num_facts a").contains("0");
    // Delete the import file
    cy.get("a").contains("Delete").click();
    cy.get("input[type=submit]").click();
  });
});
