import dotenv from "dotenv";

dotenv.config({ path: "../.env" });

import { verifyDownloadTasks } from "cy-verify-downloads";
import { defineConfig } from "cypress";
import { readdirSync, rmSync } from "node:fs";
import { plugin as cypressGrepPlugin } from "@cypress/grep/plugin";

export default defineConfig({
  e2e: {
    specPattern: "cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}",
    baseUrl: "http://localhost:4173",
  },
});

// XXX We don't actually know which one we should use
// XXX if there are more than one!
const backendHost = process.env.BACKEND_HOST?.split(",")?.[0];
const frontendHost = process.env.FRONTEND_HOST?.split(",")?.[0];

module.exports = defineConfig({
  scrollBehavior: "center",
  env: {
    backendHost,
    frontendHost,
    grepFilterSpecs: true,
    grepOmitFiltered: true,
    grepIntegrationFolder: ".",
  },
  e2e: {
    baseUrl: `http://${frontendHost}`,
    // Viewport used for non-responsive checks (e.g. checks in the admin)
    viewportWidth: 1920,
    viewportHeight: 1080,
    // List of viewports used for responsive checks. All tests responsive
    // tests are run on the entire list here. (Using `describeResponsive`)
    viewports: [
      // 4k
      [2560, 1440],
      // Desktop
      [1920, 1080],
      // Tablet
      [1024, 768],
      [768, 1024],
      // Phone
      [414, 896],
      [360, 640],
    ],
    setupNodeEvents(on, config) {
      on("before:browser:launch", (browser = {}, launchOptions) => {
        // Start browsers with prefers-reduced-motion set to "reduce" to avoid flakyness from
        // waiting for animations to finish.
        if (browser.name === "electron") {
          launchOptions.preferences.prefersReducedMotion = true;
        } else if (browser.family === "chromium") {
          launchOptions.args.push("--force-prefers-reduced-motion");
        } else if (browser.family === "firefox") {
          launchOptions.preferences["ui.prefersReducedMotion"] = 1;
        }

        return launchOptions;
      });
      on("task", verifyDownloadTasks);
      on("task", {
        log(message) {
          console.log(message);
          return null;
        },
        table(message) {
          console.table(message);
          return null;
        },
        cleanDownloadsFolder() {
          rmSync(config.downloadsFolder, {
            recursive: true,
            force: true,
          });
          return null;
        },
        downloads() {
          return readdirSync(config.downloadsFolder);
        },
      });
      cypressGrepPlugin(config);
      return config;
    },
  },
  retries: {
    // Configure retry attempts for `cypress run`
    // Default is 0
    runMode: 3,
    // Configure retry attempt for `cypress open`
    // Default is 0
    // openMode: 0,
  },
});
