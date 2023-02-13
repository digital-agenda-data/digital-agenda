export {};

declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Cypress {
    interface Chainable {
      /**
       * Custom command to select an item from EclSelect component
       * @example cy.selectFilter("breakdown", "Total")
       */
      selectFilter(
        inputName: string,
        label: string
      ): Chainable<JQuery<HTMLElement>>;

      /**
       * Open the "search indicators" input in the site header, type in
       * the search query and perform the search.
       * @example cy.searchIndicators("social media")
       */
      searchIndicators(searchQuery: string): Chainable<JQuery<HTMLElement>>;

      /**
       * Download a link and pass the response to the chain
       * @example cy.get("a").contains("Export data").downloadLink().should("contain", "foo.bar")
       */
      downloadLink(): Chainable<string>;

      /**
       * Check if the file has been downloaded and verify magic numbers to
       * match the specified type.
       * @example cy.checkDownload(/.*\.png/, "png")
       */
      checkDownload(pattern: RegExp, expectedType: string): Chainable<void>;

      /**
       * Check if an export link and verify magic numbers to match the
       * specified type.
       * @example cy.checkExportLink("Export data", "xlsx")
       */
      checkExportLink(
        linkText: string,
        expectedType: string
      ): Chainable<string>;

      /**
       * Perform checks for a chart page
       */
      checkChart(
        chartGroup: string,
        chart: string,
        config: { filters; title; point; tooltip; definitions }
      ): Chainable<undefined>;
    }
  }
}
