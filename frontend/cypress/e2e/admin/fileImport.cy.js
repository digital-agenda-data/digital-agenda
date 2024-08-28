describe("Check data file import", () => {
  function checkFileImport({
    fixture,
    expectedStatus = "SUCCESS",
    expectedFacts = "1",
  }) {
    cy.login();
    // Navigate to the data file import page
    cy.get("a").contains("Upload data from file").click();
    cy.get("a").contains("Add Upload data from file").click();
    // Add a new data file import
    cy.get("input[type=file]").selectFile(`cypress/fixtures/${fixture}`);
    cy.get("textarea[name=description]").type("Test file import");
    cy.get("input[type=submit][value=Save]").click();
    // Wait for the task to finish
    cy.get("a").contains("Upload file results").click();
    cy.get("tbody tr:first-child td.field-status_display").contains(
      expectedStatus,
      {
        timeout: 10000,
      },
    );
    // Navigate to the import config change form
    cy.get("tbody tr:first-child td.field-import_file_link a").click();
    // Check that only one fact has been imported
    cy.get(".field-num_facts a").contains(expectedFacts);
    // Delete the import file
    cy.get("a").contains("Delete").click();
    cy.get("input[type=submit]").click();
  }

  it("Create and run data file import XLSX", () => {
    checkFileImport({
      fixture: "import_file_valid.xlsx",
    });
  });
  it("Create and run data file import XLS", () => {
    checkFileImport({
      fixture: "import_file_valid.xls",
    });
  });
  it("Create and run data file import with no remarks", () => {
    checkFileImport({
      fixture: "import_file_valid_no_remarks.xlsx",
    });
  });
  it("Create and run invalid data file import", () => {
    checkFileImport({
      fixture: "import_file_invalid.xlsx",
      expectedStatus: "FAILURE",
      expectedFacts: "0",
    });
  });
  it("Create and run invalid data file import duplicate", () => {
    checkFileImport({
      fixture: "import_file_invalid_duplicate.xlsx",
      expectedStatus: "FAILURE",
      expectedFacts: "0",
    });
  });
});
