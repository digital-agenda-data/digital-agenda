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
  },
);

Cypress.Commands.addAll({
  login(user = "admin@example.com", password = "admin") {
    const host = Cypress.env("backendHost");
    cy.visit(`${host}/admin/`);
    cy.get("input[name=username]").type(user);
    cy.get("input[name=password]").type(password);
    return cy.get("input[type=submit]").click();
  },
  checkHasChartData() {
    cy.get(".chart-filter [data-name]")
      .filter(":visible")
      .each((el) => {
        cy.wrap(el)
          .find(".multiselect__single, .multiselect__tag")
          .first()
          .contains(/.+/);
      });
    cy.get(".highcharts-no-data").should("not.exist");
    cy.get(".highcharts-point").should("exist");
  },
  checkNavigateBetweenCharts(chartGroup, chartNames) {
    cy.navigateToChart(chartGroup, chartNames[0]);
    cy.checkHasChartData();
    for (const nextChart of chartNames.slice(1)) {
      cy.get("a").contains(nextChart).click();
      cy.checkHasChartData();
    }
  },
  checkFilter(inputName, label) {
    if (!Array.isArray(label)) {
      return cy
        .get(`[data-name='${inputName}'] .multiselect__single`)
        .contains(label);
    }
  },
  selectFilter(inputName, label) {
    // Wait for multiselect to be rendered but wai until it's finished loading
    cy.get(`[data-name='${inputName}']`).should("exist");
    cy.get(`[data-name='${inputName}'][data-loading=true]`).should("not.exist");
    // Then click it to reveal the dropdown
    cy.get(`[data-name='${inputName}']`).click();

    if (!Array.isArray(label)) {
      cy.get(`[data-name='${inputName}'] [role='option']`)
        .contains(label)
        .click();
    } else {
      for (const item of label) {
        cy.get(`[data-name='${inputName}'] [role='option']`)
          .contains(item)
          .closest("[role='option']")
          .then(($el) => {
            const checkbox = $el.find("input[type=checkbox]");
            if (!checkbox.is(":checked")) {
              cy.wrap($el).click();
            }
            cy.wrap(checkbox).should("be.checked", true);
          });
      }
    }
    // Wait for the dropdown to disappear and make sure the option we wanted
    // was selected.
    cy.get(`[data-name='${inputName}'] input[type=text]`)
      .first()
      .type("{esc}", { force: true });
    cy.get(`[data-name='${inputName}'] .multiselect__content`).should(
      "not.exist",
    );
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

    cy.get("form.ecl-search-form input[type=search]").type(searchQuery);
    cy.get("form.ecl-search-form [type=submit]").click();
    cy.get("h1").contains("Search for indicators");
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
            (info) => info.typename,
          );

          expect(expectedType).to.be.oneOf(detectedTypes);
        });
      });
  },
  checkDownload(pattern, expectedType) {
    cy.verifyDownload(pattern, { contains: true });
    cy.task("downloads").then((files: Array<string>) => {
      const downloadsFolder = Cypress.config("downloadsFolder");
      const fullPath = path.join(
        downloadsFolder,
        files.find((fn) => fn.includes(pattern)),
      );

      cy.readFile(fullPath, null).then((buffer) => {
        const detectedTypes = filetypeinfo(buffer).map((info) =>
          info.typename.toLowerCase(),
        );

        expect(expectedType.toLowerCase()).to.be.oneOf(detectedTypes);
      });
    });
  },
  navigateToChart(chartGroup, chart) {
    cy.visit("/");
    cy.get(".ecl-list-illustration a").contains(chartGroup).click();
    cy.get(".ecl-list-illustration a").contains(chart).click();
  },
  hasTexts(selector, texts = []) {
    if (!texts?.length) return;

    cy.get(selector)
      .invoke("text")
      .then((text) => {
        for (const txt of texts) {
          // Highcharts adds ZeroWidthSpaces in the text, so we can't
          // check normally. If the space is preceded by a hyphen, remove it
          // completely as it will introduce a false space between two values.
          // (e.g. Age 16- 18)
          expect(
            text
              .replace(/-[\u200B-\u200D\uFEFF]/, "-")
              .replace(/[\u200B-\u200D\uFEFF]/g, " ")
              .replace(/\s+/g, " "),
          ).to.contain(txt);
        }
      });
  },
  checkPoint(point, tooltip = []) {
    cy.get(`.highcharts-point[aria-label='${point}']`).should("be.visible");
    if (tooltip && tooltip.length > 0) {
      // Triggering focus first allows for tooltips to appear on "spline" charts as well.
      // As just using mouse events doesn't work for them for some reason.
      // XXX Although I'm not sure if it's always on the correct point
      cy.get(`.highcharts-point[aria-label='${point}']`).trigger("focus", {
        force: true,
      });
      cy.get(`.highcharts-point[aria-label='${point}']`).trigger("mouseover", {
        force: true,
      });

      for (const txt of tooltip) {
        cy.get(".highcharts-tooltip").should("contain", txt);
      }
    }
  },
  checkChartInstance({
    filters = {},
    title = [],
    point = null,
    pointNr = null,
    tooltip = [],
    definitions = [],
    xAxis = [],
    yAxis = [],
    xAxisTitle = [],
    yAxisTitle = [],
    legend = [],
  }) {
    // Check credits
    cy.get(".highcharts-credits").contains("European Commission");

    // Check chart definitions
    for (const txt of definitions) {
      cy.get(".chart-definitions").contains(txt);
    }

    // Check the filters
    for (const filtersKey in filters) {
      cy.checkFilter(filtersKey, filters[filtersKey]);
    }

    // Check a point in the chart and the tooltip
    if (point) {
      cy.checkPoint(point, tooltip);
    }

    if (pointNr !== null) {
      cy.get(".highcharts-series-group .highcharts-point").should(
        "have.length",
        pointNr,
      );
    }

    // Check various texts
    cy.hasTexts(".highcharts-title, .highcharts-subtitle", title);
    cy.hasTexts(".highcharts-xaxis-labels text", xAxis);
    cy.hasTexts(".highcharts-xaxis .highcharts-axis-title", xAxisTitle);
    cy.hasTexts(".highcharts-yaxis-labels text", yAxis);
    cy.hasTexts(".highcharts-yaxis .highcharts-axis-title", yAxisTitle);
    cy.hasTexts(".highcharts-legend-item text", legend);
  },
  checkChart(config) {
    cy.task("cleanDownloadsFolder");
    // Wait for loading
    cy.get(".chart-container-digital-agenda").should("exist");
    cy.get(".chart-container-digital-agenda .lds-app-loader").should(
      "not.exist",
    );

    // Set the filters
    for (const filtersKey in config.filters ?? {}) {
      cy.selectFilter(filtersKey, config.filters[filtersKey]);
    }

    // Check the chart instance after all the filters have been set.
    cy.checkChartInstance(config);

    // Check downloading the chart as a png
    cy.get("a").contains("Download image").click();
    cy.checkDownload(".png", "png");

    // Check downloading the chart as a png
    cy.get("a").contains("Download SVG").click();
    cy.checkDownload(".svg", "svg");

    // Check the export data link
    cy.checkExportLink("Export data", "xlsx");

    // Check share link
    cy.get("button").contains("Share").click();
    cy.get(".ecl-social-media-share input[type=text]")
      .invoke("val")
      .then((value) => {
        // Navigate to the short URL and check the chart again.
        // Everything should be the same as the backend should redirect
        // us to the exact same page as before.
        cy.visit(value.toString());
        cy.checkChartInstance(config);
      });

    // Check the chart again in embedded mode
    cy.get("a")
      .contains("Embedded URL")
      .parent("a")
      .invoke("attr", "href")
      .then((href) => {
        // Can't click on in since it opens in a new tab, so
        // navigate and check the chart again. Everything should
        // still be the same, but embedded instead.
        cy.visit(href);
        cy.checkChartInstance({
          ...config,
          // No filters of definitions in the embedded mode of the chart
          filters: {},
          definitions: [],
        });
      });

    return cy;
  },
});
