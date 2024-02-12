describe("Check user admin functionality", () => {
  it("Check login admin", () => {
    cy.login();
    cy.get("a").contains("Users").click();
    cy.get("a").contains("Add user");
  });
  it("Check login inactive", () => {
    cy.login("inactive@example.com", "inactive");
    cy.get(".errornote").contains(
      "Please enter the correct email and password for a staff account.",
    );
    cy.get("a").contains("Users").should("not.exist");
  });
  it("Check login user", () => {
    cy.login("user@example.com", "user");
    cy.get("a").contains("Users").should("not.exist");
    cy.get("p").contains("You don’t have permission to view or edit anything.");
  });
});
