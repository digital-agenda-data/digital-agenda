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
    }
  }
}
