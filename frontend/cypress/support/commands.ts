import path from "path";
import { filetypeinfo } from "magic-bytes.js";

Cypress.Commands.addAll(
  {
    prevSubject: true,
  },
  {
    downloadLink(prevSubject) {
      return cy
        .wrap(prevSubject)
        .invoke("attr", "href")
        .then((url) => cy.request(url))
        .its("body");
    },
  }
);

Cypress.Commands.addAll({
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
      .contains("Search for indicators");
  },

  checkExportLink(linkText, expectedType) {
    return cy
      .get("a")
      .contains(linkText)
      .parent("a")
      .invoke("attr", "href")
      .then((url) => {
        cy.request({
          url,
          encoding: null,
        }).then((response) => {
          const detectedTypes = filetypeinfo(new Uint8Array(response.body)).map(
            (info) => info.typename
          );

          expect(expectedType).to.be.oneOf(detectedTypes);
        });
      });
  },
  checkDownload(pattern, expectedType) {
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
          const detectedTypes = filetypeinfo(buffer).map(
            (info) => info.typename
          );

          expect(expectedType).to.be.oneOf(detectedTypes);
        });
      });
  },
  checkChart(
    chartGroup,
    chart,
    { filters = {}, title = [], point = null, tooltip = [], definitions = [] }
  ) {
    // Navigate to the chart
    cy.task("cleanDownloadsFolder")
      .visit("/")
      .get(".ecl-list-illustration a")
      .contains(chartGroup)
      .click()
      .get(".ecl-list-illustration a")
      .contains(chart)
      .click();

    // Set the filters
    for (const filtersKey in filters) {
      cy.selectFilter(filtersKey, filters[filtersKey]);
    }

    const checkChartInstance = () => {
      // Check chart title/subtitle
      cy.get(".highcharts-title, .highcharts-subtitle")
        .invoke("text")
        .then((text) => {
          for (const txt of title) {
            // Highcharts adds ZeroWidthSpaces in the text, so we can't
            // check normally
            expect(text.replace(/[\u200B-\u200D\uFEFF]/g, " ")).to.contain(txt);
          }
        });

      // Check a point in the chart and the tooltip
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

    // Check chart definitions
    for (const txt of definitions) {
      cy.get(".chart-definitions").contains(txt);
    }

    // Check downloading the chart as a png
    // XXX This is unstable disable for now!
    // if (title.length > 0) {
    //   cy.get("a")
    //     .contains("Download image")
    //     .click()
    //     .checkDownload(/png$/, "png");
    // }

    // Check the export data link
    cy.checkExportLink("Export data", "xlsx");

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
});
