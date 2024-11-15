import describeResponsive from "../support/describeResponsive";

describeResponsive("Check accessibility page", () => {
  it("Check page", () => {
    cy.visit("/");
    cy.get("a").contains("Accessibility statement").click();
    cy.get("h1").contains("Accessibility statement");
    cy.get("h2").contains("Compliance status");
  });
});
