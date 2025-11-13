import "./commands";
import "cypress-axe";
import "cypress-wait-until";
import "cypress-network-idle";

import verifyDownloads from "cy-verify-downloads";

verifyDownloads.addCustomCommand();

Cypress.on("uncaught:exception", (err) => {
  console.error(err);
});
