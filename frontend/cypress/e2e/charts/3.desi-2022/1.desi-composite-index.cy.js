import describeResponsive from "../../../support/describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.navigateToChart("Digital Economy and Society Index", "composite index");
    // Fiddle with one of the sliders
    cy.get("input[type=range][name=desi_hc]")
      .invoke("val", 10)
      .trigger("input", { force: true });
    // Check the chart and verify that the values were indeed adjusted
    cy.checkChart({
      title: ["Digital Economy and Society Index", "Year: 2022"],
      point: "European Union, 18.299184242424243. Human Capital.",
      tooltip: [
        "European Union",
        "Human Capital",
        "18.30 weighted score (0 to 100)",
      ],
      definitions: [
        "Indicator: Digital Economy and Society Index",
        "Definition: DESI overall index, calculated as the weighted average of the four main DESI dimensions with the weights selected by the user.",
        "Breakdown: Human Capital",
        "Breakdown: Connectivity",
        "Breakdown: Integration of Digital Technology",
        "Breakdown: Digital Public Services",
        "Unit of measure: weighted score (0 to 100)",
        "Definition: Weighted score of the DESI dimension",
      ],
    });
  });
});
