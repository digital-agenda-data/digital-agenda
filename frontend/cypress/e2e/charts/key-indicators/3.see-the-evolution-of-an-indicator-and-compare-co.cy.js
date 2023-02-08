import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.checkChart(
      "Key Indicators",
      "See the evolution of an indicator and compare countries",
      {
        filters: {
          indicatorGroup: "Digital Skills",
          indicator: "ICT graduates",
          breakdown: "Females",
          unit: "% of graduates",
        },
        title: ["ICT graduates, Females"],
        point: "2019, 0.8. European Union.",
      }
    );
  });
});
