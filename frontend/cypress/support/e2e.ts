import "./commands";
import "cypress-axe";
import "cypress-wait-until";
import "cypress-network-idle";

import verifyDownloads from "cy-verify-downloads";

verifyDownloads.addCustomCommand();

Cypress.on("uncaught:exception", (err) => {
  Cypress.log({
    name: "Uncaught Exception",
    message: err.message,
    consoleProps: () => ({
      error: err,
    }),
  });

  console.error("Uncaught Exception:", err);
});
