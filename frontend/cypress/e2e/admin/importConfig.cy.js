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
    cy.get("input[name=reference_period]").type("time");
    cy.get("input[name=remarks]").type("test remarks");
    cy.get("input[name=remarks_is_surrogate]").click();
    cy.get("input[name=period_start]").type("2019");
    cy.get("input[name=period_end]").type("2019");
    cy.get("#id_filters textarea.ace_text-input").clear({ force: true });
    cy.get("#id_filters textarea.ace_text-input").type(
      '{"hhtyp": ["total"], "indic_is": ["h_broad"], "unit": ["pc_hh"], "geo": ["EU27_2020"]}',
      {
        force: true,
        parseSpecialCharSequences: false,
      },
    );
    cy.get("#id_mappings textarea.ace_text-input").clear({ force: true });
    cy.get("#id_mappings textarea.ace_text-input").type(
      '{"breakdown": {"total": "hh_total"}, "country": {"EU27_2020": "EU"}, "reference_period": {"2019": "2000"}}',
      {
        force: true,
        parseSpecialCharSequences: false,
      },
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
    // Check that only one fact has been imported, and open the fact details
    cy.get(".field-num_facts a").contains("1").click();
    cy.get("tbody tr:first-child th.field-indicator a").click();

    // Check imported values
    cy.get("[name=value]").should("have.value", "87.53");
    cy.get(".field-indicator").contains("[h_broad]");
    cy.get(".field-breakdown").contains("[hh_total]");
    cy.get(".field-unit").contains("[pc_hh]");
    cy.get(".field-country").contains("[EU]");
    cy.get(".field-period").contains("[2019]");
    cy.get("[name=reference_period]").should("have.value", "2000");
    cy.get("[name=remarks]").should("have.value", "test remarks");

    // Delete the import config
    cy.get(".field-import_config .view-related").click();
    cy.get("a").contains("Delete").click();
    cy.get("input[type=submit]").click();
  });
});
