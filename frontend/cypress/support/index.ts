export {};

declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Custom command to select an item from EclSelect component
       * @example cy.selectFilter("breakdown", "Total")
       */
      selectFilter(inputName: string, label: string): Chainable<JQuery<HTMLElement>>
    }
  }
}
