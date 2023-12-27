describe("Check import configuration", () => {
  it("Create and run import config", () => {
    cy.login();
    // Navigate to the import config page
    cy.get("a").contains("Import configs").click();
    cy.get("a").contains("Add import config").click();
    // Add a new import config with filters set to only import a single Fact
    cy.get("input[name=code]").type("isoc_ci_it_h");
    cy.get("input[name=title]").type("Test import config");
    cy.get("input[name=indicator]").type("indic_is");
    cy.get("input[name=breakdown]").type("hhtyp");
    cy.get("input[name=period_start]").type("2019");
    cy.get("input[name=period_end]").type("2019");
    cy.get("#id_filters textarea.ace_text-input").clear({ force: true });
    cy.get("#id_filters textarea.ace_text-input").type(
      '{"hhtyp": ["total"], "indic_is": ["h_broad"], "unit": ["pc_hh"], "geo": ["EU27_2020"]}',
      {
        force: true,
        parseSpecialCharSequences: false,
      }
    );
    cy.get("#id_mappings textarea.ace_text-input").clear({ force: true });
    cy.get("#id_mappings textarea.ace_text-input").type(
      '{"breakdown": {"total": "hh_total"}, "country": {"EU27_2020": "EU"}}',
      {
        force: true,
        parseSpecialCharSequences: false,
      }
    );
    cy.get("input[type=submit][value=Save]").click();
    // Trigger an import task
    cy.get("td.action-checkbox input[type=checkbox]").first().click();
    cy.get("select[name=action]").select("Trigger import for selected configs");
    cy.get("button[type=submit]").contains("Go").click();
    // Wait for the task to finish
    cy.get("tbody tr:first-child td.field-status_display").contains("SUCCESS", {
      timeout: 10000,
    });
    // Navigate to the import config change form
    cy.get("tbody tr:first-child td.field-import_config_link a").click();
    // Check that only one fact has been imported
    cy.get(".field-num_facts a").contains("1");
    // Delete the import config
    cy.get("a").contains("Delete").click();
    cy.get("input[type=submit]").click();
  });
});
