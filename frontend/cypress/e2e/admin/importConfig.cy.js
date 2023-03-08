describe("Check import configuration", () => {
  it("Create and run import config", () => {
    cy.login()
      // Navigate to the import config page
      .get("a")
      .contains("Import configs")
      .click()
      .get("a")
      .contains("Add import config")
      .click()
      // Add a new import config with filters set to only import a single Fact
      .get("input[name=code]")
      .type("isoc_bde15b_h")
      .get("input[name=title]")
      .type("Test import config")
      .get("input[name=indicator]")
      .type("indic_is")
      .get("input[name=breakdown]")
      .type("hhtyp")
      .get("input[name=period_start]")
      .type("2019")
      .get("input[name=period_end]")
      .type("2019")
      .get("#id_filters textarea.ace_text-input")
      .clear({ force: true })
      .type(
        '{"hhtyp": ["total"], "indic_is": ["h_broad"], "unit": ["pc_hh"], "geo": ["EU27_2020"]}',
        {
          force: true,
          parseSpecialCharSequences: false,
        }
      )
      .get("input[type=submit][value=Save]")
      .click()
      // Trigger an import task
      .get("td.action-checkbox input[type=checkbox]")
      .first()
      .click()
      .get("select[name=action]")
      .select("Trigger import for selected configs")
      .get("button[type=submit]")
      .contains("Go")
      .click()
      // Wait for the task to finish
      .get("tbody tr:first-child td.field-status_display")
      .contains("SUCCESS")
      // Navigate to the import config change form
      .get("tbody tr:first-child td.field-import_config_link a")
      .click()
      // Check that only one fact has been imported
      .get(".field-num_facts a")
      .contains("1")
      // Delete the import config
      .get("a")
      .contains("Delete")
      .click()
      .get("input[type=submit]")
      .click();
  });
});
