export {};

interface CheckChartConfig {
  filters?: object;
  title?: string[];
  point?: string;
  tooltip?: string[];
  definitions?: string[];
  xAxis?: string[];
  yAxis?: string[];
  xAxisTitle?: string[];
  yAxisTitle?: string[];
  legend?: string[];
}

declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Cypress {
    interface Chainable {
      /**
       * Log into the admin UI
       */
      login(user?: string, password?: string): Chainable<JQuery<HTMLElement>>;
      /**
       * Custom command to select an item from EclSelect component
       * @example cy.selectFilter("breakdown", "Total")
       */
      selectFilter(
        inputName: string,
        label: string,
      ): Chainable<JQuery<HTMLElement>>;

      /**
       * Check that the filter is set to the specified value
       * @example cy.checkFilter("breakdown", "Total")
       */
      checkFilter(
        inputName: string,
        label: string,
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
       * @example cy.checkDownload(".png", "png")
       */
      checkDownload(pattern: string, expectedType: string): Chainable<void>;

      /**
       * Check if an export link and verify magic numbers to match the
       * specified type.
       * @example cy.checkExportLink("Export data", "xlsx")
       */
      checkExportLink(
        linkText: string,
        expectedType: string,
      ): Chainable<string>;

      /**
       * Navigate to a chart
       */
      navigateToChart(chartGroup: string, chart: string): void;

      /**
       * Check if the selector contains all the specified texts.
       * Ignores ZeroWidthSpaces.
       */
      hasTexts(selector: string, texts?: string[]): void;

      /**
       * Check for the existence of the specified point.
       * Force hover it and check the tooltip contents to match.
       */
      checkPoint(point: string, tooltip?: string[]): void;
      /**
       * Perform checks for a chart page.
       *  - set specified filters
       *  - check the chart instance
       *  - check export link
       *  - check share url, and recheck chart instance
       *  - check the embedded url, and recheck chart instance
       */
      checkChart(config: CheckChartConfig): Chainable<undefined>;

      /**
       * Check the chart instance:
       *  - check credits
       *  - check filters are correctly set
       *  - check title/subtitle
       *  - check xAxis/yAxis labels
       *  - check the specified point in the chart
       *  - check the tooltip of the specified point
       */
      checkChartInstance(config: CheckChartConfig): Chainable<undefined>;
    }
  }
}
