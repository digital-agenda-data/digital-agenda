import path from "path";
import { filetypemime } from "magic-bytes.js";

export default {
  selectFilter(inputName, label) {
    return cy
      .get(`[data-name='${inputName}']`)
      .click()
      .get(`[data-name='${inputName}'] [role='option']`)
      .contains(label)
      .click();
  },
  searchIndicators(searchQuery) {
    cy.visit("/")
      .window()
      .then((remoteWindow) => {
        if (remoteWindow.innerWidth < 996) {
          // Search input is hidden on mobile, and needs to be toggled
          cy.get(".ecl-site-header__search-toggle").click();
        }
      });

    cy.get("form.ecl-search-form input[type=search]")
      .type(searchQuery)
      .get("form.ecl-search-form [type=submit]")
      .click()
      .get("h1")
      .contains("Search results for");
  },
  checkDownload(pattern, expectedMime) {
    cy.waitUntil(() =>
      cy
        .task("downloads")
        .then(
          (files: Array<string>) =>
            files.filter((fn) => fn.match(pattern)).length === 1
        )
    )
      .task("downloads")
      .then((files: Array<string>) => {
        const downloadsFolder = Cypress.config("downloadsFolder");
        const fullPath = path.join(
          downloadsFolder,
          files.find((fn) => fn.match(pattern))
        );

        cy.readFile(fullPath, null).then((buffer) => {
          expect(expectedMime).to.be.oneOf(filetypemime(buffer));
        });
      });
  },
  checkChart(
    chartGroup,
    chart,
    { filters = {}, title = [], point = null, tooltip = [], definitions = [] }
  ) {
    cy.task("cleanDownloadsFolder")
      .visit("/")
      .get(".ecl-list-illustration a")
      .contains(chartGroup)
      .click()
      .get(".ecl-list-illustration a")
      .contains(chart)
      .click();

    for (const filtersKey in filters) {
      cy.selectFilter(filtersKey, filters[filtersKey]);
    }

    const checkChartInstance = () => {
      cy.get(".highcharts-title, .highcharts-subtitle")
        .invoke("text")
        .then((text) => {
          for (const txt of title) {
            // Highcharts adds ZeroWidthSpaces in the text, so we can't
            // check normally
            expect(text.replace(/[\u200B-\u200D\uFEFF]/g, " ")).to.contain(txt);
          }
        });

      if (point) {
        cy.get(`.highcharts-point[aria-label='${point}']`)
          .should("be.visible")
          .trigger("mouseover", { force: true });

        for (const txt of tooltip) {
          cy.get(".highcharts-tooltip").should("contain", txt);
        }
      }
    };

    checkChartInstance();

    for (const txt of definitions) {
      cy.get(".chart-definitions").contains(txt);
    }

    if (title.length > 0) {
      cy.get("a")
        .contains("Download image")
        .click()
        .checkDownload(/png$/, "image/png");
    }

    // Check the chart again in embedded mode
    cy.get("a")
      .contains("Embedded URL")
      .parent("a")
      .invoke("attr", "href")
      .then((href) => {
        // Can't click on in since it opens in a new tab
        cy.visit(href);
        checkChartInstance();
      });

    return cy;
  },
};
