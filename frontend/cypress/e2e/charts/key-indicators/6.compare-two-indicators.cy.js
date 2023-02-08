import describeResponsive from "../../../describeResponsive";

describeResponsive("Check Chart", () => {
  it("Check Chart", () => {
    cy.checkChart("Key Indicators", "Compare two indicators", {
      filters: {
        indicatorGroupX: "Digital Skills",
        indicatorX: "ICT graduates",
        breakdownX: "Females",
        periodX: "2019",
        unitX: "% of graduates",
        indicatorGroupY: "Digital Skills",
        indicatorY: "ICT graduates",
        breakdownY: "Males",
        unitY: "% of graduates",
      },
      title: ["Year: 2019"],
      point: "EU, 3.1. European Union.",
      tooltip: ["European Union", "0.8% of graduates", "3.1% of graduates"],
    });
  });
});
