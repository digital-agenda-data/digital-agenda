export {};

declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Custom command to select an item from EclSelect component
       * @example cy.selectFilter("breakdown", "Total")
       */
      selectFilter(inputName: string, label: string): Chainable<JQuery<HTMLElement>>

      /**
       * Open the "search indicators" input in the site header, type in
       * the search query and perform the search.
       * @example cy.searchIndicators("social media")
       */
      searchIndicators(searchQuery: string): Chainable<JQuery<HTMLElement>>

      /**
       * Check if the file has been downloaded and has the expected mime-type
       * @example cy.checkDownload("test.png", "image/png")
       */
      checkDownload(fn: string, expectedMime: string): Chainable<void>

      /**
       * Perform checks for a chart page
       */
      checkChart(chartGroup: string, chart: string, config: { filters, title, point, tooltip, definitions }): Chainable<undefined>
    }
  }
}
